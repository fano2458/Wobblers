import cv2
import datetime

# Open the video
cap = cv2.VideoCapture('source_files/DJI_0076.mp4')

# Check if video opened successfully
if not cap.isOpened(): 
    print("Error opening video file")

# Read until video is completed
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    # Resize and display the frame
    frame = cv2.resize(frame, (800, 600))
    cv2.imshow('Video', frame)
    
    # Get the timestamp of the current frame in milliseconds
    timestamp_ms = cap.get(cv2.CAP_PROP_POS_MSEC)
    # Convert the timestamp to seconds and format it as 00:00:00,000
    timestamp_s = datetime.timedelta(milliseconds=timestamp_ms)
    formatted_timestamp = str(timestamp_s)[:-3]  # Remove the last three characters to get the format 00:00:00,000
    print('Timestamp: ', formatted_timestamp)
    
    
    # Press Q on keyboard to exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()
