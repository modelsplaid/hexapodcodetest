#fmpeg -i  rtsp://admin:admin@192.168.1.8:554/11 -vframes  1 a.jpg

import subprocess

def capture_frame_from_rtsp(rtsp_url, output_file):
    # Command to capture a single frame from the RTSP stream
    command = [
        'ffmpeg',
        '-i', rtsp_url,  # Input RTSP URL
        '-vframes', '1',  # Capture only one frame
        output_file  # Output file
    ]
    
    try:
        # Run the ffmpeg command
        subprocess.run(command, check=True)
        print("Frame saved to", output_file)
    except subprocess.CalledProcessError as e:
        print(e)
        #print(f"Error: Could not capture frame from RTSP stream. {e}")

# Example usage
rtsp_url = "rtsp://admin:admin@192.168.1.8:554/11"
output_file = "captured_frame.jpg"

capture_frame_from_rtsp(rtsp_url, output_file)


# import cv2

# def capture_frame_from_rtsp(rtsp_url, output_file):
#     # Create a VideoCapture object with the RTSP URL
#     print(000)
#     cap = cv2.VideoCapture(rtsp_url)
#     print(111)
#     if not cap.isOpened():
#         print("Error: Could not open RTSP stream.")
#         return
#     print(222)
#     # Read one frame from the stream
#     ret, frame = cap.read()
#     print(333)
#     if ret:
#         # Save the frame to a file
#         cv2.imwrite(output_file, frame)
#         print(f"Frame saved to {output_file}")
#     else:
#         print("Error: Could not read frame from RTSP stream.")
    
#     # Release the VideoCapture object
#     cap.release()

# # Example usage
# rtsp_url = "rtsp://admin:admin@192.168.1.8:554/11"
# output_file = "captured_frame.jpg"

# capture_frame_from_rtsp(rtsp_url, output_file)
