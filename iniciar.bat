@echo off
title PetShop - Sistema de Gestion
cd /d "%~dp0"
set PYTHONPATH=%~dp0
echo Iniciando PetShop...
python\python.exe app.py
pause
