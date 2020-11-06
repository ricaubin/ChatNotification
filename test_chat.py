import logging
from time import sleep
from chatHandler_ws import ChatHandlerWS

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


if __name__ == '__main__':

    chat = ChatHandlerWS()
    try:

        chat.ws_connect()
        while True:
            sleep(0.5)
            if chat.new_message:
                print(chat.message)
                chat.new_message = False
    except KeyboardInterrupt as e:
        log.info("Keyboard interrupt... leaving")
        chat.ws_disconnect()
        del chat

