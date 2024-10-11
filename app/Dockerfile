# Stage 1: Build Nginx with RTMP module
FROM nginx:alpine AS nginx-builder

# Install dependencies for building Nginx and RTMP module
RUN apk add --no-cache --virtual .build-deps \
    build-base \
    openssl-dev \
    pcre-dev \
    zlib-dev \
    libxslt-dev \
    gd-dev \
    geoip-dev \
    linux-headers \
    curl \
    git

# Clone the nginx-rtmp-module repository
RUN git clone https://github.com/arut/nginx-rtmp-module.git /tmp/nginx-rtmp-module

# Configure and build Nginx with the RTMP module
RUN cd /tmp/nginx-rtmp-module && \
    wget http://nginx.org/download/nginx-1.19.3.tar.gz && \
    tar zxvf nginx-1.19.3.tar.gz && \
    cd nginx-1.19.3 && \
    ./configure --with-http_ssl_module --add-module=../nginx-rtmp-module && \
    make && \
    make install

# Stage 2: Set up Flask backend
FROM python:3.9-slim AS flask-backend

# Set environment variables for Flask
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install Python dependencies
COPY backend/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code
COPY app/backend /app

# Expose the Flask port
EXPOSE 5000

# Start the Flask application
CMD ["python", "app.py"]

# Stage 3: Build the final image with FFmpeg and Nginx
FROM alpine:latest AS final

# Install necessary packages: Nginx, FFmpeg, and other tools
RUN apk add --no-cache \
    nginx \
    ffmpeg \
    bash \
    libc6-compat \
    ca-certificates \
    openssl \
    curl \
    python3 \
    py3-pip \
    cifs-utils  # For mounting NAS via SMB/CIFS

# Copy the compiled Nginx and the RTMP module from Stage 1
COPY --from=nginx-builder /usr/local/nginx /usr/local/nginx

# Copy the Flask backend from Stage 2
COPY --from=flask-backend /app /app

# Install Python dependencies in the final image
COPY app/backend/requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy the FFmpeg script for streaming
COPY app/scripts/stream_usb_to_rtmp.sh /usr/local/bin/stream_usb_to_rtmp.sh
RUN chmod +x /usr/local/bin/stream_usb_to_rtmp.sh

# Create necessary directories for Nginx and video storage
RUN mkdir -p /var/www/html /mnt/videos /mnt/hls /run/nginx

# NAS mount for persistent storage
RUN mkdir -p /mnt/nas/videos /mnt/nas/hls

# Expose RTMP and HTTP ports
EXPOSE 1935 80 5000

# Mount NAS (Update with correct NAS IP and credentials)
COPY app/scripts/mount_nas.sh /usr/local/bin/mount_nas.sh
RUN chmod +x /usr/local/bin/mount_nas.sh

# Start both Nginx and Flask via a bash script
COPY app/scripts/start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh

# Start Nginx, Flask, and mount NAS
CMD ["/usr/local/bin/start.sh"]