#!/bin/bash
echo "discordthemeldr"
python -m pip install -r requirements.txt

echo "generating mitmproxy certificates"
mitmdump &
mpid=$!
sleep 5
kill $mpid

echo "Adding certificate - This might ask for your password"
sudo trust anchor ~/.mitmproxy/mitmproxy-ca.pem

echo "Done, you can start Discord using start.sh now"
