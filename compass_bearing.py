import pysrt
import matplotlib.pyplot as plt
import numpy as np

threshold_height = 27

# Load the data from an SRT file
subs = pysrt.open('source_files/DJI_0076.SRT')

# Extract the latitude, longitude, and altitude data
lat = [float(sub.text.split('latitude: ')[1].split(' ')[0].replace(']', '')) for sub in subs]
lon = [float(sub.text.split('longitude: ')[1].split(' ')[0].replace(']', '')) for sub in subs]
alt = [float(sub.text.split('rel_alt: ')[1].split(' ')[0].replace(']', '')) for sub in subs]

lat = [lat[i] for i in range(len(alt)) if alt[i] < threshold_height]
lon = [lon[i] for i in range(len(alt)) if alt[i] < threshold_height]
alt = [alt[i] for i in range(len(alt)) if alt[i] < threshold_height]

plt.scatter(lat, lon, marker='.', s=2)
plt.scatter(lat[0], lon[0], color='red')  # Highlight the starting point in red
plt.xlabel('Latitude')
plt.ylabel('Longitude')

# Calculate the difference in longitude
lon_diff = np.radians(lon[1:] - np.array(lon[:-1]))

# Convert latitude to radians
lat1 = np.radians(lat[:-1])
lat2 = np.radians(lat[1:])

# Calculate the bearing
x = np.sin(lon_diff) * np.cos(lat2)
y = np.cos(lat1) * np.sin(lat2) - (np.sin(lat1) * np.cos(lat2) * np.cos(lon_diff))
initial_bearing = np.arctan2(x, y)

# Normalize the initial bearing to a compass bearing (between 0 and 360 degrees)
compass_bearing = (np.degrees(initial_bearing) + 360) % 360

print([compass_bearing[i] for i in range(0, 100)])

plt.show()
