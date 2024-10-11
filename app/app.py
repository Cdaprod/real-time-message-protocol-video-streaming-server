import os
import subprocess
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Directory where videos are stored on the NAS
VIDEO_DIR = '/mnt/nas/videos'

# Route to list all available video files in the NAS
@app.route('/list-videos', methods=['GET'])
def list_videos():
    try:
        videos = [f for f in os.listdir(VIDEO_DIR) if f.endswith('.mp4') or f.endswith('.flv')]
        return jsonify(videos)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to serve a specific video file from the NAS
@app.route('/videos/<path:filename>', methods=['GET'])
def serve_video(filename):
    try:
        return send_from_directory(VIDEO_DIR, filename)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to start the FFmpeg streaming process
@app.route('/start-stream', methods=['GET'])
def start_stream():
    try:
        # Start the FFmpeg streaming command for video and audio
        command = ("ffmpeg -f v4l2 -i /dev/video0 -f alsa -i hw:1 "
                   "-c:v libx264 -preset veryfast -maxrate 2000k -bufsize 4000k "
                   "-pix_fmt yuv420p -g 50 -c:a aac -b:a 128k -ar 44100 "
                   "-f flv rtmp://localhost/live/stream_key")
        subprocess.Popen(command, shell=True)
        return jsonify({"status": "stream started"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to stop the FFmpeg streaming process
@app.route('/stop-stream', methods=['GET'])
def stop_stream():
    try:
        # Stop the FFmpeg process by killing it
        subprocess.Popen("pkill -f ffmpeg", shell=True)
        return jsonify({"status": "stream stopped"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to archive the stream (Placeholder - customize as needed)
@app.route('/archive-stream', methods=['GET'])
def archive_stream():
    try:
        # Placeholder for archiving logic (move files, trigger recording)
        return jsonify({"status": "stream archived"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)