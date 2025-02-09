from onvif import ONVIFCamera
import requests
from urllib.parse import urlparse

def capture_onvif_snapshot(ip, port, username, password, save_path='snapshot.jpg'):
    # Create camera object
    camera = ONVIFCamera(ip, port, username, password,wsdl_dir='/home/pi/HexaClean/python-onvif-zeep/wsdl/')

    # Create media service
    media_service = camera.create_media_service()

    # Get profiles
    profiles = media_service.GetProfiles()
    
    if not profiles:
        raise Exception("No media profiles found")
    print("profiles: ",profiles)
    # Use first profile
    profile_token = profiles[0].token

    # Get snapshot URI
    snapshot_uri = media_service.GetSnapshotUri({'ProfileToken': profile_token})
    print(f"Snapshot URI: {snapshot_uri.Uri}")

    # Extract URL components
    url = urlparse(snapshot_uri.Uri)
    
    # Send HTTP GET request with authentication
    response = requests.get(
        snapshot_uri.Uri,
        auth=requests.auth.HTTPDigestAuth(username, password) if url.username is None 
        else requests.auth.HTTPBasicAuth(username, password),
        timeout=10
    )

    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Image saved to {save_path}")
    else:
        raise Exception(f"Failed to fetch snapshot. Status code: {response.status_code}")

# Usage example
if __name__ == "__main__":
    # Camera credentials
    # CAMERA_IP = '192.168.1.14'
    # CAMERA_PORT = 8899
    # USERNAME = 'admin'
    # PASSWORD = 'admin'
    CAMERA_IP = '192.168.1.168'
    CAMERA_PORT = 8899
    USERNAME = 'admin'
    PASSWORD = 'admin'    
    try:
        capture_onvif_snapshot(CAMERA_IP, CAMERA_PORT, USERNAME, PASSWORD)
    except Exception as e:
        print(f"Error: {str(e)}")
