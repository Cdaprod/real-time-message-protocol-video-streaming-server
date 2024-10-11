#!/bin/bash

# NAS details
NAS_IP="192.168.0.19"
NAS_SHARE_VIDEOS="videos"
NAS_SHARE_HLS="hls"
NAS_USER="your_username"
NAS_PASSWORD="your_password"

# Mount NAS directories
mount.cifs //$NAS_IP/$NAS_SHARE_VIDEOS /mnt/nas/videos -o username=$NAS_USER,password=$NAS_PASSWORD,iocharset=utf8,vers=3.0
mount.cifs //$NAS_IP/$NAS_SHARE_HLS /mnt/nas/hls -o username=$NAS_USER,password=$NAS_PASSWORD,iocharset=utf8,vers=3.0