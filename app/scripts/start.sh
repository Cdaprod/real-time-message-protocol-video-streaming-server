#!/bin/bash

# Mount NAS
/usr/local/bin/mount_nas.sh

# Start Nginx
/usr/local/nginx/sbin/nginx

# Start Flask Backend
cd /app && python app.py