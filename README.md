# message-analyzer

Analyzing our text/fb messenger messages

## Setup

Uses Python 3.6.5.

1. Create a `variables.py` file in the project root directory with the following variables:

    ```
    CONTACT_INFO = <phone number or apple id, whichever is used in imessage, of the recipient of your messages>
    ABSOLUTE_PATH = <absolute path to sqlite db, corresponds to ~/Library/Messages/chat.db>
    NAME = <Your first name used in fb messenger>
    TARGETS = <An array of the names of the users, ie. ['Lucy','Bill']
    MONGODB_URI = <MONGO URI of mongodb instance where we're going to store the messages for safekeeping>
    CLIENT_MONGODB = <MONGO client>
    MESSENGER_ID = <Your messenger id, as shown in the data packets -_->
    ```

2. Save the html page source file of a fb messenger conversation in a `data` directory created at the root of the project. See `MessageScraper` for more info.

3. Run `pip3 install -r requirements.txt`

## Classes

1. MessageScraper:

    * Gets all iMessage interactions with any other user specified by their phone number or apple id, including reactions and attachments.

    * Attachments are copied to `data/attachments` with the same filenames.

    * Scrapes page source of fb messenger messages using bs4 to get interactions with another user.

        To get this page source, go to messenger.com, scroll all the way to the beginning of the conversation with the user of
        interest, and click "save as" to save it as an html file. Save it in a data/ directory at the root of the project.

    * I recommend using <http://sqlitebrowser.org> for examining the sqlite database (~/Library/Messages/chat.db) which is what the scraper reads from to get iMessage data.

2. MessageAnalyzer

    * Analyzes the actual text
    * Word clouds
    * Entity recognition

3. TextClassifier

    * Classification of text. Currently used to determine if a text is from Lucy or Bill.

    * Current options: Naive bayes, logistic regression, svm.

## Server

Run `python app.py` to start the server which contains API calls to analyze text.

### Endpoints

- `/imessages`

    Returns all iMessages (in order) in a JSON array. Messages are scrapped again each time the API is requested.

    messasge format:

    ```
    {
        message: text message content,
        date_delivered: delivered date,
        reaction: 1 for reaction, 0 for other,
        associated_message_guid: (only for reactions) the message guid associated with the reaction,
        messager: 1 for 'me', 0 for the other,
        attachment: (only for messages with attachment) filename of the attachment,
        guid: (only for non-reactions) guid of the message,
        reactions: for messenger, reactions are already attached to messages,
        is_system_message: if the message is a messenger system message,
    }
    ```

    reaction format:
    ```
    {
        messager: 1 for 'me', 0 for the other,
        has_emoji: 1 if the message doesn't need to be mapped to an emoji,
        emoji: the reaction emoji, the field only exists if has_emoji == 1,
    }
    ```

- `/attachments/<path:path>`

    Serves attachments by looking for the `path` file in `data/attachments`. `path` should be the filename rather than the complete path (should've been renamed -_-).

    Example:

    `{url}/attachments/violet.png` points to `data/attachments/violet.png`.

More interesting analysis visualizations to come.

