import sys

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QFileDialog, QLabel, QMessageBox

from calc_back import EncoderBack


def show_message(title, message):
    msg_box = QMessageBox()
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setIcon(QMessageBox.Warning)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec_()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.encoder = None
        self.layout = QVBoxLayout()
        self.encode_input_field = None
        self.init_ui()
        self.setMinimumSize(1080, 720)

    def create_button(self, label, action):
        btn = QPushButton(label, self)
        btn.clicked.connect(action)
        return btn

    def init_ui(self):
        self.setWindowTitle('Стеганография')

        self.layout.addWidget(self.create_button('Зашифровать', self.show_encode_ui))
        self.layout.addWidget(self.create_button('Расшифровать', self.show_decode_ui))

        self.setLayout(self.layout)

    def show_encode_ui(self):
        self.clear_layout()

        self.encode_input_field = QLineEdit(self)
        ascii_regex = QRegExp("[\x00-\x7F]*")
        ascii_validator = QRegExpValidator(ascii_regex, self.encode_input_field)
        self.encode_input_field.setValidator(ascii_validator)
        self.layout.addWidget(self.encode_input_field)

        self.layout.addWidget(self.create_button('Выбрать фотографию', self.open_file_dialog))
        self.layout.addWidget(self.create_button('Зашифровать', self.encode_action))
        self.layout.addWidget(self.create_button('Сохранить изменения', self.save_file_dialog))
        self.layout.addWidget(self.create_button('Вернуться', self.show_main_ui))

        self.setLayout(self.layout)

    def show_decode_ui(self):
        self.clear_layout()

        self.layout.addWidget(self.create_button('Выберите файл', self.open_file_dialog))
        self.layout.addWidget(self.create_button('Расшифровать', self.decode_action))
        self.layout.addWidget(self.create_button('Вернуться', self.show_main_ui))

        self.setLayout(self.layout)

    def clear_layout(self):
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def open_file_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите фотографию", filter="*.bmp")
        if file_name:
            try:
                self.encoder = EncoderBack(file_name)
            except Exception as e:
                show_message("Ошибка", e)

    def save_file_dialog(self):
        if self.encoder is None:
            show_message("Ошибка", "Необходимо выбрать фотографию")
            return
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить")
        if file_name:
            self.encoder.save_image(file_name)

    def encode_action(self):
        if self.encoder is None:
            show_message("Ошибка", "Необходимо выбрать фотографию")
            return
        input_text = self.encode_input_field.text()
        if input_text == "":
            show_message("Ошибка", "Необходимо ввести текст")
            return
        try:
            self.encoder.encode_message(input_text)
            show_message("Успех", f"Сообщение успешно закодировано в фотографию")
        except Exception as e:
            show_message("Ошибка", str(e))

    def decode_action(self):
        if self.encoder is None:
            show_message("Ошибка", "Необходимо выбрать фотографию")
            return
        try:
            decoded_text = self.encoder.decode_message()
        except Exception as e:
            show_message("Ошибка", str(e))
            return

        show_message("Результат", f"Расшифрованная строка: {decoded_text}")

    def show_main_ui(self):
        if not self.encoder.saved:
            reply = QMessageBox.question(self, 'Подтвердите', 'У вас есть несохраненные изменения.\nПри переходе они будут потеряны. Вы уверены?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return
        self.encoder = None
        self.clear_layout()
        self.init_ui()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
