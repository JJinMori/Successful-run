# Script Reaction Runner

A small Python tool that runs your scripts and reacts to the result. If the script finishes without errors, it plays a **success** video and sound. If it crashes, raises an error, or times out, it plays a different **failure** video and sound.

A file watcher can trigger this automatically every time you save a `.py` file in your project folder.

## Features

- Runs any Python script and checks its exit code
- Separate videos for success and failure
- Optional audio (`.mp3`, `.wav`, `.ogg`); without audio files it simply plays the video
- Auto-run on save with a file watcher
- Media is preloaded for a fast start
- Helper script to extract audio from your videos
- Close the video window with `Esc`, `q`, or the window's close button

## Requirements

- Windows
- Python 3.10 or newer (tested on 3.14)
- Packages listed in `requirements.txt`: `opencv-python`, `pygame-ce`, `watchdog`, `imageio-ffmpeg`

## Installation

```
git clone <your-repo-url>
cd <your-repo-folder>
py -m pip install -r requirements.txt
```

> Note: use `pygame-ce` instead of `pygame`. The original `pygame` has no prebuilt package for the newest Python versions and fails to build.

## Project structure

```
project/
├── runner.py            # runs one script and plays the result
├── watcher.py           # re-runs scripts automatically when you save them
├── audio_uit_video.py   # extracts mp3 audio from the videos
├── requirements.txt
└── media/
    ├── succes.mp4       # required: played on success
    ├── fout.mp4         # required: played on failure
    ├── succes.mp3       # optional
    └── fout.mp3         # optional
```

The media files are not included. Add your own short clips to the `media/` folder using exactly these names.

## Usage

Run a single script:

```
py runner.py my_script.py
```

Watch the folder and run scripts whenever you save them (keep this terminal open):

```
py watcher.py
```

Extract the audio from your videos into mp3 files (only needed once):

```
py audio_uit_video.py
```

## How it works

1. The target script is started in a separate process.
2. The exit code decides the result: `0` means success, anything else (or a timeout) means failure.
3. The matching sound and video are played.

## Settings

At the top of `runner.py`:

| Setting          | Default | Meaning                                     |
|------------------|---------|---------------------------------------------|
| `SCRIPT_TIMEOUT` | `30`    | Seconds before a script is counted as failed |
| `MAX_SECONDEN`   | `10`    | Maximum length of the video playback         |

At the top of `watcher.py`, `NEGEER` lists files that are never run, and `WACHT_TUSSEN_RUNS` sets the pause between runs.

## Troubleshooting

- **No music plays:** the `.mp3` file is missing from `media/`. This is allowed, the video still plays. Run `audio_uit_video.py` to extract the audio from your videos.
- **No video plays:** check that `media/succes.mp4` and `media/fout.mp4` exist and have exactly these names. Windows hides file extensions by default, so check for names like `succes.mp4.mp4`.
- **`pygame` fails to install:** install `pygame-ce` instead.
- **Script hangs and counts as failed:** scripts that wait for `input()` never finish and hit the timeout.

## Warning

The watcher really executes every `.py` file you save in the folder. Do not put scripts there that delete files or do anything else you would not want to run automatically.

## Media and copyright

Do not publish videos or music you do not have the rights to. Keep your own clips local, for example by adding `media/` to `.gitignore`.

## License

MIT
