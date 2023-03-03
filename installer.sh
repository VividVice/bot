#!/bin/bash

sudo apt update
sudo apt upgrade
sudo apt install ffmpeg
python3 -m pip install --force-reinstall https://github.com/yt-dlp/yt-dlp/archive/master.tar.gz
pip install discord.py
pip install ffmpeg-python
pip install asyncio
pip install PyNaCl
pip install pynacl
pip install requests