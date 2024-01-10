import pysrt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy import interpolate
import numpy as np

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

# Create a series of points for interpolation
x = np.linspace(0, len(lat), len(lat))

# Create a cubic spline interpolation function for latitude and longitude
spl_lat = interpolate.splrep(x, lat, s=0)
spl_lon = interpolate.splrep(x, lon, s=0)

# Create a smooth series of x values
x_smooth = np.linspace(0, len(lat), 500)  # 500 is the number of points for smoothness

# Get the smooth latitude and longitude values
lat_smooth = interpolate.splev(x_smooth, spl_lat)
lon_smooth = interpolate.splev(x_smooth, spl_lon)

if make_3d_visualization:
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(lat_smooth, lon_smooth, alt, marker='.', markersize=2)
    # Highlight the starting point in red
    ax.scatter(lat_smooth[0], lon_smooth[0], alt[0], color='red')
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Longitude')
    ax.set_zlabel('Altitude (m)')
else:
    plt.plot(lat_smooth, lon_smooth, marker='.', markersize=2)
    plt.scatter(lat_smooth[0], lon_smooth[0], color='red')  # Highlight the starting point in red
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')

plt.show()
