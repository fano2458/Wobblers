import pysrt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


make_3d_visualization = False
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

if make_3d_visualization:
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(lat, lon, alt, marker='.', s=2)
    # Highlight the starting point in red
    ax.scatter(lat[0], lon[0], alt[0], color='red')
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Longitude')
    ax.set_zlabel('Altitude (m)')
else:
    plt.scatter(lat, lon, marker='.', s=2)
    plt.scatter(lat[0], lon[0], color='red')  # Highlight the starting point in red
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')

plt.show()
