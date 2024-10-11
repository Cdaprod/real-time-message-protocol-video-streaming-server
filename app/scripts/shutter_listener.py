import RPi.GPIO as GPIO
import subprocess
import time

# Pin setup
button_pin = 18  # Use the pin number where the button is connected
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Stream process placeholder
ffmpeg_process = None

def start_stream():
    global ffmpeg_process
    # Start FFmpeg stream command
    ffmpeg_process = subprocess.Popen([
        'ffmpeg', '-f', 'v4l2', '-i', '/dev/video0', '-f', 'alsa', '-i', 'hw:1',
        '-c:v', 'libx264', '-preset', 'veryfast', '-b:v', '3000k', '-maxrate', '3000k', 
        '-bufsize', '6000k', '-vf', 'format=yuv420p', '-g', '50', '-c:a', 'aac', 
        '-b:a', '128k', '-ar', '44100', '-f', 'flv', 'rtmp://<your-rtmp-server-ip>/live/stream'
    ])

def stop_stream():
    global ffmpeg_process
    if ffmpeg_process is not None:
        ffmpeg_process.terminate()  # Stop the stream
        ffmpeg_process = None

try:
    while True:
        # Detect button press
        button_state = GPIO.input(button_pin)
        if button_state == GPIO.LOW:  # Button is pressed
            if ffmpeg_process is None:
                print("Starting stream...")
                start_stream()
            else:
                print("Stopping stream...")
                stop_stream()
        time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()