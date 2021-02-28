import matplotlib
from scipy.interpolate import griddata
import pymysql
import timeit
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

# Open authenticated database connection
start = timeit.default_timer()
db = pymysql.connect("localhost","root","parWONE123","plant_data_1920" )
cursor = db.cursor()

# SQL query to read information from database
sql = "SELECT * FROM irrigation_data"
water = []
color = []
heat = []
light = []

try:
   # Execute the SQL command
   cursor.execute(sql)

   # Fetch all the rows in a list of lists
   results = cursor.fetchall()
   for j in range(0,len(results)):
      water.append(results[j][2])
      color.append(results[j][3])
      heat.append(results[j][4])
      light.append(results[j][5])
except:
   print ("Error: unable to fetch data")

db.close()

# Set lists containing variable sets
x1 = np.linspace(min(water), max(water), len(np.unique(water))); 
y1 = np.linspace(min(color), max(color), len(np.unique(color)));
x2, y2 = np.meshgrid(x1, y1);

# Interpolate Z variable to new XY axis
z2 = griddata( (water, color), heat, (x2, y2), method='cubic', fill_value = 0);
z2[z2 < min(heat)] = min(heat);

# Interpolate C variable to new XY axis
c2 = griddata( (water, color), light, (x2, y2), method='cubic', fill_value = 0);
c2[c2 < min(light)] = min(light); 

# Set dimensions for plot
color_dimension = c2;
minn, maxx = color_dimension.min(), color_dimension.max();
norm = matplotlib.colors.Normalize(minn, maxx);
m = plt.cm.ScalarMappable(norm=norm);
m.set_array([]);
fcolors = m.to_rgba(color_dimension);

# Plot XYZC variables from 2D to 4D graph
fig = plt.figure(); ax = fig.gca(projection='3d');
surf = ax.plot_surface(x2, y2, z2, facecolors = fcolors, linewidth=0, rstride=1, cstride=1,
                       antialiased=False);
cbar = fig.colorbar(m, shrink=0.5, aspect=5);
cbar.ax.get_yaxis().labelpad = 15; cbar.ax.set_ylabel("Light", rotation = 270);

# Set axis labels and plot
ax.set_xlabel("Water"); ax.set_ylabel("Color");
ax.set_zlabel("Heat");
plt.title('');
plt.show();