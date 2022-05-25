@echo off
title Discord Theme Loader
echo Loading Discord Theme loader
pip install pipx
python -m pipx ensurepip
python -m pipx install mitmproxy
python -m pipx runpip mitmproxy install -r requirements.txt

echo generating certificates
start cmd /c "mitmdump.exe"
timeout /T 5 /NOBREAK
taskkill /F /IM mitmdump.exe

echo ADDING CERTIFICATE - This requires admin privileges
powershell -Command "Start-Process -Verb RunAs certutil '-addstore root %USERPROFILE%\.mitmproxy\mitmproxy-ca-cert.cer'"
certutil -addstore root %USERPROFILE%\.mitmproxy\mitmproxy-ca-cert.cer

echo done, you can run start.bat now
pause