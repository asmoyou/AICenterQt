import os
import sys
import time

import cv2
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from qt_material import apply_stylesheet
import ui_AICenterMain

# os.environ["QT_FONT_DPI"] = "96"

#global widgets
widgets = None

class Thread(QThread):
    updateFrame = Signal(QImage)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.trained_file = None
        self.status = True
        self.cap = True

    def set_file(self, fname):
        # The data comes with the 'opencv-python' module
        self.trained_file = os.path.join(cv2.data.haarcascades, fname)

    def run(self):
        self.cap = cv2.VideoCapture(1)
        while self.status:
            cascade = cv2.CascadeClassifier(self.trained_file)
            ret, frame = self.cap.read()
            if not ret:
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            detections = cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in detections:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            color_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Creating and scaling Qimage
            h, w, ch = color_frame.shape
            img = QImage(color_frame.data, w, h, ch * w, QImage.Format_RGB888)
            scaled_img = img.scaled(640, 480, Qt.KeepAspectRatio)

            # Emitting signal
            self.updateFrame.emit(scaled_img)
        sys.exit(-1)


class QSSLoader:
    def __init__(self):
        pass

    @staticmethod
    def read_qss_file(qss_file_name):
        with open(qss_file_name, "r", encoding='UTF-8') as file:
            return file.read()

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = ui_AICenterMain.Ui_MainWindow()
        self.ui.setupUi(self)
        self.cwd = os.getcwd()
        self.setWindowTitle("AICenter")
        self.menu = self.menuBar()
        self.menu_file = self.menu.addMenu("File")
        exit = QAction("Exit", self, triggered=app.quit)
        self.menu_file.addAction(exit)

        self.menu_about = self.menu.addMenu("test")
        about = QAction("About Qt", self, shortcut=QKeySequence(QKeySequence.HelpContents),
                        triggered=app.aboutQt)
        self.menu_about.addAction(about)
        self.menu_about.addAction(about)

        # Create a label for the display camera
        self.label = QLabel(self)
        self.label.setFixedSize(640, 480)

        # Thread in charge of updating the image
        self.th = Thread(self)
        self.th.finished.connect(self.close)
        self.th.updateFrame.connect(self.setImage)

        # Model group
        self.group_model = QGroupBox("Trained Model")
        self.group_model.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        model_layout = QVBoxLayout()

        self.combobox = QComboBox()
        for xml_file in os.listdir(cv2.data.haarcascades):
            if xml_file.endswith(".xml"):
                self.combobox.addItem(xml_file)

        model_layout.addWidget(QLabel("File:"), 10)
        model_layout.addWidget(self.combobox, 90)
        self.group_model.setLayout(model_layout)

        # Buttons layout
        buttons_layout = QHBoxLayout()
        self.button1 = QPushButton("Start")
        self.button2 = QPushButton("Stop/Close")
        self.button1.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.button2.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        buttons_layout.addWidget(self.button1)
        buttons_layout.addWidget(self.button2)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.group_model, 1)
        right_layout.addLayout(buttons_layout, 1)

        # Main layout
        layout = QVBoxLayout()
        self.setMenuBar(self.menu)
        layout.addWidget(self.label)
        layout.addLayout(right_layout)

        # Central widget
        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Connections
        self.button1.clicked.connect(self.start)
        self.button2.clicked.connect(self.kill_thread)
        self.button2.setEnabled(False)
        self.combobox.currentTextChanged.connect(self.set_model)

        # mycode
        self.show()
        # self.ui.open.clicked.connect(self.start_service)
        # self.ui.pushButton.clicked.connect(self.error_alert)

    @Slot()
    def set_model(self, text):
        self.th.set_file(text)

    @Slot()
    def kill_thread(self):
        print("Finishing thread...")
        self.button2.setEnabled(False)
        self.button1.setEnabled(True)
        self.th.cap.release()
        cv2.destroyAllWindows()
        self.status = False
        self.th.terminate()
        time.sleep(1)

    @Slot()
    def start(self):
        print("Starting thread...")
        self.button1.setEnabled(False)
        self.button2.setEnabled(True)
        self.th.set_file(self.combobox.currentText())
        self.th.start()

    @Slot()
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))


    def start_service(self):
        button = QMessageBox.question(self, "Start Service",
                                      "Are you sure you want to start the service?",
                                      QMessageBox.Yes | QMessageBox.No)
        # QMessageBox.information(self, "Start Service", "Service started")
        if button == QMessageBox.Yes:
            print("Service started")
        else:
            print("Service not started")

    def error_alert(self):
        button = QMessageBox.critical(self, "Error",
                                      "Error occurred",
                                      buttons=QMessageBox.Discard | QMessageBox.NoToAll | QMessageBox.Ignore,
                                      defaultButton=QMessageBox.Discard)
        if button == QMessageBox.Discard:
            print("Discard")
        elif button == QMessageBox.NoToAll:
            print("NoToAll")
        elif button == QMessageBox.Ignore:
            print("Ignore")






if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("logo.ico"))
    window = MainWindow()
    # style_file = 'themes/theme_dark.qss'
    # style_sheet = QSSLoader.read_qss_file(style_file)
    # window.setStyleSheet(style_sheet)
    apply_stylesheet(app, theme='dark_teal.xml')
    sys.exit(app.exec())

