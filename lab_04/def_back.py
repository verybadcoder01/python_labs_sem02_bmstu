import math

def dist_sq(point_a, point_b):
    return (point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2

def dist(point_a, point_b):
    return math.sqrt(dist_sq(point_a, point_b))

def find_closest_point(points, point_p):
    if len(points) == 0:
        return -1
    min_ind = 0
    min_dist = dist_sq(points[0], point_p)
    for i in range(1, len(points)):
        cur_dist = dist_sq(points[i], point_p)
        if cur_dist < min_dist:
            min_dist = cur_dist
            min_ind = i
    return min_ind, min_dist

def find_min_circle(points):
    min_rad = math.inf
    best_res = (-1, -1, -1)
    for center_ind in range(len(points)):
        for point_b_ind in range(len(points)):
            for point_c_ind in range(len(points)):
                center = points[center_ind]
                point_b = points[point_b_ind]
                point_c = points[point_c_ind]
                if point_b == point_c or point_c == center or point_b == center:
                    continue
                if abs(dist_sq(center, point_b) - dist_sq(center, point_c)) <= 1e-5 and dist_sq(center, point_b) < min_rad:
                    best_res = (center_ind, point_b_ind, point_c_ind)
                    min_rad = dist_sq(center, point_b)
    return best_res[0], best_res[1], best_res[2]