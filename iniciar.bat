@echo off
title PetShop - Sistema de Gestion
cd /d "%~dp0sistema"
set PYTHONPATH=%~dp0sistema
echo Iniciando PetShop...
python\python.exe app.py
pause
