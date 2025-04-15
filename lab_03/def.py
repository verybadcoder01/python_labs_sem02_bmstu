from random import random, randint
import math
from PIL import Image

CLUSTER_COLORS = [[255, 0, 0], [0, 255, 0], [0, 0, 255]]
WHITE = (0, 0, 0)
BLACK = (255, 255, 255)


def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]))


def gen_black_points_image(img_path, cnt):
    size = (50, 50)
    img = Image.new("RGB", size, WHITE)
    pixel_data = [WHITE] * size[0] * size[1]
    rand_points = [randint(0, size[0] * size[1] - 1) for _ in range(cnt)]
    for p in rand_points:
        pixel_data[p] = BLACK
    img.putdata(pixel_data)
    img.save(img_path)


class ImageWorker:
    def __init__(self, img_path):
        self.img_path = img_path
        img_data = Image.open(img_path)
        self.pixel_values = [list(i) for i in list(img_data.getdata())]
        self.channels_count = len(self.pixel_values[0])
        self.width = img_data.width
        self.height = img_data.height
        img_data.close()

    def extract_black_points(self):
        return [[i // self.width, i % self.width] for i in range(len(self.pixel_values)) if
                self.pixel_values[i] == list(WHITE)]

    def place_point_on_img(self, x, y, color):
        self.pixel_values[x * self.width + y] = color

    def remove_not_bw(self):
        for i in range(len(self.pixel_values)):
            if self.pixel_values[i] == CLUSTER_COLORS[0] or self.pixel_values == CLUSTER_COLORS[
                1] or self.pixel_values == CLUSTER_COLORS[2]:
                self.pixel_values[i] = list(BLACK)

    def save_image(self, path):
        img_data = Image.open(self.img_path)
        new_img = Image.new(img_data.mode, img_data.size, WHITE)
        new_img.putdata([tuple(i) for i in self.pixel_values])
        new_img.save(path)


class KMeans:
    def __init__(self, points, bound_x, bound_y):
        self.points = points
        self.cluster_ind = [randint(0, 2) for _ in range(len(points))]
        self.centers = []
        for i in range(3):
            self.centers.append([round(random() * bound_x), round(random() * bound_y)])

    def recalc_centers(self):
        for p_ind in range(len(self.points)):
            cur_closest = 0
            cur_min_dist = dist(self.points[p_ind], self.centers[0])
            for c_ind in range(len(self.centers)):
                c_dist = dist(self.centers[c_ind], self.points[p_ind])
                if c_dist < cur_min_dist:
                    cur_closest = c_ind
                    cur_min_dist = c_dist
            self.cluster_ind[p_ind] = cur_closest
        cluster_sum = [[0, 0], [0, 0], [0, 0]]
        cluster_points_cnt = [0, 0, 0]
        for i in range(len(self.points)):
            cluster_sum[self.cluster_ind[i]][0] += self.points[i][0]
            cluster_sum[self.cluster_ind[i]][1] += self.points[i][1]
            cluster_points_cnt[self.cluster_ind[i]] += 1
        for i in range(len(self.centers)):
            self.centers[i][0] = round(cluster_sum[i][0] / cluster_points_cnt[i])
            self.centers[i][1] = round(cluster_sum[i][1] / cluster_points_cnt[i])

    def get_clusters(self):
        cl = [[], [], []]
        for i in range(len(self.cluster_ind)):
            cl[self.cluster_ind[i]].append(self.points[i])
        return cl

    def iterate(self, n):
        for i in range(n):
            self.recalc_centers()
            yield self.centers, self.get_clusters()


def main():
    # gen_black_points_image("white.bmp", 10000)
    img_path = "white.bmp"
    worker = ImageWorker(img_path)
    black_points = worker.extract_black_points()
    k_mean_worker = KMeans(black_points, worker.height, worker.width)
    for centers, clusters in k_mean_worker.iterate(10):
        worker.remove_not_bw()
        for c_ind in range(len(centers)):
            for point in clusters[c_ind]:
                worker.place_point_on_img(point[0], point[1], CLUSTER_COLORS[c_ind])
            print(f"Координаты центра: {centers[c_ind][0]}, {centers[c_ind][1]}")
        worker.save_image(img_path)
        _ = input("Проверьте изображение\n")


if __name__ == '__main__':
    main()
