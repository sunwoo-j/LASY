# LASY - Assistant for Latin Poetry Scansion

## Overview
**LASY (Latin Assistant for Scansion)** is a tool designed to help with the scansion of Latin poetry, specifically for lines written in dactylic hexameter or pentameter. This program aims to be a supportive aid for students and enthusiasts of Latin literature.

### Important Note
LASY assumes that any input provided is a valid line of Latin poetry. While it can be a helpful tool for checking scansion, it may not always be accurate, especially with self-created lines of poetry. It is recommended to use LASY as a secondary resource, with primary guidance coming from teachers and peers. The program does not encompass the full complexity of Latin literature and may have limitations in its accuracy. 

## Features
- **Scansion of Latin Poetry**: Enter a line of Latin poetry to receive a scansion analysis.
- **Custom Dictionary**: Add new words to the program’s dictionary to enhance its understanding and accuracy.
- **Quiz Functionality**: Add new quiz lines to test your knowledge and practice Latin scansion.

## How to Add New Words to the Dictionary
1. Navigate to the `Text` folder and open `dictionary.txt`.
2. On a new blank line, write the word in the following format:
   ```
   [word]@[alternative forms]@[definitions]@[part of speech, conjugation/declension etc.]
   ```
   - **Example**: `mensa@mensae@table; meal; course(at a meal)@noun f 1`
3. Save the file. The new word will be incorporated into the dictionary upon reopening the dictionary window.

**Note**: The program automatically sorts the dictionary entries in alphabetical order.

## How to Add New Quiz Lines
1. Navigate to the `Text` folder and open `quiz.txt`.
2. On a new blank line, write the quiz line in the following format:
   ```
   [line]@[meters]
   ```
   - Use `d` for dactyl and `s` for spondee.
   - **Example**: `Hespere, quis caelo fertur crudelior ignis?@dsss`
3. Save the file. The new quiz line will be available upon reopening the quiz window.

**Error Handling**: In case of any errors resulting from edits to `dictionary.txt` or `quiz.txt`, refer to `dictionary_backup.txt` and `quiz_backup.txt` for the latest error-free versions.

## Acknowledgments
Special thanks to:
- Mrs. Nesbit
- Ms. Baird
- Ms. Coll

## Contact
For further assistance or inquiries, please contact jung.snw@gmail.com.

ⓒ Sunwoo Jung, 2020. All rights reserved.
