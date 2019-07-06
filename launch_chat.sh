#!/bin/bash
# launcher_chat.sh
# launch the chat notification app after setting display and source venv
export DISPLAY=:0.0
source /home/pi/chatnotification/venv/bin/activate
python3 main_app.py
