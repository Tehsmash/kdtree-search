import csv
import re
import math
import time

# read data in in the format points = [(x, y, c)]
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
all_nozzle_points = points


class KDNode(object):
    point = None
    depth = 0
    left_child = None
    right_child = None


def make_kd_tree(points, depth=0):
    if not points:
        return None
    axis = depth % 2
    sorted_points = sorted(points, key=lambda tup: tup[axis], reverse=True)
    middle = len(sorted_points)//2

    node = KDNode()
    node.point = sorted_points[middle]
    node.depth = depth
    node.left_child = make_kd_tree(sorted_points[:middle], depth+1)
    node.right_child = make_kd_tree(sorted_points[middle+1:], depth+1)
    return node


tree= make_kd_tree(all_nozzle_points)


def distance(pointa, pointb):
    return ((pointa[0]-pointb[0])**2) + ((pointa[1]-pointb[1])**2)


def nearest_neighbour(node, point, _best=None):
    if node is None:
        return _best
    if _best is None:
        _best = node.point
    if distance(point, node.point) < distance(point, _best):
        _best = node.point

    axis = node.depth % 2

    if point[axis] > node.point[axis]:
        _best = nearest_neighbour(node.left_child, point, _best)
    else:
        _best = nearest_neighbour(node.right_child, point, _best)
    
    point_on_axis = list(point)
    point_on_axis[axis] = node.point[axis]

    if distance(point, tuple(point_on_axis)) < distance(point, _best):
        if point[axis] > node.point[axis]:
            _best = nearest_neighbour(node.right_child, point, _best)
        else:
            _best = nearest_neighbour(node.left_child, point, _best)

    return _best

def find_first_all_green(max_y, min_y, sample_size):
    if print_output:
        print("Scanning %d to %d per %d" % (max_y, min_y, sample_size))
    for y in range(max_y, min_y, -sample_size):
        youtput = "y = %d \t" % y
        all_green = True
        for x in range(nozzle_min_x, nozzle_max_x, 1):
            best = nearest_neighbour(tree, (x, y))

            if best[2] >= over_concentration_value:
                youtput += "R"
                all_green = False
            elif best[2] < under_concentration_value:
                youtput += "B"
                all_green = False
            else:
                youtput += "G"
        if print_output:
            print(youtput)
        if all_green:
            break
    return y

print_output = False
over_concentration_value = 0.55
under_concentration_value = 0.44
nozzle_min_y = -20000
nozzle_max_y = 6000
nozzle_min_x = 0
nozzle_max_x = 260

high_scale = find_first_all_green(nozzle_max_y, nozzle_min_y, 1000)
mid_scale = find_first_all_green(high_scale+1000, high_scale, 100)
fine_scale = find_first_all_green(mid_scale+100, mid_scale, 10)
finer_scale = find_first_all_green(fine_scale+10, fine_scale, 1)

print(finer_scale)
