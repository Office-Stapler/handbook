# handbook
A simple discord bot that takes in a course code (UNSW) and outputs information about that course.

## Development Setup

To start development, first clone the Git repository

```sh
git clone https://github.com/Office-Stapler/handbook.git
```

and then run

```sh
python3 -m venv venv
. venv/bin/activate
pip3 install -r requirements.txt
```

Remember to deactivate the `venv` later:

```sh
deactivate
```

## Usage Setup

To run the bot, simply fill in [config.json](https://github.com/Office-Stapler/handbook/blob/master/config.json)
with your Discord bot token and desired trigger prefix. Then run

```sh
python3 bot.py
```
