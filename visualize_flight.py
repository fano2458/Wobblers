import cv2
import pysrt
import datetime
import re

# Open the video
cap = cv2.VideoCapture('source_files/DJI_0076.mp4')

# Load the data from an SRT file
subs = pysrt.open('source_files/DJI_0076.SRT')

# Extract the timestamps and coordinates from the SRT file


with open('source_files/DJI_0076.SRT', 'r') as file:
    content = file.read()

# # Используйте регулярное выражение для поиска временных меток
# timestamps = re.findall(r'\d{2}:\d{2}:\d{2},\d{3}', content)

# timestamps_in_msec = []
# for timestamp in timestamps:
#     hours, minutes, seconds_milliseconds = timestamp.split(':')
#     seconds, milliseconds = seconds_milliseconds.split(',')
#     total_milliseconds = int(hours) * 60 * 60 * 1000 + int(minutes) * 60 * 1000 + int(seconds) * 1000 + int(milliseconds)
#     timestamps_in_msec.append(total_milliseconds)

timestamps_srt = [str(sub.start) for sub in subs]  # Keep the timestamps in the format 0:00:00,000
lat = [float(sub.text.split('latitude: ')[1].split(' ')[0].replace(']', '')) for sub in subs]
lon = [float(sub.text.split('longitude: ')[1].split(' ')[0].replace(']', '')) for sub in subs]

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
    # Convert the timestamp to the format 0:00:00,000
    #formatted_timestamp_video = str(datetime.timedelta(milliseconds=timestamp_video)).replace('.', ',')[:-3]
    print(timestamp_video, timestamps_srt[i])
    # If the video timestamp matches the SRT timestamp, print the coordinates
    if i < len(timestamps_srt) and abs(float(timestamp_video) - float(timestamps_srt[i].replace(',', '.'))) <= 0.005:
        print('Timestamp: ', formatted_timestamp_video)
        print('Coordinates: ', lat[i], lon[i])
        i += 1  # Move to the next timestamp and coordinates
    # Press Q on keyboard to exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()
