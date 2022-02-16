# GPad

Program that converts your gamepad to mouse, and adds some keyboard actions.

## IMPORTANT

### - 1

This program was not tested in any platform other than Windows 10
It may not work on older versions of windows.
Most probably macOS and Linux distributions will not support this program as well.

### - 2

Windows defender sees program as keylogger.
To avoid that, you need add program's root folder into "excluded folders" list.

How to do:
https://support.microsoft.com/en-us/windows/add-an-exclusion-to-windows-security-811816c0-4dfd-af4a-47e4-c301afe13b26

## Requirements

- python3 sdk (recommended newer than 3.5)
- pip3
- Also, virtual environment package should be installed in your python sdk.

To check virtual environment:
``` shell
python -m venv
```
Usage instructions should be printed on your terminal, otherwise type below command to install virtual environment.
``` shell
pip install virtualenv
```

## Installation

Execute "create_venv.bat" batch file. It will create virtual environment and install required python packages automatically.

## Executing The Program

### First way

- Open windows terminal
- Change directory to this folder by using ```cd``` command.
- Type ```venv\Scripts\activate```
- Finally, type ```python main.py``` to run.

### Second way

There is an example batch file named "example.bat"

- Create a new batch file wherever you want.
- Copy and paste everything inside "example.bat"
- Change file location with this folder location inside new batch file.
- Finally, if you double click your batch file, it will start program and opens a terminal. Do not close terminal. If you do that, program will be terminated.

## Default Actions

- left stick axes -> move cursor
- left stick press -> press / release mouse's middle button
- left trigger -> boosts cursor and scroll speeds

- right stick axes -> clicks arrow keys
- right stick press -> performs "altgr+tab" action
- right trigger -> -- no action --

- dpad y -> scroll up/down
- dpad x -> switch between desktops (win+ctrl+right_arrow ~ win+ctrl+left_arrow)

- A -> press / release left mouse button
- B -> press / release right mouse button
- X -> escape key
- Y -> capture screen (win+shift+s)

- LShoulder -> win+tab
- RShoulder -> enter

- select -> pause/resume program
- start -> exit controller

### Interrupt Mode

enable/disable combination: while right_trigger and left_trigger are fully pressed, press right stick for 1.5 seconds and release.

While interrupt mode is on, program does not perform any mouse or keyboard actions ("pause/resume" and "exit controller" do not work as well) until performing same action to disable interrupt mode.
