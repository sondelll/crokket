# Crokket Secure
_- The "I didn't come here to be a stenographer" ASR AI, powered by pretrained models from OpenAI_

## Requirements
- [Anaconda](https://www.anaconda.com/)
- Cuda-enabled graphics card (Only necessary if you want it to be.. not slow.)

## Getting started
This assumes Anaconda (conda for short) has been installed.
We suggest using the terminal inside Visual Studio Code, but if you have a preferred way of command-line usage - go right ahead.

Make sure you are in the crokket directory that you cloned/downloaded, and use `conda env create` to have Anaconda create the Python environment with all the dependencies for you. You can of course set up the environment manually, but it's not recommended.

(conda can be a bit finnicky at times, a workaround for this kind of issue is to use Anaconda Navigator to launch a shell using the `crokket` environment and using that instead of the built-in one in VSCode)

Take your audio file, (only .wav files are supported as of right now), and place it somewhere you can easily copy or remember the file path.

To transcribe the audio, use `python main.py path/to/file.wav`. The transcript with the same name as your audio file can be found under the data folder in this directory. 

NOTE: If it is the first time you launch the program, it will download around 3 GB (assuming you're using the default `medium` model).

A somewhat modern consumer computer with a 30-series or newer graphics card is expected to transcribe in the ranges of 4-6 hours of audio per hour of runtime. The output is of course not perfect but it should save you some time.

Best of luck.