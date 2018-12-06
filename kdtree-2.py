# read data in in the format points = [(x, y, c)]
import csv
import re
points = []
with open('leedata2.txt', 'rb') as csvfile:
    for line in csvfile.readlines():
        if line.startswith('%'):
            continue
        safe_line = re.sub(' +', ' ', line)
        safe_line = safe_line.strip()
        point_data = safe_line.split(' ')
        points.append((float(point_data[0]), float(point_data[1]), float(point_data[3])))

# Filter out points we don't care about
min_y = -20000
max_y = 6000
max_x = 260
min_x = 0
all_nozzle_points = []
for point in points:
    if point[0] > min_x and point[0] < max_x and point[1] < max_y and point[1] > min_y:
        all_nozzle_points.append(point)

# Sort all points by y value
sorted_nozzle_points = sorted(all_nozzle_points, key=lambda tup: tup[1], reverse=True)

# Scan down the y axis looking for a y to y+1 point that is all green
min_point_in_data = 0
max_point_in_data = len(sorted_nozzle_points)
while min_point_in_data != max_point_in_data:
    current_point = (min_point_in_data+max_point_in_data)/2
    point = sorted_nozzle_points[current_point]

    print("Analysing point %f %f with %f" % point)
    bound = point[1] + 1
    is_all_green = True
    for point2 in sorted_nozzle_points[current_point:]:
       if point2[1] > bound:
           break
       if not (point2[2] >= 0.44 and point2[2] < 0.55):
           is_all_green = False
           break

    if not is_all_green:
        min_point_in_data = current_point+1
    else:
        max_point_in_data = current_point

print("Found point %f with concentration %f with all points +1um green" % (sorted_nozzle_points[current_point][1], sorted_nozzle_points[current_point][2]))
