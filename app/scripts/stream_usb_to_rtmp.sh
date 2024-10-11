#!/bin/bash

# Configuration
VIDEO_DEVICE="/dev/video0"          # Adjust based on your setup
AUDIO_DEVICE="hw:1,0"               # Adjust based on your setup
RTMP_SERVER="rtmp://localhost/live/stream_key"  # Update stream_key as needed

# Start streaming with FFmpeg
ffmpeg -f v4l2 -i "$VIDEO_DEVICE" \
       -f alsa -i "$AUDIO_DEVICE" \
       -c:v libx264 -preset veryfast -maxrate 2000k -bufsize 4000k \
       -pix_fmt yuv420p -g 50 \
       -c:a aac -b:a 128k -ar 44100 \
       -f flv "$RTMP_SERVER"