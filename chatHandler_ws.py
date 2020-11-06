import logging
import websocket
import json
import re

try:
    import thread
except ImportError:
    import _thread as thread

connection_string = 'ws://irc-ws.chat.twitch.tv:80'
config_filename = 'chat_config.json'

log = logging.getLogger(__name__)


class ChatHandlerWS(object):
    """
    Handles Twitch messages from websocket connection
    """

    def __init__(self):
        """
        Initialize web socket chat handler
        """
        websocket.enableTrace(True)
        config_file = open(config_filename, mode='r')
        self.configuration = json.load(config_file)
        config_file.close()
        self.new_message = False
        self.message = ""
        self.temp_msg = ""
        self.connected = False
        self.ws = None
        log.info('ChatHandler initiated')

    def ws_connect(self):
        """
        Connect to ws server
        :return:
        """
        self.ws = websocket.WebSocketApp(url=connection_string, on_error=self.on_error,
                                         on_close=self.on_close,
                                         on_message=self.on_message)
        self.ws.on_open = self.on_open
        thread.start_new_thread(self.ws.run_forever, ())

    def ws_disconnect(self):
        """
        Disconnect from ws server
        :return:
        """
        self.ws.close()

    def on_open(self):
        """
        Callback on websocket opening
        Sends opening sequence to connect to twitch
        :return:
        """
        print("On open")
        self.ws.send('PASS {}'.format(self.configuration['token']))
        self.ws.send('NICK {}'.format(self.configuration['user']))
        self.ws.send('JOIN #{}'.format(self.configuration['channel']))
        # now lets connect to chat
        self.ws.send('CAP REQ :twitch.tv/tags twitch.tv/commands')
        self.connected = True
        log.info('Connection established')

    def on_error(self, error):
        """
        Call back on error
        :param error:
        :return:
        """
        log.info(f"On Error:{error}")

    def on_close(self):
        """
        Callback from connection closed
        :return:
        """
        log.info(f"On close")
        self.connected = False

    def on_message(self, msg):
        """
        Callback when WS receive message
        :param msg: the message received
        :return:
        """
        log.debug(f"message received: {msg}")

        if 'PING :tmi.twitch.tv' in msg:
            log.info('Received PING replying with PONG')
            self._send_pong()

        if 'PRIVMSG' in msg:
            log.info('Found PRIVMSG')
            self.message = self._parse_message(msg)
            self.new_message = True

    def _send_pong(self):
        """
        Twitch sends a PING that verify client live status.
        We must respond with a PONG
        :return:
        """
        self.ws.send('PONG :tmi.twitch.tv')

    def _parse_message(self, message):
        """
        Parse receive message to see if its a user message
        :param message: received string from websocket
        :return: formated message to display
        """
        new_msg = ""
        try:
            # matches a user
            match = re.search(r"([a-z,_,0-9]+)@[a-z,_,0-9]+.tmi.twitch.tv", message, flags=re.IGNORECASE)
            if match:
                new_msg = match.group(1)
                # matches the message from user
                match = re.search(r"PRIVMSG #[a-z,A-Z,0-9,_]+ :([\S,\s]+)$", message, flags=re.IGNORECASE)
                new_msg += " ---> " + match.group(1)
        except:
            return 'Message error'
        return new_msg

    def is_connected(self):
        """
        Returns status of connection
        :return:
        """
        return self.connected
