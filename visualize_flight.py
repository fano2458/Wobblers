import cv2
import pysrt
import datetime
import re
import math


def calculate_bearing(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    y = math.sin(dlon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
    bearing = math.atan2(y, x)
    return math.degrees(bearing)


# Open the video
cap = cv2.VideoCapture('source_files/DJI_0076.mp4')

# Load the data from an SRT file
subs = pysrt.open('source_files/DJI_0076.SRT')

# Open the .srt file
with open('source_files/DJI_0076.srt', 'r') as file:
    srt_text = file.read()

# Extract the times
times = re.findall(r'(> \d{2}:\d{2}:\d{2},\d{3})', srt_text)    

# Convert to milliseconds
timestamps_srt = []
for time in times:
    time = time[2:]
    h, m, s_ms = time.split(':')
    s, ms = s_ms.split(',')
    total_ms = int(h) * 3600000 + int(m) * 60000 + int(s) * 1000 + int(ms)
    timestamps_srt.append(total_ms)
    
lat = [float(sub.text.split('latitude: ')[1].split(' ')[0].replace(']', '')) for sub in subs]
lon = [float(sub.text.split('longitude: ')[1].split(' ')[0].replace(']', '')) for sub in subs]

prev_lat, prev_lon = None, None

# Check if video opened successfully
if not cap.isOpened(): 
    print("Error opening video file")

# Read until video is completed
i = 0  # Index for the SRT timestamps and coordinates
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    # Resize and display the frame
    frame = cv2.resize(frame, (800, 600))
    cv2.imshow('Video', frame)
    
    # Get the timestamp of the current frame in milliseconds
    timestamp_video = cap.get(cv2.CAP_PROP_POS_MSEC)

    if i < len(timestamps_srt) and abs(float(timestamp_video) - float(timestamps_srt[i])) <= 2.5: # 2.5 msec difference is allowed
        print('Timestamp: ', timestamp_video)
        print('Coordinates: ', lat[i], lon[i])
        if prev_lat is not None and prev_lon is not None:
            print('Angle: ', calculate_bearing(prev_lat, prev_lon, lat[i], lon[i]))
        prev_lat = lat[i]
        prev_lon = lon[i]
        i += 1  # Move to the next timestamp and coordinates
    # Press Q on keyboard to exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()
