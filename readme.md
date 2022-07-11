My contributions to the Japanese learning community. For questions and support, I can be contacted @Marv [in TheMoeWay](https://learnjapanese.moe/join/).

- [Sorting Mined Anki Cards by Frequency](#sorting-mined-anki-cards-by-frequency)
  - [Usage](#usage)
    - [Frequency Order](#frequency-order)
  - [Backfilling Old Cards](#backfilling-old-cards)
- [Anki Card Blur](#anki-card-blur)
  - [Usage](#usage-1)
    - [Default to Enabled/Disabled](#default-to-enableddisabled)
  - [Non Persistent/NoJS Version](#non-persistentnojs-version)
  - [ShareX Hotkey for NSFW cards](#sharex-hotkey-for-nsfw-cards)

## Sorting Mined Anki Cards by Frequency

When reading and adding cards from the content you're reading, you'll come across a variety of words with varying degrees of usefulness. Especially as a beginner, you'll want to learn the useful words as soon as possible and learn the less useful words later. With this we can sort a backlog of mined cards by frequency using various installed Yomichan frequency lists.

This handlebar for Yomichan will add a `{freq}` field that will send the first frequency value available to Anki in a numerical format. 

- First, in your Anki card template create a new field for frequency, we can name this `Frequency` or whatever you like.
![](images/anki_Fields_for_Mining_2022-07-10_10-12-31.png)

- Then in Yomichan options, insert the following handlebar code at the end of the menu in `Configure Anki card templates...`.
![](images/chrome_Yomichan_Settings_-_Google_Chrome_2022-07-10_10-10-26.png)
```handlebars
{{#*inline "freq"}}
    {{~#if (op ">" definition.frequencies.length 0)~}}
        {{#regexReplace "[^\d]" ""}}
            {{definition.frequencies.[0].frequency}}
        {{/regexReplace}}
    {{~/if~}}
{{/inline}}
```
(This only selects the first frequency list value, if you know a method of selecting the lowest frequency value using handlebars please let me know.)

- In `Configure Anki card format...`, we may need to refresh the card model for the new field to show up. To do this, change the model to something else and change it back. This will clear your fields so take a screenshot to remember what you had. When your frequency field shows up, add `{freq}` in its value box to use the handlebar.
![](images/chrome_Yomichan_Settings_-_Google_Chrome_2022-07-10_10-15-02.png)

### Usage

To sort our new cards by frequency, we need the Anki [Advanced Browser](https://ankiweb.net/shared/info/874215009) addon. Then in your card browser, search for new cards in your mining deck and right click the menu to display your frequency field as shown.
![](images/anki_Browse_(1_of_2224_cards_selected)_2022-07-10_10-22-41.png)

Now we can simply sort our new cards by our frequency field, then press `ctrl + a` to select all and then `ctrl + shift + s` to reorder them all. 

- I personally then select the first thirty or so cards and randomly sort them again using the random sort option for more variability when reviewing.

Alternatively you could use the [AnkiAutoReorder](https://github.com/KamWithK/AnkiAutoReorder) addon. I have not personally tried it though.

#### Frequency Order

As mentioned, this only takes the first available frequency value from your frequency lists, so your list order matters. Order them by how important they are to you, and also by what has the lowest values first. I primarily read VNs, so my list order looks like this:
![](images/chrome_Yomichan_Settings_-_Google_Chrome_2022-07-10_10-41-48.png)

### Backfilling Old Cards

If you already have a large backlog of old cards without frequency values, you might need to fill in these values first or they won't be sorted. You could just opt to finish reviewing these cards first, but there is a hacky method to backfill these cards. But **backup your collection before attempting this, it could cause significant lag to your Anki.**

- Create a frequency list in `.txt` format that contains a list of expressions followed by frequency values. You can use the ones I have created [here](frequency), I recommend downloading the [JPDB](frequency/JPDB.txt) list as it's the most exhaustive. 

- In Anki, go to File -> Import, then select the txt frequency file. Map the first field to your term/expression field, then the second field to your frequency field. **Make sure to enable "Update existing notes when first field matches."** 
![](images/anki_Import_2022-07-10_10-47-55.png)

- This will update your existing notes' frequency values, but it'll also import a LOT of new cards. To delete these new cards, search `added:1 Glossary:` in your card browser. The `added:1` is to find cards added today, and `Glossary:` (change it depending on your field name) is to find cards that have no glossary, as all your existing cards should have it. 

- Then hit `ctrl + a` to select all and `ctrl + del` to delete these new cards. But **be sure** you aren't deleting any valid cards first.

## Anki Card Blur

Adding cards from VNs, we might find some risque content that we still want to look at while reviewing because it's cute. However, you might review in places where you don't always want other people to see your cards. Using this card template, we can blur media in Anki and have the option persist throughout a review session.

- Decide on a tag for NSFW cards. I use `-NSFW` so the tag is sorted first for easy access. If you choose something else you'll need to replace all instances of `-NSFW` in this guide with your tag name (with `ctrl + h` in a text editor or an [online tool](http://www.unit-conversion.info/texttools/replace-text/)).

- Tag your NSFW cards with this tag in Anki (see [ShareX Hotkey](#anki-hotkey-for-nsfw-cards)).

- Download the anki-persistence script (`minified.js` or `script.js`) from [here](https://github.com/SimonLammer/anki-persistence/releases/tag/v1.0.0). Then rename it `__persistence.js` and place it in your Anki [user/media folder](https://docs.ankiweb.net/files.html#file-locations).

- In your card template where you want the image to go, paste in this HTML, renaming `{{Picture}}` to match the name of the field that contains your media.
```html
<div id="main_image" class="{{Tags}}">
  <a onclick="toggleNsfw()">{{Picture}}</a>
</div>
```

- Then, at the end of the template paste in this code: 
```html
<script>
  // nsfw
  (function () {
    const nsfwDefaultPC = true;
    const nsfwDefaultMobile = false;
    const imageDiv = document.getElementById('main_image');
    const image = imageDiv.querySelector('a img');
    if(!image){
      imageDiv.parentNode.removeChild(imageDiv);
    }
    let loaded = false;
    setInterval(() => {
      if (!loaded) {
        if (typeof Persistence === 'undefined') {
          return;
        }
        loaded = true;

        let onMobile = document.documentElement.classList.contains('mobile');
        let nsfwAllowed = onMobile ? nsfwDefaultMobile : nsfwDefaultPC;
        if (Persistence.isAvailable() && Persistence.getItem('nsfwAllowed') == null) {
          Persistence.setItem('nsfwAllowed', nsfwAllowed);
        } else if (Persistence.isAvailable()) {
          nsfwAllowed = Persistence.getItem('nsfwAllowed');
        }
        setImageStyle(nsfwAllowed);
      }
    }, 50);
  })();

  function toggleNsfw() {
    if (Persistence.isAvailable()) {
      let nsfwAllowed = !!Persistence.getItem('nsfwAllowed');
      nsfwAllowed = !nsfwAllowed;
      Persistence.setItem('nsfwAllowed', nsfwAllowed);
      setImageStyle(nsfwAllowed);
    } else {
      setImageStyle(undefined, true);
    }
  }

  function setImageStyle(nsfwAllowed = undefined, toggle = false) {
    const imageDiv = document.getElementById('main_image');
    const image = imageDiv.querySelector('img');

    if (nsfwAllowed != undefined) {
      imageDiv.classList.toggle('nsfwAllowed', nsfwAllowed);
    } else if (toggle) {
      imageDiv.classList.toggle('nsfwAllowed');
    }
  }
</script>
```

Then in your card styling paste in the following css, making sure to replace `-NSFW` with your tag name.

```css
#main_image.nsfwAllowed  {
  border-top: 2.5px dashed fuchsia !important;
}
#main_image {
  border-top: 2.5px solid springgreen;
}
#main_image img {
  cursor: pointer;
}
#main_image.-NSFW {
  border-left: 2.5px dashed red;
  border-right: 2.5px dashed red;
  border-bottom: 2.5px dashed red;
}
#main_image.nsfwAllowed.-NSFW  {
  border-top: 2.5px dashed red !important;
}
#main_image.-NSFW img {
  filter: blur(30px);
}
#main_image.nsfwAllowed img {
  filter: blur(0px) !important;
}
```

### Usage

During a review session, you can click/tap the image to toggle card blurring. When the blurring is enabled, there will be a solid green line at the top of the image. When blurring is not enabled, there will be a fuchsia dotted line, and when the card is NSFW the borders will be dotted red. This option will persist throughout a review session but the setting will reset after exiting the session.

x | Blur disabled | Blur enabled
-- | -- | -- 
SFW | ![](images/anki_Preview_2022-07-10_15-37-54.png) | ![](images/anki_Preview_2022-07-10_15-54-14.png) 
NSFW | ![](images/anki_Preview_2022-07-10_15-37-37.png) | ![](images/anki_Preview_2022-07-10_15-37-34.png)

Media: ハミダシクリエイティブ ©まどそふと

#### Default to Enabled/Disabled

In the code we pasted in the template, there are variables that can change whether it is enabled by default on desktop/mobile, the thought being that this is most for reviewing on a phone. These can be changed with `true` marking that cards will not be blurred by default.

```js
const nsfwDefaultPC = true;
const nsfwDefaultMobile = false;
```

### Non Persistent/NoJS Version

If you want all cards to be blurred by default and for it to stay that way, you can simply do something like this instead. The `.mobile` part can be removed so it works on desktop as well.
html: 
```html
<div class="main_image {{Tags}}">{{Picture}}</div>
```
css: 
```css
.mobile .NSFW img {
  filter: blur(30px);
}

.mobile .NSFW img:hover {
  filter: blur(0px);
}
```

### ShareX Hotkey for NSFW cards

I use the hotkeys in [this guide](https://rentry.co/mining#hotkey-for-screenshot) (highly recommended) for adding images/audio to new cards while reading. For the screenshot hotkey, I have a hotkey in addition to the normal one that adds a `-NSFW` tag to the new card for convenience so they don't have to be tagged manually after creation. In the argument part of step 8, just use this code instead: 
```powershell
-NoProfile -Command "$medianame = \"%input\" | Split-Path -leaf; $data = Invoke-RestMethod -Uri http://127.0.0.1:8765 -Method Post -ContentType 'application/json; charset=UTF-8' -Body '{\"action\": \"findNotes\", \"version\": 6, \"params\": {\"query\":\"added:1\"}}'; $sortedlist = $data.result | Sort-Object -Descending {[Long]$_}; $noteid = $sortedlist[0]; Invoke-RestMethod -Uri http://127.0.0.1:8765 -Method Post -ContentType 'application/json; charset=UTF-8' -Body \"{`\"action`\": `\"updateNoteFields`\", `\"version`\": 6, `\"params`\": {`\"note`\":{`\"id`\":$noteid, `\"fields`\":{`\"Picture`\":`\"<img src=$medianame>`\"}}}}\"; " Invoke-RestMethod -Uri http://127.0.0.1:8765 -Method Post -ContentType 'application/json; charset=UTF-8' -Body \"{ `\"action`\": `\"addTags`\",`\"version`\": 6,`\"params`\": {`\"notes`\": [$noteid],`\"tags`\": `\"NSFW`\"}}\";
```