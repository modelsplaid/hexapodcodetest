import subprocess

def capture_rtsp_to_mp4(rtsp_url, output_file, duration=None):
    """
    Capture an RTSP stream and save it as an MP4 file.
    
    :param rtsp_url: The RTSP URL of the video stream.
    :param output_file: The output file path (e.g., "output.mp4").
    :param duration: Optional duration in seconds to capture (e.g., 10 for 10 seconds).
    """
    command = [
        'ffmpeg',
        '-t','5',
        '-i', rtsp_url,  # Input RTSP URL
        '-q:v', '2',
        '-rtsp_transport', 'udp',
        '-c:v', 'libx264',  # Video codec
        '-preset', 'veryfast',  # Encoding preset
        '-maxrate', '3000k',  # Maximum bitrate
        '-bufsize', '6000k',  # Buffer size
        '-pix_fmt', 'yuv420p',  # Pixel format
        '-g', '50',  # Keyframe interval
        '-c:a', 'aac',  # Audio codec
        '-b:a', '128k',  # Audio bitrate
        '-ac', '2',  # Audio channels
        '-ar', '44100',  # Audio sample rate
        '-movflags', '+faststart',  # Optimize for web playback
        output_file  # Output file
    ]
    
    # if duration:
    #     command.insert(2, '-t')
    #     command.insert(3, str(duration))
    
    try:
        # Run the ffmpeg command
        subprocess.run(command, check=True)
        print(f"Video saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error: Could not capture video from RTSP stream. {e}")

# Example usage
#rtsp_url = "rtsp://admin:admin@192.168.1.8:554/11"
#rtsp_url = "rtsp://admin:admin@192.168.1.14:554/11"
rtsp_url = "rtsp://admin:@192.168.1.168:554/11"
output_file = "output.mp4"
duration = 10  # Optional: Capture for 10 seconds

capture_rtsp_to_mp4(rtsp_url, output_file, duration)
