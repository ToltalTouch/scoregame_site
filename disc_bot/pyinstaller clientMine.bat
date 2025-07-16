@echo off
pyinstaller --onedir ^
--add-data "C:\minescore_project\disc_bot\minefiles\server.jar;." ^
--add-data "C:\minescore_project\disc_bot\minefiles\TLauncher-Installer-1.8.5.exe;." ^
client_mine.py
pause


