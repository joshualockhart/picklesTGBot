import time
import sys
import telepot
from telepot.loop import MessageLoop
from telepot.delegate import per_chat_id, create_open, pave_event_space
import config

TOKEN = config.TELEGRAM_KEY
BACKEND_URL = config.PICKLES_BACKEND_URL

class User(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def open(self, initial_msg, seed):
        content_type, chat_type, chat_id = telepot.glance(initial_msg)
        self.sender.sendMessage('Welcome, {}'.format(chat_id))

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        self.sender.sendMessage("You said: {}".format(msg['text']))

    def on__idle(self, event):
        self.sender.sendMessage('Idling')
        self.close()

bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(types=['private']), create_open, User, timeout=30),
])
MessageLoop(bot).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(10)
