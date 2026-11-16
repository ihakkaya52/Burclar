#!/usr/bin/env bash
# Gerekli paketleri ve fontları kurar (Debian/Ubuntu).
set -e
cd "$(dirname "$0")"
sudo apt-get install -y ffmpeg fonts-dejavu-core fonts-noto-color-emoji || true
pip install -r requirements.txt
mkdir -p motor/fonts
curl -sSL -o motor/fonts/Anton-Regular.ttf "https://raw.githubusercontent.com/google/fonts/main/ofl/anton/Anton-Regular.ttf"
curl -sSL -o motor/fonts/Montserrat-VF.ttf "https://raw.githubusercontent.com/google/fonts/main/ofl/montserrat/Montserrat%5Bwght%5D.ttf"
echo "Kurulum tamam."
