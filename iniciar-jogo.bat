@echo off
title Game Of Pulos Launcher

echo ===================================
echo  Game Of Pulos
echo ===================================
echo.
echo Instalando dependencias (Pygame Zero)...
echo Por favor, aguarde.
echo.

python -m pip install pgzero

echo.
echo Dependencias instaladas.
echo Iniciando o jogo...
echo.

pgzrun game.py

echo.
echo Jogo finalizado.
pause
