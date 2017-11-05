import sys
import time
import random
import telepot
import requests
from session import Session
from telepot.loop import MessageLoop
from telepot.delegate import per_chat_id, create_open, pave_event_space

from pickles_handler import PicklesHandler

import config

TOKEN = config.TELEGRAM_KEY

class User(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.ph = PicklesHandler()
        self.sheets = {}

    def open(self, initial_msg, seed):
        content_type, chat_type, chat_id = telepot.glance(initial_msg)

        try:
            self.remote_user_id = self.ph.get_userid_from_username(chat_id)
        except ValueError as ex:
            print("No user with that id, adding to DB")
            self.remote_user_id = self.ph.new_user(chat_id)

        for sheet in self.ph.get_sheets(self.remote_user_id):
            self.sheets[sheet['name']] = sheet['id']

        self.session = Session(chat_id)
        if self.session.current_sheet_id != None:
            self.handle_commands(initial_msg['text'])
        else:
            self.sender.sendMessage('Welcome, {}. You have no sheet open for writing.'.format(chat_id))

        return True  # prevent on_message() from being called on the initial message

    def send_user_list_of_their_sheets(self):
        sheet_names = list(self.sheets.keys())

        if len(sheet_names) == 0:
            self.sender.sendMessage("You have no sheets!")
        elif len(sheet_names) == 1:
            self.sender.sendMessage("You have one sheet: {}".format("".join(sheet_names[0])))
        else:
            self.sender.sendMessage("Your sheets are: {}".format("".join([name + ", " for name in sheet_names[:-1]]+[sheet_names[-1]])))

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        self.handle_commands(msg['text'])

    def handle_commands(self, msg):
        command = msg.split(' ')[0]
        remainder = msg[len(command)+1:]

        if command == '/sheets':
            self.send_user_list_of_their_sheets()
        elif command == '/open':
            # if sheet exists then open it up and write each new message as a new element
            try:
                if self.session.current_sheet_id != None:
                    self.sender.sendMessage("Closed sheet.")
                self.session.current_sheet_id = self.sheets[remainder]
                self.sender.sendMessage("Opened sheet '{}' for writing.".format(remainder))
            except:
                self.session.current_sheet_id = self.ph.new_sheet(remainder, self.remote_user_id)
                self.sheets[remainder] = self.session.current_sheet_id
                self.sender.sendMessage("Created a sheet called '{}' and opened it for writing.".format(remainder))
        elif command == '/close':
            # close current sheet
            self.session.current_sheet_id = None
        elif command == '/delete':
            # delete a sheet
            raise NotImplemented
        else:
            # write the message to the currently opened sheet.
            if self.session.current_sheet_id != None:
                self.ph.new_element(command+" "+remainder, self.session.current_sheet_id)
            else:
                self.sender.sendMessage("No currently open sheet! Open a sheet for writing with the /open command")

    def on__idle(self, event):
        self.sender.sendMessage('Idling')
        self.session.commit()
        self.close()


bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(types=['private']), create_open, User, timeout=30),
])
MessageLoop(bot).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(10)
