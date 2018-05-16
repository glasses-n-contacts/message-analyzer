# message-analyzer

Analyzing our text/fb messenger messages

## Setup:
Create a variables.py file with the following variables:
CONTACT_INFO = <phone number or apple id, whichever is used in imessage, of the recipient of your messages>
ABSOLUTE_PATH = <absolute path to sqlite db, corresponds to ~/Library/Messages/chat.db>
NAME = <Your first name used in fb messenger>

## Classes:

1. MessageScraper:
* Gets all iMessage interactions with any other user specified by their phone number or apple id
* Parses page source of fb messenger messages to get interactions with another user.
To get this page source, go to messenger.com, scroll all the way to the beginning of the conversation with the user of
interest, and click "save as" to save it as an html file. Save it in a data/ directory at the root of the project.

2. Analyzer
* Analyzes the actual text

