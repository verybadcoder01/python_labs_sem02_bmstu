import sys

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                             QTableWidget, QTableWidgetItem, QLineEdit, QPushButton, QLabel,
                             QFrame, QSizePolicy)
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QPointF
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import QMessageBox

from def_back import find_min_circle, find_closest_point, dist

WRONG_COORD_NUMBER = Exception("Некорректное число координат")
WRONG_SCOPE = Exception("Все координаты должны быть в отрезке [-50; 50]")


def show_message(title, message):
    msg_box = QMessageBox()
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setIcon(QMessageBox.Warning)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec_()


class PointsCanvas(QWidget):
    point_added = pyqtSignal(tuple)
    point_removed = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 400)
        self.points = []
        self.circle_points_inds = []
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.logical_x_min = -50.0
        self.logical_x_max = 50.0
        self.logical_y_min = -50.0
        self.logical_y_max = 50.0

    def widget_to_logical(self, x, y):
        w = self.width()
        h = self.height()
        logical_x = self.logical_x_min + (x / w) * (self.logical_x_max - self.logical_x_min)
        logical_y = self.logical_y_max - (y / h) * (self.logical_y_max - self.logical_y_min)
        return logical_x, logical_y

    def logical_to_widget(self, x, y):
        w = self.width()
        h = self.height()
        widget_x = (x - self.logical_x_min) / (self.logical_x_max - self.logical_x_min) * w
        widget_y = (self.logical_y_max - y) / (self.logical_y_max - self.logical_y_min) * h
        return widget_x, widget_y

    def set_circle(self, point_a, point_b, point_c):
        self.circle_points_inds = [point_a, point_b, point_c]

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            point = self.widget_to_logical(event.x(), event.y())
            self.points.append(point)
            self.point_added.emit(point)
            self.update()
        elif event.button() == Qt.RightButton:
            point = self.widget_to_logical(event.x(), event.y())
            closest_point, min_dist = find_closest_point(self.points, point)
            if closest_point == -1 or min_dist > 5:
                return
            self.points.pop(closest_point)
            self.point_removed.emit(closest_point)
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setPen(QPen(Qt.gray, 1, Qt.DotLine))
        for x in range(int(self.logical_x_min), int(self.logical_x_max) + 1):
            wx, _ = self.logical_to_widget(x, 0)
            painter.drawLine(int(wx), 0, int(wx), self.height())
        for y in range(int(self.logical_y_min), int(self.logical_y_max) + 1):
            _, wy = self.logical_to_widget(0, y)
            painter.drawLine(0, int(wy), self.width(), int(wy))

        painter.setPen(QPen(Qt.red, 6))
        for x, y in self.points:
            wx, wy = self.logical_to_widget(x, y)
            painter.drawPoint(int(wx), int(wy))

        if len(self.circle_points_inds) == 3:
            painter.setPen(QPen(Qt.blue, 3))
            center_logical = self.points[self.circle_points_inds[0]]
            point_b_logical = self.points[self.circle_points_inds[1]]
            center_widget = self.logical_to_widget(center_logical[0], center_logical[1])
            point_b_widget = self.logical_to_widget(point_b_logical[0], point_b_logical[1])
            rad = dist(center_widget, point_b_widget)
            painter.drawEllipse(
                QPointF(center_widget[0], center_widget[1]),
                rad,
                rad
            )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Решение планиметрической задачи')
        self.setGeometry(100, 100, 1200, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout()
        main_widget.setLayout(layout)

        left_panel = QVBoxLayout()

        input_group = QVBoxLayout()
        self.input_point = QLineEdit()
        input_group.addWidget(QLabel("Введите точку в формате (x y):"))
        input_group.addWidget(self.input_point)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["X", "Y"])

        self.btn_add = QPushButton("Добавить точку")
        self.btn_clear = QPushButton("Очистить точки")
        self.btn_calc = QPushButton("Решить задачу")
        self.btn_clear_result = QPushButton("Очистить результат задачи")

        left_panel.addLayout(input_group)
        left_panel.addWidget(self.table)
        left_panel.addWidget(self.btn_add)
        left_panel.addWidget(self.btn_calc)
        left_panel.addWidget(self.btn_clear)
        left_panel.addWidget(self.btn_clear_result)

        self.canvas = PointsCanvas()
        layout.addLayout(left_panel, 1)
        layout.addWidget(self.canvas, 2)

        self.btn_add.clicked.connect(self.add_point)
        self.btn_clear.clicked.connect(self.clear_points)
        self.canvas.point_added.connect(self.add_table_row)
        self.canvas.point_removed.connect(self.remove_table_row)
        self.btn_calc.clicked.connect(self.find_circle)
        self.btn_clear_result.clicked.connect(self.clear_result)

    def add_point(self):
        try:
            point = list(map(lambda x: float(x), self.input_point.text().split(" ")))
            if len(point) != 2:
                raise WRONG_COORD_NUMBER
            elif point[0] < self.canvas.logical_x_min or point[0] > self.canvas.logical_x_max or point[
                1] < self.canvas.logical_y_min or point[1] > self.canvas.logical_y_max:
                raise WRONG_SCOPE
        except Exception as e:
            s = "Некорректный ввод"
            if e == WRONG_SCOPE or e == WRONG_COORD_NUMBER:
                s = str(e)
            show_message("Ошибка", s)
            return
        self.add_table_row(point)
        self.canvas.points.append(point)
        self.canvas.update()

    def add_table_row(self, point):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(f"{point[0]:.6f}"))
        self.table.setItem(row, 1, QTableWidgetItem(f"{point[1]:.6f}"))

    def remove_table_row(self, row_ind):
        self.table.removeRow(row_ind)

    def clear_points(self):
        self.table.setRowCount(0)
        self.canvas.points.clear()
        self.canvas.update()

    def find_circle(self):
        points = self.canvas.points
        if len(points) < 3:
            show_message("Ошибка", "Слишком мало точек. Необходимо хотя бы 3")
            return
        ind_a, ind_b, ind_c = find_min_circle(points)
        if ind_a == -1 and ind_b == -1 and ind_c == -1:
            show_message("Результат", "Нет 3 точек, на которых можно построить окружность")
            return
        self.canvas.set_circle(ind_a, ind_b, ind_c)
        self.canvas.update()

    def clear_result(self):
        self.canvas.circle_points_inds = []
        self.canvas.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
