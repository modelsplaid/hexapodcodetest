from onvif import ONVIFCamera
import time
#onvif-cli --user 'admin' --password 'password' --host '192.168.1.168' --port 8899 -w /home/pi/HexaClean/python-onvif-zeep/wsdl
#onvif-cli devicemgmt GetHostname --user 'admin' --password 'admin' --host '192.168.1.168' --port 8899 -w /home/pi/HexaClean/python-onvif-zeep/wsdl
#mycam = ONVIFCamera(host='192.168.1.168', port=8899, user='admin', passwd='', wsdl_dir='/home/pi/HexaClean/python-onvif-zeep/wsdl/')
#mycam = ONVIFCamera(host='192.168.1.14', port=8899, user='admin', passwd='admin', wsdl_dir='/home/pi/HexaClean/python-onvif-zeep/wsdl/')

mycam = ONVIFCamera(host='192.168.1.8', port=8899, user='admin', passwd='admin')
#onvif-cli devicemgmt GetHostname --user 'admin' --password '' --host '192.168.1.168' --port 8899
print("get host name")
# Get Hostname
time.sleep(1)
resp = mycam.devicemgmt.GetHostname()
print ('My camera`s hostname: ' + str(resp.Name))
time.sleep(1)
# Get system date and time
dt = mycam.devicemgmt.GetSystemDateAndTime()
tz = dt.TimeZone
year = dt.UTCDateTime.Date.Year
hour = dt.UTCDateTime.Time.Hour

print(dt,tz,year,hour)
