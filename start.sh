#!/bin/bash
discord_executable=$0

if [ $discord_executable == "" ]; then
   discord_executable=discord
fi

echo "discordthemeldr"
this_path=$(dirname $(realpath $0))
cd "$this_path"
echo "Starting Discord"
$discord_executable proxy-server="127.0.0.1:8080" &
pid=$!

echo "Starting Proxy"
mitmdump -s discord-proxy.py -p 8080 &
mpid=$!

echo "MPID: $mpid"

while ps -p $pid &>/dev/null; do
   # do nothing but block execution until discord is closed
   sleep 1
done

echo "Discord is no longer running"
kill -s SIGKILL $mpid
