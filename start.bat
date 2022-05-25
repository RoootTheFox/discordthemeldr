@echo off
title discordthemeldr
start "discordthemeldr" cmd /c mitmdump -s discord-proxy.py
taskkill /F /IM Discord.exe
%LocalAppData%\Discord\Update.exe --processStart Discord.exe --process-start-args "--proxy-server=\"127.0.0.1:8080\""