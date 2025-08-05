@echo off
cd /d "%~dp0"
echo Iniciando o Agente Narrativo com Ética Emergente...
call venv\Scripts\activate.bat
python main.py
pause

