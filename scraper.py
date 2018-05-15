import subprocess
import sqlite3
import sys
import nltk


class MessageScraper:

    """
    @param self:
    @param contact_info: phone number (ie. +19999999999) or apple id
    @param path_to_db: the absolute path to the chat db, aka the absolute path to ~/Library/Messages/chat.db
    @return
    """
    def __init__(self, path_to_db, contact_info):
        self.contact_info = contact_info
        self.path_to_db = path_to_db

    # contact_info: phone number (ie. +19999999999) or apple id
    def retrieve_texts(self):
        con = sqlite3.connect(self.path_to_db)
        results = con.execute("select is_from_me,text from message where handle_id=(" +
                              "select handle_id from chat_handle_join where chat_id=(" +
                              "select ROWID from chat where guid='iMessage;-;" + self.contact_info + "')" +
                              ")")
        for result in results:
            # Your index is 1, the other person's index is 0
            sender_index, message = result
            tokens = nltk.word_tokenize(message)
            print(tokens)
            if sender_index is 0:
                # do something with your own texts
                continue
            else:  # do something with other person's texts
                continue


if __name__ == '__main__':
    scraper = MessageScraper('/Users/lucyzhang/Library/Messages/chat.db', 'spothorse9.lucy@gmail.com')
    scraper.retrieve_texts()
