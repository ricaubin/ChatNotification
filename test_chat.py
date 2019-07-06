from chatHandler import ChatHandler
import logging
from time import sleep

logging.basicConfig(level=logging.INFO)

chat = ChatHandler()
chat.connect()

while True:
    chat.verify_text()
    sleep(0.5)
    if chat.new_message:
        print(chat.message)
        chat.new_message = False
