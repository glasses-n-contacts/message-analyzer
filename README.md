# message-analyzer

Analyzing our text/fb messenger messages

## Setup:
Uses Python 3.6.5.

1. Create a `variables.py` file in the project root directory with the following variables:
```
CONTACT_INFO = <phone number or apple id, whichever is used in imessage, of the recipient of your messages>
ABSOLUTE_PATH = <absolute path to sqlite db, corresponds to ~/Library/Messages/chat.db>
NAME = <Your first name used in fb messenger>
TARGETS = <An array of the names of the users, ie. ['Lucy','Bill']
```

2. Save the html page source file of a fb messenger conversation in a `data` directory created at the root of the project. See `MessageScraper` for more info.

3. Run `pip3 install -r requirements.txt`

## Classes:

1. MessageScraper:
* Gets all iMessage interactions with any other user specified by their phone number or apple id
* Parses page source of fb messenger messages to get interactions with another user.
To get this page source, go to messenger.com, scroll all the way to the beginning of the conversation with the user of
interest, and click "save as" to save it as an html file. Save it in a data/ directory at the root of the project.

2. MessageAnalyzer
* Analyzes the actual text

3. TextClassifier
* Classification of text. Currently used to determine if a text is from Lucy or Bill.
* Current options: Naive bayes, logistic regression, svm.