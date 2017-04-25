#Author : Abhijeet Phatak
import os
import csv
from tkinter import *
from collections import defaultdict

legend_x  = ['black','dark blue','green','sky blue','yellow','red','pink','orange','pale green','maroon','navy','brown','gold','lavender','white']
legend_y = ['"#000000"','"#0000FF"','"#008000"','"#00BFFF"','"#FFFF00"','"#FF0000"','"#FF1493"','"#FF4500"','"#98FB98"','"#800000"','"#000080"','"#8B4513"','"#FFD700"','"#AD00D9"','"#FFFFF"']
    
wd = os.getcwd() 
try:
    os.remove(wd + "\\route_plotter.html")
except:
    pass
filename = wd + "\\damage_plotter.html"
f = open(filename,'a')

#center_x = input("Enter lattitude for map center :")
center_x = 23.3333
#center_y = input("Enter longitude for map center :")
center_y = 78.7847
#zoom = input("Enter level of zoom :")
zoom = 5

sub1 = """<!DOCTYPE html>
<html>
<head>
<title>Route Optimization Visualization</title>

<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
<style type="text/css">
html { height: 100% }
body { height: 100%; margin: 0; padding: 0 }
#map_canvas { height: 100% }
</style>
<script type="text/javascript" src="http://maps.googleapis.com/maps/api/js"></script>

<script>
"""

#print("Enter the file you need to visualize")
#root = Tk()
#root.withdraw()
#file_path = filedialog.askopenfilename()

file_path  = 'C:/Users/phatak.a/Downloads/routePlotter/rvp_lanes_wise_lanes.csv'

final_matrix = []
csvfile = open(file_path,'r')
print("Analyzing..." + filename)

reader = csv.reader(csvfile, delimiter=',')
next(reader, None)
for row in reader:
    final_matrix += [row]

print("Writing the code for plotter...")
sub2 = """function initialize() {
        var homeLatlng = new google.maps.LatLng(%s,%s);
        var myOptions = {
            zoom: %s,
            center: homeLatlng,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        var map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
""" %(center_x,center_y,zoom)

coords = []
coord_dict = defaultdict(list)
for i in range(len(final_matrix)):
    coord_dict[int(final_matrix[i][0])].append("new google.maps.LatLng"+str((float(final_matrix[i][2]),float(final_matrix[i][3]))))
    print(str(i)+" : "+str((final_matrix[i][2],final_matrix[i][3]))+"-"+str((final_matrix[i][5],final_matrix[i][6])))
    coord_dict[int(final_matrix[i][0])].append("new google.maps.LatLng"+str((float(final_matrix[i][5]),float(final_matrix[i][6]))))
    
submain = ''

for j in range(len(final_matrix)):
    arrcoords = "[\n" + ',\n\t\t\t'.join(item for item in coord_dict[j+1]) + "\n]"
    color = legend_y[5]
    strokeWeight = 2
    '''
    if float(final_matrix[j][-1]) < 2:
        color = legend_y[2]
        strokeWeight = 0.1
    elif float(final_matrix[j][-1]) < 4:
        color = legend_y[4]
        strokeWeight = 1
    else:
        color = legend_y[5]
        strokeWeight = 1
    '''
    submain += """var arrCoords%s = %s;
 
    var route%s = new google.maps.Polyline({
    path: arrCoords%s,
    strokeColor: %s,
    strokeOpacity: 0.8,
    strokeWeight: %s,
    geodesic: false,
    map: map
    });
    
    """ %(j,str(arrcoords),j,j,color,strokeWeight)

sub3 = """
\t\t;
\t}
google.maps.event.addDomListener(window, 'load', initialize);
</script>
</head>
<body>
  <div id="map_canvas"></div>
</body>
</html>"""

print("Damage Plot is done")
f.write(sub1)
f.write(sub2)
f.write(submain)
f.write(sub3)
f.close()
csvfile.close()
