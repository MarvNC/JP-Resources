# Changelog

Minor changes will not be reflected here. See the commit history for more details.

## 2023-02-03

Add changelog.

## 2023-01-28

Add a way to specify the default frequency value for the backfill script by @Aquafina-water-bottle.

## 2023-01-27

Make the backfill script ignore html in the expression field by @Staz0r.

## 2023-01-16

Change the frequency handlebar to allow ignoring of frequency dictionaries by @Aquafina-water-bottle.

## 2023-01-14

Clarified python backfill script instructions on powershell backslashes by @Aquafina-water-bottle.

## 2023-01-12

Add a few couple replacement patterns for `-` and `.`.

## 2023-01-10

Add my thoughts on a few frequency dictionaries.

## Before that

(undocumented)



# `freq` Changelog

## v23.02.05.1
- Changed the default sorting method from `min` to `harmonic`

## v23.02.01.1
- Removed redundant (op "+" x) operators (since the initial "f" shorthand already has it)

## v23.01.31.6
- Fixed accidental revert of logic in `v23.01.31.4`

## v23.01.31.5
- Added `debug` sort mode for internal use

## v23.01.31.4
- Added `opt-keep-freqs-past-first-regex` and logic to use only the 1st frequency of a dictionary

## v23.01.31.3
- Apply floor() on harmonic mean and arithmetic mean result
- Only gets the first number as the frequency instead of concatenating all digits together

## v23.01.31.2
- Fixed if statement to properly wrap around all logic

## v23.01.31.2
- Added if statement around harmonic mean to not count numbers that are > 0

## v23.01.28.1
- First recorded version. Previous changes are undocumented.
