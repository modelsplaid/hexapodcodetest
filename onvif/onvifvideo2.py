from onvif import ONVIFCamera
import subprocess
from flask import Flask, Response
import io
import threading

app = Flask(__name__)

def get_rtsp_url(ip, port, username, password):
    cam = ONVIFCamera(ip, port, username, password,wsdl_dir='/home/pi/HexaClean/python-onvif-zeep/wsdl/')
    media_service = cam.create_media_service()
    profiles = media_service.GetProfiles()
    return media_service.GetStreamUri({
        'StreamSetup': {'Stream': 'RTP-Unicast', 'Transport': 'RTSP'},
        'ProfileToken': profiles[0].token
    }).Uri.replace("rtsp://", f"rtsp://{username}:{password}@")

def generate_mjpeg():
    # Improved FFmpeg command for real-time streaming
    ffmpeg_cmd = [
        'ffmpeg',
        '-rtsp_transport', 'tcp',    # Force TCP transport
        '-i', rtsp_url,              # Input RTSP URL
        '-fflags', 'nobuffer',       # Reduce latency
        '-flags', 'low_delay',
        '-c:v', 'mjpeg',             # Force MJPEG codec
        '-q:v', '3',                 # Quality level
        '-f', 'mjpeg',               # Output format
        '-update', '1',              # Single frame update
        'pipe:1'                     # Output to stdout
    ]

    process = subprocess.Popen(
        ffmpeg_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=0
    )

    # Read FFmpeg output in a stream
    while True:
        # Read JPEG frame header
        header = process.stdout.read(4)
        if not header:
            break
            
        # Verify JPEG start marker
        if header != b'\xff\xd8\xff\xe0':
            continue
            
        # Read until JPEG end marker
        jpeg_data = header
        while True:
            chunk = process.stdout.read(4096)
            if not chunk:
                break
            jpeg_data += chunk
            if jpeg_data[-2:] == b'\xff\xd9':
                break
                
        # Yield complete frame
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' +
               jpeg_data + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(
        generate_mjpeg(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@app.route('/')
def index():
    return """
    <html>
    <head><title>Camera Stream</title></head>
    <body>
        <img src="/video_feed" width="1280" height="720">
        <script>
            // Auto-reload on connection failure
            let img = document.querySelector('img');
            img.onerror = function() {
                console.log('Connection lost, reloading...');
                setTimeout(() => location.reload(), 1000);
            };
        </script>
    </body>
    </html>
    """

if __name__ == '__main__':
    # Camera configuration
    CAMERA_IP = '192.168.1.14'
    CAMERA_PORT = 8899
    USERNAME = 'admin'
    PASSWORD = 'admin'   
    
    # Get authenticated RTSP URL
    rtsp_url = get_rtsp_url(CAMERA_IP, CAMERA_PORT, USERNAME, PASSWORD)
    print(f"Using RTSP URL: {rtsp_url}")
    
    # Start Flask server
    app.run(host='0.0.0.0', port=5000, threaded=True)