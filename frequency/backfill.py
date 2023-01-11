from __future__ import annotations

import csv
import argparse
import collections
from typing import List, Dict, Any


# ===== from anki-connect ===== #
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


# ============================= #


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "expr_field",
        type=str,
        help="exact field name that contains the expression",
    )

    parser.add_argument(
        "--freq-field",
        type=str,
        help="exact field name to fill with the frequency information",
        default="Frequency",
    )

    parser.add_argument(
        "--query",
        type=str,
        help="exact note query to send to Anki",
        default=argparse.SUPPRESS,
    )

    parser.add_argument(
        "--freq-lists",
        nargs="+",
        type=str,
        help="what lists to use to backfill",
        default=["JPDB.txt", "vnsfreq.txt", "vnsfreqSTARS.txt"],
    )

    return parser.parse_args()


# freq is a string since it's not parsed at all by the csv.reader
def create_actions(ids: List[int], freq: str, freq_field: str) -> List[Dict[str, Any]]:
    actions = []
    for i in ids:
        a = {
            "action": "updateNoteFields",
            "version": 6,
            "params": {"note": {"id": i, "fields": {freq_field: freq}}},
        }
        actions.append(a)
    return actions


def main():
    args = get_args()

    if "query" in args:
        query = args.query
    else:
        # queries all notes with an empty frequency field
        query = f"{args.freq_field}:"
    print(f"Querying Anki with: '{query}'")
    notes = invoke("findNotes", query=query)

    if len(notes) == 0:
        print("Cannot find any notes to change. Exiting...")
        return
    print(f"Query found {len(notes)} notes.")

    print("Getting note info...")
    notes_info = invoke("notesInfo", notes=notes)

    # dict[str, list[int]]
    expr_to_nid = collections.defaultdict(list)
    for note_info in notes_info:
        expr = note_info["fields"][args.expr_field]["value"]
        expr_to_nid[expr].append(note_info["noteId"])

    # creates multi action to update multiple notes
    actions = []

    print("Parsing frequency lists...")
    found_exprs = set()
    for file_path in args.freq_lists:
        with open(file_path, encoding="utf-8") as f:
            for line in csv.reader(f, dialect=csv.excel_tab):
                expr, freq = line
                if expr not in found_exprs and expr in expr_to_nid:
                    new_actions = create_actions(
                        expr_to_nid[expr], freq, args.freq_field
                    )
                    actions.extend(new_actions)
                    found_exprs.add(expr)

    confirm = input(
        f"This will change {len(actions)} notes. Type 'yes' to confirm, or anything else to exit.\n> "
    )
    if confirm != "yes":
        print("Reply was not 'yes'. Exiting...")
        return

    print("Updating notes within Anki...")
    invoke("multi", actions=actions)
    print("Done!")


if __name__ == "__main__":
    main()
