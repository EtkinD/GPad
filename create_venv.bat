@echo off

start cmd /C "python -m venv venv && venv\Scripts\activate && python -m pip install --upgrade pip && python -m pip install inputs mouse keyboard"
