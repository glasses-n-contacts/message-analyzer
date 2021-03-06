import sqlite3
import os
from variables import *
from bs4 import BeautifulSoup
import pyautogui
import webbrowser
import time
import datetime
import server
import json
import operator
from shutil import copy
from scraper_helper import link_reactions_for_imessages, hook_messenger_attachment


class MessageScraper:

    '''
    @param self:
    @param contact_info: phone number (ie. +19999999999) or apple id
    @param path_to_db: the absolute path to the chat db, aka the absolute path to ~/Library/Messages/chat.db
    @param my_name: your first name that's used on fb messenger
    @return
    '''
    def __init__(self, path_to_db, contact_info, my_name):
        self.contact_info = contact_info
        self.path_to_db = path_to_db
        self.my_name = my_name
        self.database = server.get_db()

    # contact_info: phone number (ie. +19999999999) or apple id
    def get_imessage_texts(self, write_to_file=True, just_get_message=True, include_reaction=False):
        con = sqlite3.connect(self.path_to_db)
        results = con.execute(
            'select is_from_me,text,message.guid,associated_message_guid,' +
            'datetime(date/1000000000 + strftime(\'%s\', \'2001-01-01\') ,\'unixepoch\',\'localtime\'),' +
            'filename ' +
            'from message '
            'left join message_attachment_join on message.ROWID = message_attachment_join.message_id ' +
            'left join attachment on attachment.ROWID = message_attachment_join.attachment_id ' +
            'where handle_id=(' +
            'select handle_id from chat_handle_join where chat_id=(' +
            'select ROWID from chat where guid="iMessage;-;' + self.contact_info + '"))')

        if write_to_file:
            directory = 'data/'
            attachmentDirectory = 'data/attachments'
            if not os.path.exists(directory):
                os.makedirs(directory)
            if not os.path.exists(attachmentDirectory):
                os.makedirs(attachmentDirectory)

            # Write everything to file
            f0 = open(directory + 'message_data0.txt', 'w+')
            f1 = open(directory + 'message_data1.txt', 'w+')
            json0 = open(directory + 'imessage_data0.json', 'w+')
            json1 = open(directory + 'imessage_data1.json', 'w+')
            jsonall = open(directory + 'imessage_all.json', 'w+')

        my_texts = []
        other_texts = []
        allMessages = []
        for result in results:
            # Your index is 1, the other person's index is 0
            sender_index, message, guid, associated_message_guid, date_delivered, attachment_file = result
            if (message is None or len(message) == 0):
                continue

            message_to_text = message + '\n'

            if (associated_message_guid is not None):
                if not include_reaction:
                    continue
                if not just_get_message:
                    message = {
                        'message': message,
                        'date_delivered': date_delivered,
                        'is_reaction': 1,
                        'has_emoji': False,
                        'associated_message_guid': associated_message_guid,
                        'is_from_me': sender_index
                    }
            else:
                if not just_get_message:
                    message = {
                        'message': message,
                        'date_delivered': date_delivered,
                        'guid': guid,
                        'is_reaction': 0,
                        'reactions': [],
                        'is_from_me': sender_index
                    }
                    if attachment_file is not None:
                        message['attachments'] = [{
                            'url': 'http://localhost:5000/attachments/' + os.path.basename(attachment_file)
                        }]
                        if write_to_file:
                            try:
                                copy(os.path.expanduser(attachment_file),
                                     attachmentDirectory)
                            except FileNotFoundError:
                                print('Attachment file not found: ' + attachment_file)
    
            if sender_index is 0:
                if write_to_file:
                    # do something with others' texts
                    f0.write(message_to_text)
                other_texts.append(message)
            else:  # do something with your own texts
                if write_to_file:
                    f1.write(message_to_text)
                my_texts.append(message)
            allMessages.append(message)
        
        if not just_get_message:
            allMessages = link_reactions_for_imessages(allMessages)
        
        if write_to_file:
            json.dump(my_texts, json0)
            json.dump(other_texts, json1)
            json.dump(allMessages, jsonall)
        return my_texts, other_texts, allMessages

    @staticmethod
    def get_fb_messenger_source(fb_username):
        # Move to the center of the screen
        width, height = pyautogui.size()
        pyautogui.moveTo(width/2, height/2)
        # Open the website
        webbrowser.open('https://www.messenger.com/t/' + fb_username)
        while True:
            pyautogui.scroll(200)
            time.sleep(2)  # delays for 2 seconds.
        return

    def get_messenger_messages(self, use_cached_file=False):
        return_data = {}
        directory = 'data/BillLucyMessenger.html'
        if not os.path.exists(directory):
            print('This file does not exist')
            return

        if not os.path.exists('data/messenger_data0.txt'):
            open('data/messenger_data0.txt', 'w+')
        if not os.path.exists('data/messenger_data1.txt'):
            open('data/messenger_data1.txt', 'w+')

        file0 = open('data/messenger_data0.txt', 'r+')  # The other user's messages
        file1 = open('data/messenger_data1.txt', 'r+')  # My messages

        content0 = file0.readlines()
        content1 = file1.readlines()

        other_name = TARGETS[1]
        if len(content0) > 1 and len(content1) > 1 and use_cached_file:
            print('Use cached file')
            for message in content0:
                if self.my_name not in return_data:
                    return_data[self.my_name] = [message.strip('\n')]
                else:
                    return_data[self.my_name].append(message.strip('\n'))
            for message in content1:
                if other_name not in return_data:
                    return_data[other_name] = [message.strip('\n')]
                else:
                    return_data[other_name].append(message.strip('\n'))

            return return_data

        with open(directory, encoding='utf-8') as f:
            data = f.read()
            soup = BeautifulSoup(data, 'html.parser')
            divs = soup.find_all('div', {'class': '_41ud'})
            for div in divs:
                messager_div = div.find('h5')
                messager_name = messager_div.text.strip('\n')
                message_div = div.find('div', {'class': 'clearfix'})
                message = message_div.text

                if other_name in messager_name:
                    file0.write(message + '\n')
                elif self.my_name in messager_name:
                    file1.write(message + '\n')

                if messager_name not in return_data:
                    return_data[messager_name] = [message]
                else:
                    return_data[messager_name].append(message)

            # Returns a dictionary, with the keys being the user names,
            # and the values being arrays of messages that the user sent
            return return_data
    
    # need data/messenger_all.json
    @staticmethod
    def all_messenger_from_json(just_text=False):
        all_messages = []
        with open('data/messenger_all.json') as f:
            data = json.load(f)
            for raw in data:
                if 'message' not in raw:
                    # meta messages
                    continue

                raw_reactions = raw['message_reactions']
                reactions = []
                for raw_reaction in raw_reactions:
                    reaction = {
                        'is_from_me': raw_reaction['user']['id'] == MESSENGER_ID,
                        'has_emoji': True,
                        'emoji': raw_reaction['reaction']
                    }
                    reactions.append(reaction)
                
                time = datetime.datetime.fromtimestamp(float(raw['timestamp_precise'])/1000.0)

                message = {
                    'message': raw['message']['text'],
                    'date_delivered': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'is_reaction': 0,
                    'is_from_me': raw['message_sender']['id'] == MESSENGER_ID,
                    'reactions': reactions
                }

                hook_messenger_attachment(message, raw)
                
                all_messages.append(message)
        
        all_messages = sorted(all_messages, key=operator.itemgetter('date_delivered'))
        if just_text:
            return_messages = {NAME: [], TARGETS[1]: []}
            for message in all_messages:
                if message['is_from_me']:
                    return_messages[NAME].append(message['message'])
                else:
                    return_messages[TARGETS[1]].append(message['message'])
            return return_messages

        return all_messages
    
    def all_for_frontend(self):
        _, _, imessages = self.get_imessage_texts(
            write_to_file=False, just_get_message=False, include_reaction=True
        )
        messengers = self.all_messenger_from_json()
        messages = imessages + messengers
        messages = sorted(messages, key=operator.itemgetter('date_delivered'))
        return messages

    def all_messages(self, write_to_db=True):
        messenger_texts = self.all_messenger_from_json(True) #self.get_messenger_messages()
        my_messages = messenger_texts[self.my_name]

        names = messenger_texts.keys()
        other_name = ''
        for name in names:
            if self.my_name != name:
                other_name = name
        other_messages = messenger_texts[other_name]
        my_texts, other_texts, _ = self.get_imessage_texts()
        my_messages.extend(my_texts)
        other_messages.extend(other_texts)

        if write_to_db:
            self.database.messages.insert_one({'messager': self.my_name, 'messages': my_messages,
                                               'date': datetime.datetime.utcnow()})
            self.database.messages.insert_one({'messager': other_name, 'messages': other_messages,
                                               'date': datetime.datetime.utcnow()})

        return my_messages, other_messages


if __name__ == '__main__':
    scraper = MessageScraper(ABSOLUTE_PATH, CONTACT_INFO, NAME)
    print(scraper.all_messenger_from_json(True))

    # MessageScraper.get_fb_messenger_source(MESSENGER_USERNAME)
    # my_texts, other_texts, allMessages = scraper.get_imessage_texts(
    #     write_to_file=True, just_get_message=False, include_reaction=True)
    # scraper.get_messenger_messages(False)
    # scraper.get_texts()
    # my_texts, other_texts = scraper.all_messages()
    # print(my_texts)
    # print(other_texts)
