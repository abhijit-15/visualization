#Author : Abhijeet Phatak
import os
import csv
from tkinter import *
from collections import defaultdict
from urllib.request import urlopen

def shorten(url):
    data = urlopen("http://tinyurl.com/api-create.php?url="+url)
    #print(data)
    return str(data.readlines()[0].decode())

legend_x  = ['black','dark blue','green','sky blue','yellow','red','pink','orange','pale green','maroon','navy','brown','gold','lavender','white']
legend_y = ['"#000000"','"#0000FF"','"#008000"','"#00BFFF"','"#FFFF00"','"#FF0000"','"#FF1493"','"#FF4500"','"#98FB98"','"#800000"','"#000080"','"#8B4513"','"#FFD700"','"#AD00D9"','"#FFFFF"']
    
wd = os.getcwd() 
try:
    os.remove(wd + "\\route_plotter.html")
except:
    pass
filename = wd + "\\route_plotter.html"
f = open(filename,'a')

#center_x = input("Enter lattitude for map center :")
center_x = 12.8852659
#center_y = input("Enter longitude for map center :")
center_y = 77.6533668
#zoom = input("Enter level of zoom :")
zoom = 12

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

print("Enter the file you need to visualize")
root = Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

final_matrix = []
csvfile = open(file_path,'r')
print("Analyzing..." + filename)

reader = csv.reader(csvfile, delimiter=',')
next(reader, None)
for row in reader:
    final_matrix += [row]

vl = []
for j in range(len(final_matrix)):
    vl += [final_matrix[j][0]]
vl_set = set(vl)

if 'Unplanned' in vl_set:
    vl_set.remove('Unplanned')

vl_list = list(int(i) for i in vl_set)
num_of_vans = (max(vl_list))
print("Number of vans used "+str(num_of_vans))


sub2 = """function initialize() {
        var homeLatlng = new google.maps.LatLng(%s,%s);
        var myOptions = {
            zoom: %s,
            center: homeLatlng,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        var map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
""" %(center_x,center_y,zoom)

not_planned = 0
lat_lngs = [] 
for j in range(len(final_matrix)):
	if final_matrix[j][0] == 'Unplanned':
		not_planned += 1
		lat_lngs += [(float(final_matrix[j][5]),float(final_matrix[j][6]))]
print("Number of shipments not planned : "+str(not_planned))

np_s = []
for i in range(len(lat_lngs)):
	np_s += ['[' + str(lat_lngs[i][0]) + ',' + str(lat_lngs[i][1]) + ']'] 

np_string = ','.join(x for x in np_s)

print("Writing the code for plotter...")
subadd = 'var undel = ' + '{' + "'" + 'undel' + "'" + ":" + '[' + np_string + ']' + '}'

subadd2 = """
	  var dont_plot = JSON.parse(JSON.stringify(undel));		  
	  for(i=0;i<dont_plot['undel'].length;i++){
	  var latLng = new google.maps.LatLng(dont_plot['undel'][i][0],dont_plot['undel'][i][1]);
	  var marker = new google.maps.Marker({
		position: latLng,
		map: map});
	};
"""


coords = []
coord_dict = defaultdict(list)
for i in range(len(final_matrix)):
    if final_matrix[i][0] != 'Unplanned':
        coord_dict[int(final_matrix[i][0])].append("new google.maps.LatLng"+str((float(final_matrix[i][5]),float(final_matrix[i][6]))))

#http://10.85.50.254:8990/?point=12.885266%2C77.653367&point=12.878402%2C77.647047&point=12.85261%2C77.660694&locale=en-US&date-time=undefined&layer=OpenStreetMap.de

url_dict = {}
url_short = {}

van_list = sorted(list(set(x for x in list(final_matrix[y][0] for y in range(len(final_matrix))))))
url_list = []

layer = "OpenStreetMap.de" #"Lyrk"
for i in van_list:
    map_url = "http://10.85.50.254:8990/?"
    for j in range(len(final_matrix)):
        if final_matrix[j][0] != 'Unplanned':
            if final_matrix[j][0] == str(i):
                map_url += "point="+str(final_matrix[j][5])+"%2C"+str(final_matrix[j][6])+"&"
            else:
                continue
        else:
            continue
    map_url += "locale=en-US&date-time=undefined&layer=%s" %layer
    url_dict[i] = map_url
    url_short[i] = shorten(str(map_url))

submain = ''

for j in range(num_of_vans):
    arrcoords = "[\n" + ',\n\t\t\t'.join(item for item in coord_dict[j+1]) + "\n]"
    color = legend_y[j]
    submain += """var arrCoords%s = %s;

    var marker = new google.maps.Marker({
          position: %s,
          map: map,
        });
 
    var route%s = new google.maps.Polyline({
    path: arrCoords%s,
    strokeColor: %s,
    strokeOpacity: 1.0,
    strokeWeight: 2,
    geodesic: true,
    map: map
    });
    
    """ %(j,str(arrcoords),str(arrcoords),j,j,color)


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


f.write(sub1)
f.write(sub2)
f.write(subadd)
f.write(subadd2)
f.write(submain)
f.write(sub3)
f.close()
csvfile.close()

print("Legend")
for i in range(num_of_vans):
    print("Route for van "+str(i+1)+" is shown by " + str(legend_x[i]) + " color.")

for i in range(num_of_vans):
    print("Van " + str(i+1) + " detailed route : "+  url_short[str(i+1)])
    #print(url_dict[str(i+1)])
