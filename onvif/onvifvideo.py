from onvif import ONVIFCamera
import subprocess
from flask import Flask, Response
import threading
import time

app = Flask(__name__)

def get_rtsp_url(ip, port, username, password):
    # Connect to ONVIF camera
    cam = ONVIFCamera(ip, port, username, password,wsdl_dir='/home/pi/HexaClean/python-onvif-zeep/wsdl/')
    media_service = cam.create_media_service()
    profiles = media_service.GetProfiles()
    
    if not profiles:
        raise Exception("No media profiles found")
    
    # Get stream URI for first profile
    stream_uri = media_service.GetStreamUri({
        'StreamSetup': {'Stream': 'RTP-Unicast', 'Transport': 'RTSP'},
        'ProfileToken': profiles[0].token
    })
    
    # Add credentials to RTSP URL
    rtsp_url = stream_uri.Uri
    return rtsp_url.replace("rtsp://", f"rtsp://{username}:{password}@")

def generate_frames():
    # FFmpeg command to convert RTSP to MJPEG
    ffmpeg_cmd = [
        'ffmpeg',
        '-rtsp_transport', 'udp',  # Force TCP transport
        '-i', rtsp_url,
        '-q:v', '2',              # Quality setting
        '-f', 'mjpeg',
        '-update', '1',
        'pipe:1'
    ]
    
    process = subprocess.Popen(
        ffmpeg_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=0
    )
    
    try:
        while True:
            #time.sleep(0.3)
            frame = process.stdout.read(1024 * 1024)  # Read frame data
            if not frame:
                break
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    finally:
        process.terminate()
        process.wait()

@app.route('/video_feed')
def video_feed():
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@app.route('/')
def index():
    return """
    <html>
    <head>
        <title>ONVIF Camera Stream</title>
    </head>
    <body>
        <h1>Camera Live Stream</h1>
        <img src="/video_feed" style="max-width: 70%; height: auto;">
    </body>
    </html>
    """

if __name__ == '__main__':
    # Camera configuration
    CAMERA_IP = '192.168.1.14'
    CAMERA_PORT = 8899
    USERNAME = 'admin'
    PASSWORD = 'admin'
    
    # Get RTSP URL
    rtsp_url = get_rtsp_url(CAMERA_IP, CAMERA_PORT, USERNAME, PASSWORD)
    print(f"RTSP Stream URL: {rtsp_url}")
    
    # Start Flask server
    app.run(host='0.0.0.0', port=5760, threaded=True)
