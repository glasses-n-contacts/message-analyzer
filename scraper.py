import sqlite3
import os
from variables import *
from bs4 import BeautifulSoup


class MessageScraper:

    """
    @param self:
    @param contact_info: phone number (ie. +19999999999) or apple id
    @param path_to_db: the absolute path to the chat db, aka the absolute path to ~/Library/Messages/chat.db
    @param my_name: your first name that's used on fb messenger
    @return
    """
    def __init__(self, path_to_db, contact_info, my_name):
        self.contact_info = contact_info
        self.path_to_db = path_to_db
        self.my_name = my_name

    # contact_info: phone number (ie. +19999999999) or apple id
    def get_texts(self, write_to_file=True):
        con = sqlite3.connect(self.path_to_db)
        results = con.execute("select is_from_me,text from message where handle_id=(" +
                              "select handle_id from chat_handle_join where chat_id=(" +
                              "select ROWID from chat where guid='iMessage;-;" + self.contact_info + "')" +
                              ")")

        if write_to_file:
            directory = "data/"
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Write everything to file
            f0 = open(directory + "message_data0.txt", "w+")
            f1 = open(directory + "message_data1.txt", "w+")

        my_texts = []
        other_texts = []
        for result in results:
            # Your index is 1, the other person's index is 0
            sender_index, message = result
            if (message is None or message.startswith('Laughed at') or message.startswith('Liked “') or
                message.startswith('Loved “') or message.startswith('Disliked “') or
                message.startswith('Emphasized “') or message.startswith('Laughed at ') or
                    len(message) == 0):
                continue
            if sender_index is 0:
                if write_to_file:
                    # do something with others' texts
                    f0.write(message)
                other_texts.append(message)
            else:  # do something with your own texts
                if write_to_file:
                    f1.write(message)
                my_texts.append(message)
        return my_texts, other_texts

    @staticmethod
    def get_messenger_messages():
        directory = "data/BillLucyMessenger.html"
        if not os.path.exists(directory):
            print("This file does not exist")
            return
        with open(directory, encoding="utf-8") as f:
            return_data = {}
            data = f.read()
            soup = BeautifulSoup(data, "html.parser")
            divs = soup.find_all("div", {"class": "_41ud"})
            for div in divs:
                messager_div = div.find("h5")
                messager_name = messager_div.text
                message_div = div.find("div", {"class": "clearfix"})
                message = message_div.text
                if messager_name not in return_data:
                    return_data[messager_name] = []
                else:
                    return_data[messager_name].append(message)

            # Returns a dictionary, with the keys being the user names,
            # and the values being arrays of messages that the user sent
            return return_data

    def all_messages(self):
        messenger_texts = self.get_messenger_messages()
        my_messages = messenger_texts[self.my_name]

        names = messenger_texts.keys()
        other_name = ""
        for name in names:
            if self.my_name != name:
                other_name = name
        other_messages = messenger_texts[other_name]

        my_texts, other_texts = self.get_texts()
        my_messages.extend(my_texts)
        other_messages.extend(other_texts)

        return my_messages, other_messages


if __name__ == '__main__':
    scraper = MessageScraper(ABSOLUTE_PATH, CONTACT_INFO, NAME)
    # scraper.get_texts()
    my_texts, other_texts = scraper.all_messages()
    print(my_texts)
    print(other_texts)
