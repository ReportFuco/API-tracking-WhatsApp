@echo off
echo Starting FastAPI and ngrok...

cd /d %~dp0

REM FastAPI
start "FastAPI" cmd /k "call env\Scripts\activate && python -m app.main"

REM ngrok
start "ngrok" cmd /k "ngrok http 8000"

echo Everything started.

code "C:\Users\Francisco Arancibia\Documents\proyectos\proyectos python\API tracking habitos"