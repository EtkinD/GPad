@echo off

REM Change below to your own path.
set _GPADPATH="C:\Enter\Path\To\Your\Local\Gpad"

start cmd /C "cd %_GPADPATH% && venv\Scripts\activate && python main.py"
