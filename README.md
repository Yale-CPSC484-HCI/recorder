# HCI Recording and Local Playback Tool

This project can record data from the HCI Display

## Setup

If you don't have them, install [pyenv](https://github.com/pyenv/pyenv#basic-github-checkout) and [pipenv](https://pypi.org/project/pipenv/).

Create the virtual environment and install dependencies with: `pipenv install` inside the project directory.

## Record Data

Record to `data/sample1`

```
pipenv run python src/main.py --websocket-server 172.28.142.145:8888 --data-path data/sample1 --mode record
```

## Playback Data

Playback the data in `data/sample1`

```
pipenv run python src/main.py --data-path data/sample1 --mode playback
```
