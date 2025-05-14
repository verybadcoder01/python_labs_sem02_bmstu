import math


def cross_product(point_a, point_b):
    return point_a[0] * point_b[1] - point_a[1] * point_b[0]


def build_vector(point_a, point_b):
    return [point_b[0] - point_a[0], point_b[1] - point_a[1]]


def dist_sq(point_a, point_b):
    return (point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2

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

def is_inside_triangle(A, B, C, P):
    ab_vector = build_vector(A, B)
    ac_vector = build_vector(A, C)
    cross_ab = cross_product(ab_vector, ac_vector)
    ap_vector = build_vector(A, P)
    cross_p_ab = cross_product(ab_vector, ap_vector)
    if cross_ab * cross_p_ab < 0 or cross_p_ab == 0:
        return False

    bc_vector = build_vector(B, C)
    cross_bc = cross_product(bc_vector, ab_vector)
    pb_vector = build_vector(P, B)
    cross_p_bc = cross_product(bc_vector, pb_vector)
    if cross_bc * cross_p_bc < 0 or cross_p_bc == 0:
        return False

    ac_vector = build_vector(A, C)
    cross_ca = cross_product(ac_vector, bc_vector)
    pc_vector = build_vector(P, C)
    cross_p_ca = cross_product(ac_vector, pc_vector)
    if cross_ca * cross_p_ca < 0 or cross_p_ca == 0:
        return False

    return True


def is_on_segment(A, B, P):
    sq_seg_len = dist_sq(A, B)
    return abs(sq_seg_len - dist_sq(A, P) - dist_sq(B, P)) <= 1e-5


def point_on_triangle_sides(A, B, C, P):
    return (is_on_segment(A, B, P) or
            is_on_segment(B, C, P) or
            is_on_segment(C, A, P))


def calc_points_inside_triangle(points, point_a, point_b, point_c):
    return sum(1 for P in points if
               is_inside_triangle(point_a, point_b, point_c, P) and not point_on_triangle_sides(point_a, point_b,
                                                                                                point_c, P))


def calc_points_outside_triangle(points, point_a, point_b, point_c):
    return sum(1 for P in points if
               not is_inside_triangle(point_a, point_b, point_c, P) and not point_on_triangle_sides(point_a, point_b,
                                                                                                    point_c, P))


def build_triangle(points):
    min_diff = math.inf
    best_res = (-1, -1, -1)
    for point_a_ind in range(len(points)):
        for point_b_ind in range(len(points)):
            for point_c_ind in range(len(points)):
                point_a = points[point_a_ind]
                point_b = points[point_b_ind]
                point_c = points[point_c_ind]
                points_inside = calc_points_inside_triangle(points, point_a, point_b, point_c)
                points_outside = calc_points_outside_triangle(points, point_a, point_b, point_c)
                if abs(points_inside - points_outside) < min_diff:
                    min_diff = abs(points_inside - points_outside)
                    best_res = (point_a_ind, point_b_ind, point_c_ind)
    return best_res
