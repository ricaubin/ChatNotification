# Twitch Chat Notification

Twitch Chat Notification is a simple UI that displays 
the last Chat on a Twitch channel and notify visually of new messages
changing the background color and gradually returns to base color.

Basic window size is 800x480, the size of basic 5inch hdmi tactile screen
for Raspberry Pi 3.

## Getting Started

These instructions will get you a copy of the project up and
 running on your local machine for development.
  See deployment for notes on how to deploy the project on a live
   system.

### Prerequisites

Git to download this source.

Latest Python 3 installed.

In a any directory

### Installing

Download into your target folder by executing the git clone command.

```
>git clone https://github.com/ricaubin/ChatNotification.git
```

Prepare a virtual environment for the app. Execute in the project directory.

```
>python -m venv ./venv
```

Activate the virtual environment.

Windows
```
>venv/Scripts/activate
```

Linux
```
>source venv/bin/activate
```

Install required packages

````
(venv)>pip install -r requirements.txt
````

Once all installed prepare chat_config.json by filling your twitch bot infos
````
{
  "token": "oauth:<Your Key here>",
  "user" : "YourBotUser",
  "channel" : "YourTwitchChannel"
}
````

token can be obtained at twitch here: [Twitch apps token generator](https://twitchapps.com/tmi/)
Personally I created an account just for this app and chatbot apps.

Now run the main_app.py

```
(venv)> python main_app.py
```

If everything went well you should see a simple window with a textbox
and a Connect button. Press connect to monitor desired twitch channel
configured.

## Auto start with Linux daemon

This project main target is to run on a Raspberry Pi 3 and I've included
a systemd service file to start application through a script.

### steps
Install application in /home/pi/chatnotification and setup its virtualenv

Install chat_notification.service

Enable service

Start chat_notification.service

If all goes well application should start.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Richard Aubin** - *Initial work* - [Ricaubin](https://github.com/ricaubin)

See also the list of [contributors](https://github.com/ricaubin/ChatNotification/contributors) who participated in this project.

## License

See the [LICENSE.md](LICENSE.md) file for details
