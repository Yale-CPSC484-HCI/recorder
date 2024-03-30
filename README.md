# HCI Recording and Local Playback Tool

This project can record data from the HCI Display

## Setup

If you don't have them, install [pyenv](https://github.com/pyenv/pyenv#basic-github-checkout) and [pipenv](https://pypi.org/project/pipenv/).

Create the virtual environment and install dependencies with: `pipenv install` inside the project directory.

## Play the sample data

There is a small amount of sample data in `data/sample`. You can play it back with:

```
pipenv run python src/main.py --data-path data/sample --mode play
```

## Record Your Own Data

Record to `data/sample1`, replacing `[Server_Name]` with the name of the HCI Display server found in this list: [https://cpsc484-584-hci.gitlab.io/s24/display_tutorial/#server-names](https://cpsc484-584-hci.gitlab.io/s24/display_tutorial/)

```
pipenv run python src/main.py --websocket-server [Server_Name]:8888 --data-path data/sample1 --mode record
```

For example, to record data from Display 1, in AKW: 
```
pipenv run python src/main.py --websocket-server cpsc484-01.stdusr.yale.internal:8888 --data-path data/sample1 --mode record
```

## Playback Your Data

Playback the data in `data/sample1`

```
pipenv run python src/main.py --data-path data/sample1 --mode play
```

## Data Preview

You can preview the data during recording or playback by opening your local browser to [http://127.0.0.1:4444](http://127.0.0.1:4444).

> Note: the IP address `127.0.0.1` refers to your local computer.

## Consuming Locally Recorded Data

Start this project in playback mode.

In your app, connect to (1) `ws://127.0.0.1:4444/twod` for the depth image with pose information; (2) `ws://127.0.0.1:4444/frames` for the spatial data frames; and (3) `ws://127.0.0.1:4444/sp2tx` for the speech to text data.

## Setup on the Zoo

To setup this project on the Zoo, please refer to the [Zoo setup readme](./docs/zoo_setup.md).
