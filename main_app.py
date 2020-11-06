from guizero import App, TextBox, Box, PushButton
from chatHandler_ws import ChatHandlerWS
from notifications import Notifications
import logging

logging.basicConfig(level=logging.WARNING)
base_color = (112, 146, 190)
text_color = "white"
notification_cnt = 0


def verify_chat(mychat: ChatHandlerWS):
    """
    Verifies if new_message flag is flagged
    :param mychat: chat handler object
    :return:
    """
    if mychat.new_message:
        bg_color = notify.new_notification_color()
        old_message = message.value
        message.value = mychat.message + old_message
        mychat.new_message = False
    else:
        bg_color = notify.new_color(message.bg)

    message.bg = bg_color


def connection_button(mychat: ChatHandlerWS):
    if mychat.is_connected():
        mychat.ws_disconnect()
        btn_connect.text = 'Connect'
        message.value = "Disconnected from server"
    else:
        mychat.ws_connect()
        btn_connect.text = 'Disconnect'
        message.value = "Connection established to server"


def closing(mychat: ChatHandlerWS):
    if mychat.is_connected():
        mychat.ws_disconnect()
    del mychat


if __name__ == '__main__':
    app = App("Chat Companion :)", width=800, height=480, bg=base_color, layout="auto")
    button_box = Box(app, width="fill", height=40, align="bottom")
    message_box = Box(app, border=4, height="fill", width="fill")
    message_box.bg = (255, 255, 255)
    message = TextBox(message_box, multiline=True, width="fill", height=350, visible=True)
    message.text_size = 16
    chat = ChatHandlerWS()

    btn_connect = PushButton(button_box, text="Connect", align="left", command=connection_button, args=[chat],
                             width=20, height=30, visible=True, padx=2, pady=2)
    btn_connect.text_size = 18
    btn_connect.bg = "white"
    btn_connect.show()
    notify = Notifications()
    message_box.repeat(Notifications.CHECK_LOOP_MS, verify_chat, [chat])
    app.display()
    closing(chat)
