import matplotlib
from scipy.interpolate import griddata
import pymysql
import timeit
import numpy as np
import matplotlib.pyplot as plt  # To visualize
import pandas as pd  # To read data
import math
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter


# Open database connection
start = timeit.default_timer()
db = pymysql.connect("localhost","root","parWONE123","plant_data_1920" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to INSERT a record into the database.
sql = "SELECT * FROM irrigation_data"
water = []
color = []
heat = []
light = []
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Fetch all the rows in a list of lists.
   results = cursor.fetchall()
   for j in range(0,len(results)):
      water.append(results[j][2])
      color.append(results[j][3])
      heat.append(results[j][4])
      light.append(results[j][5])
except:
   print ("Error: unable to fetch data")

# disconnect from server
db.close()
x1 = np.linspace(min(water), max(water), len(np.unique(water))); 
y1 = np.linspace(min(color), max(color), len(np.unique(color)));
x2, y2 = np.meshgrid(x1, y1);

# Interpolation of Z: old X-Y to the new X-Y grid.
# Note: Sometimes values ​​can be < z.min and so it may be better to set 
# the values too low to the true minimum value.
z2 = griddata( (water, color), heat, (x2, y2), method='cubic', fill_value = 0);
z2[z2 < min(heat)] = min(heat);

# Interpolation of C: old X-Y on the new X-Y grid (as we did for Z)
# The only problem is the fact that the interpolation of C does not take
# into account Z and that, consequently, the representation is less 
# valid compared to the previous solutions.
c2 = griddata( (water, color), light, (x2, y2), method='cubic', fill_value = 0);
c2[c2 < min(light)] = min(light); 

#--------
color_dimension = c2; # It must be in 2D - as for "X, Y, Z".
minn, maxx = color_dimension.min(), color_dimension.max();
norm = matplotlib.colors.Normalize(minn, maxx);
m = plt.cm.ScalarMappable(norm=norm);
m.set_array([]);
fcolors = m.to_rgba(color_dimension);

# At this time, X-Y-Z-C are all 2D and we can use "plot_surface".
fig = plt.figure(); ax = fig.gca(projection='3d');
surf = ax.plot_surface(x2, y2, z2, facecolors = fcolors, linewidth=0, rstride=1, cstride=1,
                       antialiased=False);
cbar = fig.colorbar(m, shrink=0.5, aspect=5);
cbar.ax.get_yaxis().labelpad = 15; cbar.ax.set_ylabel("Light", rotation = 270);
ax.set_xlabel("Water"); ax.set_ylabel("Color");
ax.set_zlabel("Heat");
plt.title('');
plt.show();