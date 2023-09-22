from __future__ import annotations

import csv
import argparse
import collections
import re
from typing import List, Dict, Any
from dict_names import dict_names


# ========================== from anki-connect =========================== #

# https://github.com/FooSoft/anki-connect#python
import json
import urllib.request

def request(action, **params):
    return {"action": action, "params": params, "version": 6}


def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode("utf-8")
    response = json.load(
        urllib.request.urlopen(
            urllib.request.Request("http://localhost:8765", requestJson)
        )
    )
    if len(response) != 2:
        raise Exception("response has an unexpected number of fields")
    if "error" not in response:
        raise Exception("response is missing required error field")
    if "result" not in response:
        raise Exception("response is missing required result field")
    if response["error"] is not None:
        raise Exception(response["error"])
    return response["result"]

# =========================================================================== #

rx_HTML = re.compile("<.*?>")

def normalize_expr(expression: str):
    # removes HTML and surrounding whitespace
    return re.sub(rx_HTML, '', expression).strip()

def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "--query",
        type=str,
        help="exact note query to send to Anki",
        default=argparse.SUPPRESS,
    )

    parser.add_argument(
        "--tag",
        type=str,
        help="tag to tag all modified cards with. Use '' to not tag any cards",
        default="backfill-stylized",
    )

    return parser.parse_args()


def create_actions(ids: List[int], html: str, freq_field: str) -> List[Dict[str, Any]]:
    actions = []
    for i in ids:
        a = {
            "action": "updateNoteFields",
            "version": 6,
            "params": {"note": {"id": i, "fields": {freq_field: html}}},
        }
        actions.append(a)
    return actions


# freq is a string since it's not parsed at all by the csv.reader
def format_html(dict_name: str, freq: str) -> str:
    html_string = f'<div class="frequencies__group" data-details="{dict_name}">'\
                            '<div class="frequencies__number">'\
                                f'<span class="frequencies__number-inner">{freq}</span>'\
                            '</div>'\
                            '<div class="frequencies__dictionary">'\
                                f'<span class="frequencies__dictionary-inner">{dict_name}</span>'\
                            '</div>'\
                        '</div>'

    return html_string

def main():
    args = get_args()

    if "query" in args:
        query = args.query
    else:
        # queries all notes with an empty stylized frequency field
        query = f'"note:JP Mining Note" "FrequenciesStylized:"'

    print(f"Querying Anki with: '{query}'")
    notes = invoke("findNotes", query=query)

    if len(notes) == 0:
        print("Cannot find any notes to change. Exiting...")
        return
    print(f"Query found {len(notes)} notes.")

    print("Getting note info...")
    notes_info = invoke("notesInfo", notes=notes)

    expr_to_nid = collections.defaultdict(list)
    nid_to_reading = collections.defaultdict(str)
    for note_info in notes_info:
        # Make sure the note is a JP Mining Note and has correctly named fields
        try:
            if note_info["modelName"] != "JP Mining Note":
                raise KeyError

            word = note_info["fields"]["Word"]
            frequencies_stylized = note_info["fields"]["FrequenciesStylized"]
        except KeyError:
            print('\nThis script is only designed to work for notes of type "JP Mining Note", containing a "Word" field and a "FrequenciesStylized" field.\n')
            print('If you used a custom query, please make sure it only returns notes of type "JP Mining Note"')
            print('You can ensure this by adding \\"note:JP Mining Note\\" to your query.\n')

            print(f'Script failed on the following note of type "{note_info["modelName"]}":')
            print(note_info)
            return

        expr = normalize_expr(word["value"])
        expr_to_nid[expr].append(note_info["noteId"])

        # Get the reading in Hiragana, return empty string if no WordReadingHiragana field or if it's empty
        # Old versions of JPMN don't have this field, so can't assume it exists
        nid_to_reading[note_info["noteId"]] = normalize_expr(note_info["fields"].get("WordReadingHiragana",{}).get("value",''))

    # creates multi action to update multiple notes
    actions = []
    notes_to_tag = set()

    print("Parsing frequency lists...")
    nid_to_html = collections.defaultdict(str)
    for file_path, dict_name in dict_names:
        with open(file_path, 'r', encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                # Remove the newline character
                line = line[:-1]
                # if the freq list has reading info, extract it, otherwise reading = ''
                expr, freq, *reading = line.split('\t')
                reading = reading[0] if reading else ''

                if expr in expr_to_nid:
                    for nid in expr_to_nid[expr]:
                        # If reading information exists in both the note and the list, make sure the readings match
                        if reading and nid_to_reading[nid]:
                            if reading != nid_to_reading[nid]:
                                continue

                        nid_to_html[nid] += format_html(dict_name, freq)

    for nid, html in nid_to_html.items():
        new_actions = create_actions([nid], html, "FrequenciesStylized")
        actions.extend(new_actions)
        notes_to_tag.add(nid)

    input_msg = f"This will change {len(actions)} notes ({len(notes) - len(actions)} notes had no frequencies found). Type 'yes' to confirm, or anything else to exit.\n> "

    confirm = input(input_msg)
    if confirm != "yes":
        print("Reply was not 'yes'. Exiting...")
        return

    tag_notes = {
        "action": "addTags",
        "version": 6,
        "params": {
            "notes": list(notes_to_tag),
            "tags": args.tag
        }
    }

    actions.append(tag_notes)
    print("Updating notes within Anki...")
    invoke("multi", actions=actions)
    print("Done!")


if __name__ == "__main__":
    main()
