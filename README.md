# Crokket
_- The "I didn't come here to be a stenographer" ASR AI, powered by pretrained models from OpenAI_

## Requirements
- Windows
- Python 3.11 (`winget install Python.Python.3.11`)
- Venv (Should be included with the Python install, otherwise: `pip install venv`)
- Cuda-enabled graphics card (Only necessary if you want it to be.. not slow.)
- Cuda toolkit (`winget install Nvidia.CUDA`)

### Updates
If there has been an update, there's a possibility that some dependencies changed, if you're unsure you can run `conda env update` to update any dependency changes that has been made.

## Installation
There are a couple of steps, but it should be a fairly quick job.
This guide assumes you are at the root of the repository when running commands.

### Install Python and CUDA Toolkit
- `winget install Python.Python.3.11`
- `winget install Nvidia.CUDA`

### Create and activate your virtual environment
- `python -m venv .venv`
- `.venv/Scripts/activate`

### Install the PIP requirements
- `python -m pip install -r requirements.txt`

## Getting started
We suggest using the terminal inside Visual Studio Code, but if you have a preferred way of command-line usage - go right ahead.

Take your audio file, (only .wav files are supported as of right now), and place it somewhere you can easily copy or remember the file path.

To transcribe the audio, use `python main.py path/to/file.wav`. This runs Crokket in direct invokation mode, skipping the interactive part and performing slightly better in terms of speed. (Be sure to use paths that `look/something/like/this.wav` and `not\like\this.wav`, there's no support for backslash paths yet)
If you would prefer to use the graphical interface, just run `python main.py` and press enter on the message about using the GUI.
The transcript with the same name as your audio file can be found under the data folder in this directory. 

NOTE: If it is the first time you launch the program, it will download around 3 GB (assuming you're using the default `medium` model).

A somewhat modern consumer computer with a 30-series or newer graphics card is expected to transcribe in the ranges of 4-6 hours of audio per hour of runtime. The output is of course not perfect but it should save you some time.

**ALWAYS CHECK YOUR OUTPUT AND MAKE THE NECESSARY CORRECTIONS**

Best of luck.
