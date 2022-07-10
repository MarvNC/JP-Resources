# JP Resources

My contributions to the Japanese learning community.

## Sorting mined Anki cards by frequency

When reading and adding cards from the content you're reading, you'll come across a variety of words with varying degrees of usefulness. Especially as a beginner, you'll want to learn the useful words as soon as possible and learn the less useful words later. With this we can sort a backlog of mined cards by frequency using various installed Yomichan frequency lists.

This handlebar for Yomichan will add a `{freq}` field that will send the first frequency value available to Anki in a numerical format. 

- First, in your Anki card template create a new field for frequency, we can name this `Frequency` or whatever you like.
![anki_Fields_for_Mining_2022-07-10_10-12-31](https://user-images.githubusercontent.com/17340496/178155071-52bcbf17-ba00-4acf-8491-2887670e5798.png)

- Then in Yomichan options, insert the following handlebar code at the end of the menu in `Configure Anki card templates...`.
![chrome_Yomichan_Settings_-_Google_Chrome_2022-07-10_10-10-26](https://user-images.githubusercontent.com/17340496/178155060-f6d9608c-e263-496e-a495-824fff282950.png)

```handlebars
{{#*inline "freq"}}
    {{~#if (op ">" definition.frequencies.length 0)~}}
        {{#regexReplace "[^\d]" ""}}
            {{definition.frequencies.[0].frequency}}
        {{/regexReplace}}
    {{~/if~}}
{{/inline}}
```

- In `Configure Anki card format...`, we may need to refresh the card model for the new field to show up. To do this, change the model to something else and change it back. This will clear your fields so take a screenshot to remember what you had. When your frequency field shows up, add `{freq}` in its value box to use the handlebar.
![chrome_Yomichan_Settings_-_Google_Chrome_2022-07-10_10-15-02](https://user-images.githubusercontent.com/17340496/178155079-7d1a9939-e494-416f-871e-128f3edeff0c.png)

### Usage

