import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.btn_upload_text_file = None
        self.btn_generate_text_from_image = None
        self.btn_generate_image_from_text = None
        self.btn_upload_image_file = None
        self.text_label = None
        self.image_label = None

        self.current_pixmap = None

        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(self.set_text_layout(), stretch=1)
        main_layout.addLayout(self.set_image_layout(), stretch=1)

    def set_text_layout(self) -> QtWidgets.QVBoxLayout:
        self.text_label = QtWidgets.QLabel()
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(False)
        self.text_label.setText("No Text Loaded")

        self.btn_upload_text_file = QtWidgets.QPushButton("Open file")
        self.btn_upload_text_file.clicked.connect(self.load_text)
        self.btn_generate_image_from_text = QtWidgets.QPushButton("Generate Image")
        self.btn_generate_image_from_text.clicked.connect(self.generate_image_from_text)
        self.btn_generate_image_from_text.setEnabled(False)

        text_area = QtWidgets.QScrollArea()
        text_area.setWidgetResizable(True)
        text_area.setWidget(self.text_label)

        text_layout = QtWidgets.QVBoxLayout()
        text_layout.addWidget(text_area)
        text_layout.addWidget(self.btn_upload_text_file)
        text_layout.addWidget(self.btn_generate_image_from_text)

        return text_layout

    def set_image_layout(self) -> QtWidgets.QVBoxLayout:
        self.image_label = QtWidgets.QLabel()
        self.image_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.image_label.setText("No Image Loaded")
        self.image_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored)

        self.btn_upload_image_file = QtWidgets.QPushButton("Load Image")
        self.btn_upload_image_file.clicked.connect(self.load_image)
        self.btn_generate_text_from_image = QtWidgets.QPushButton("Generate Text")
        self.btn_generate_text_from_image.clicked.connect(self.generate_text_from_image)
        self.btn_generate_text_from_image.setEnabled(False)

        image_layout = QtWidgets.QVBoxLayout()
        image_layout.addWidget(self.image_label)
        image_layout.addWidget(self.btn_upload_image_file)
        image_layout.addWidget(self.btn_generate_text_from_image)

        return image_layout

    @QtCore.Slot()
    def load_text(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self, "Open Text File")
        text = None
        with open(file[0]) as file:
            text = file.readlines()
        text = ' '.join(text)
        self.set_text_parameters(text)
        self.btn_generate_image_from_text.setEnabled(True)

        self.image_label.clear()
        self.image_label.setText("No Image Loaded")
        self.current_pixmap = None
        self.btn_generate_text_from_image.setEnabled(False)

    @QtCore.Slot()
    def load_image(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Image File", "",
                                                             "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.current_pixmap = QtGui.QPixmap(file_path)
            self.update_image_label()

            self.btn_generate_text_from_image.setEnabled(True)

            self.text_label.clear()
            self.current_pixmap = None
            self.reset_text_parameters()
            self.btn_generate_image_from_text.setEnabled(False)

    @QtCore.Slot()
    def generate_image_from_text(self):
        print('Generating image...')

    @QtCore.Slot()
    def generate_text_from_image(self):
        print('Generating text...')
        self.text_label.setText("Generating text...")

    def set_text_parameters(self, text):
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)
        self.text_label.setFont(QtGui.QFont("Courier", 10))
        self.text_label.setText(text)

    def reset_text_parameters(self):
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setFont(QtGui.QFont())
        self.text_label.setText("No Text Loaded")

    def update_image_label(self):
        # Масштабируем изображение в соответствии с текущим размером QLabel
        if self.current_pixmap:
            scaled_pixmap = self.current_pixmap.scaled(
                self.image_label.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)

    def resizeEvent(self, event):
        self.update_image_label()
        super().resizeEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
