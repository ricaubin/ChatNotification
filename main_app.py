from guizero import App, TextBox, Box, PushButton
from chatHandler import ChatHandler
from notifications import Notifications
import logging

logging.basicConfig(level=logging.INFO)
base_color = (0, 0, 160)
text_color = "white"
notification_cnt = 0


def verify_chat(mychat:ChatHandler):
    mychat.verify_text()
    if mychat.new_message:
        bg_color = notify.new_notification_color()
        message.set(mychat.message)

        mychat.new_message = False
    else:
        bg_color = notify.new_color(message.bg)

    message.bg = bg_color


def connection_button(mychat:ChatHandler):
    if mychat.is_connected():
        mychat.disconnect()
        btn_connect.text = 'Connect'
        message.set("Disconnected from server")
    else:
        mychat.connect()
        btn_connect.text = 'Disconnect'
        message.set("Connection established to server")


def closing(mychat:ChatHandler):
    del mychat


if __name__ == '__main__':
    app = App("Chat Notify!!!", width=800, height=480, bg=base_color, layout="auto")
    message_box = Box(app, border=4, height=350, width="fill")
    message_box.bg = (255, 255, 255)
    message = TextBox(message_box, multiline=True, width="fill", height=350, visible=True)
    message.text_size = 18
    chat = ChatHandler()
    btn_connect = PushButton(app, text="Connect", align="bottom", command=connection_button, args=[chat],
                             width=25, height=30, visible=True, padx=2, pady=2)
    btn_connect.text_size = 24

    btn_connect.bg = "white"
    btn_connect.show()
    notify = Notifications()
    message_box.repeat(Notifications.CHECK_LOOP_MS, verify_chat, [chat])
    app.display()
    app.on_close(closing(chat))
