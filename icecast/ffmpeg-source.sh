#!/bin/bash
echo "Aguardando Icecast iniciar..."
sleep 5

ffmpeg -re -stream_loop -1 -i /audio.mp3 \
  -vn -c:a libmp3lame -b:a 128k -content_type audio/mpeg \
  -f mp3 "icecast://source:hackme@icecast:8000/test.mp3"
