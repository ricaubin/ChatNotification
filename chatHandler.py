import socket
import logging
import re
import json
import io

connection_data = ('irc.chat.twitch.tv', 6667)
config_filename = 'chat_config.json'

log = logging.getLogger(__name__)


class ChatHandler:

    def __init__(self):
        config_file = io.open(config_filename, mode='r')
        self.configuration = json.load(config_file)
        config_file.close()
        self.new_message = False
        self.message = ""
        self.temp_msg = ""
        self.server = 0
        self.connected = False
        log.info('ChatHandler initiated')

    def __delete__(self, instance):
        self.server.close()

    def connect(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect(connection_data)
        self.server.setblocking(False)
        self.server.send(bytes('PASS ' + self.configuration['token'] + '\n\r', 'utf-8'))
        self.server.send(bytes('NICK ' + self.configuration['user'] + '\n\r', 'utf-8'))
        self.server.send(bytes('JOIN #' + self.configuration['channel'] + '\n\r', 'utf-8'))
        # now lets connect to chat
        self.server.send(bytes('CAP REQ :twitch.tv/tags twitch.tv/commands', 'utf-8'))
        self.connected = True
        log.info('Connection established')

    def disconnect(self):
        if self.connected:
            self.server.close()
            self.connected = False

    def _send_pong(self):
        self.server.send(bytes('PONG :tmi.twitch.tv' + '\n\r', 'utf-8'))

    def verify_text(self):
        if self.connected:
            try:
                msg = self.server.recv(4096).decode('utf-8')
                if msg:
                    self.temp_msg += msg
                    log.info('Received message: ' + self.temp_msg)
            except socket.error:
                # ignore the error
                pass

            if self.temp_msg:
                buf = io.StringIO(self.temp_msg, newline=None)
                for new_msg in buf.readlines():
                    if 'PING :tmi.twitch.tv' in new_msg:
                        log.info('Received PING replying with PONG')
                        self._send_pong()

                    if 'PRIVMSG' in new_msg:
                        log.info('Found PRIVMSG')
                        self.message = self._parse_message(new_msg)
                        self.new_message = True

                self.temp_msg = buf.read()

    def is_connected(self):
        return self.connected

    def _parse_message(self, message):
        new_msg = ""
        try:
            # new_msg = re.findall(r'^:([a-zA-Z0-9_]+)!', message)[0] + '>>'
            # new_msg += re.findall(r'PRIVMSG #[a-zA-Z0-9_]+ :(.+)', message)[0]
            match = re.search(r"([a-z,_,0-9]+)@[a-z,_,0-9]+.tmi.twitch.tv", message, flags=re.IGNORECASE)
            if match:
                new_msg = match.group(1)
                match = re.search(r"PRIVMSG #.+ :([\S,\s]+)$", message, flags=re.IGNORECASE)
                new_msg += " >> " + match.group(1)
        except:
            return 'Message error'
        return new_msg

    @staticmethod
    def _check_has_message(data):
        """
        Check if the data from the server contains a message a user
        typed in the chat.
        :param data: the byte string from the server
        :type data: list of bytes
        :return: returns iterator over these messages
        """
        message = ""
        try:
            # match = re.match(r'^:[a-zA-Z0-9_]+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+'
            #              r'\.tmi\.twitch\.tv '
            #             r'PRIVMSG #[a-zA-Z0-9_]+ :.+$', data)
            match = re.search(r"([a-z,_,0-9]+)@[a-z,_,0-9]+.tmi.twitch.tv", data, flags=re.IGNORECASE)
            if match:
                message = match.group(1)
                match = re.search(r"PRIVMSG #.+ :(.+)$", data)
                message += ": " + match.group(1)
        except IndexError:
            log.error('Index error in match')
        return message
