@echo off
cd /d "%~dp0"
echo Iniciando o Agente Narrativo com Etica Emergente...
call venv\Scripts\activate.bat
python main.py
pause

