import os
import sys
import time
import cv2
import requests
from requests.auth import HTTPBasicAuth
import base64
import json
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from qt_material import apply_stylesheet
import ui_main
import _thread

# os.environ["QT_FONT_DPI"] = "96"
widgets = None
thresh_hold = 0.3
basic_auth = None
serviceUrl = None
fps = 0
modelDict = {"目标检测算法": "object",
             "车辆检测算法": "vehicle",
             "人脸检测算法": "faceDetection",
             "安全帽检测算法": "HelmetDetection",
             "烟火检测算法": "fire_smoke",
             "摔倒检测算法": "fallDetection",
             "路面病害检测": "pavementDisease",
             "吸烟检测算法": "smokerDetection",
             "工服检测算法": "uniformDetection",
             "行为检测算法": "bat",
             "疲劳度检测算法": "fatigueDetection",
             "路面积水检测算法": "stagnantWater"
             }

def cv2_to_base64(image):
    data = cv2.imencode('.jpg', image)[1]
    return base64.b64encode(data.tostring()).decode('utf-8')

def predict(model, frame):
    model_url = modelDict[model]
    url = serviceUrl + model_url
    image = cv2_to_base64(frame)
    data = {'images': [image]}
    headers = {"Content-type": "application/json"}
    start_time = time.time()
    r = requests.post(url=url, headers=headers, data=json.dumps(data), auth=basic_auth)
    cost_time = time.time() - start_time
    global fps
    global results
    fps = 1 / cost_time
    rs = r.json()['results'][0]
    results = [x for x in rs if x['score'] > thresh_hold]
    return results

class Thread(QThread):
    updateFrame = Signal(QImage)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.model = None
        self.status = False
        self.cap = True
        self.analyze = False

    def run(self):
        videoSource = widgets.videoSource.text()
        if len(videoSource) == 1:
            videoSource = int(videoSource)
        # initialize the camera
        self.cap = cv2.VideoCapture(videoSource)
        widgets.video.setText("等待视频启动...")
        time.sleep(1)
        ret, frame = self.cap.read()
        # loop over the frames of the video
        count = 0
        global fps
        global results
        while self.status and self.cap.isOpened():
            count += 1
            ret, frame = self.cap.read()
            if not ret:
                continue

            if self.analyze and count % 15 == 0:
                # results = predict(self.model, frame)
                _thread.start_new_thread(predict, (self.model, frame, ))
                count = 0
            if not self.analyze:
                results = []
                fps = 0

            info_description = "fps: {:.2f}".format(fps)
            cv2.putText(frame, info_description, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            if self.model in ["行为检测算法"]:
                for result in results:
                    # print(result)
                    label = result['smoke'] + "-" + result['cellphone']+ "-" + result['headwear'] + ":" + str(round(result['score'], 2))
                    xmin, ymin, w, h = result['bbox']
                    pt1 = (int(xmin), int(ymin))
                    pt2 = (int(xmin + w), int(ymin + h))
                    pad_len = 15 * len(label)
                    pt1_pad = (int(pt1[0] + pad_len), int(pt1[1] - 30))
                    cv2.rectangle(frame, pt1, pt1_pad, (0, 0, 255), -1)
                    cv2.putText(frame, label, pt1, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                    cv2.rectangle(frame, pt1, pt2, color=(0, 0, 255), thickness=2, lineType=4)
            else:
                for result in results:
                    label = result['category'] + ":" + str(round(result['score'], 2))
                    xmin, ymin, w, h = result['bbox']
                    pt1 = (int(xmin), int(ymin))
                    pt2 = (int(xmin + w), int(ymin + h))
                    pad_len = 15 * len(label)
                    pt1_pad = (int(pt1[0] + pad_len), int(pt1[1] - 30))
                    cv2.rectangle(frame, pt1, pt1_pad, (0, 0, 255), -1)
                    cv2.putText(frame, label, pt1, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                    cv2.rectangle(frame, pt1, pt2, color=(0, 0, 255), thickness=2, lineType=4)

            color_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Creating and scaling Qimage
            h, w, ch = color_frame.shape
            img = QImage(color_frame.data, w, h, ch * w, QImage.Format_RGB888)
            w, h = widgets.video.size().width(), widgets.video.size().height()
            scaled_img = img.scaled(w, h, Qt.KeepAspectRatio)
            # Emitting signal
            self.updateFrame.emit(scaled_img)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = ui_main.Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui
        self.setWindowTitle("算法测试工具v0.1")

        # ui setting
        self.ui.startAnalyze.setEnabled(False)
        self.ui.stopAnalyze.setEnabled(False)
        self.ui.closeVideo.setEnabled(False)
        self.ui.algorithmList.currentTextChanged.connect(self.set_model)
        self.ui.videoSource.textChanged.connect(self.set_videoSource)
        self.ui.serviceUrl.textChanged.connect(self.set_serviceUrl)
        self.ui.openVideo.clicked.connect(self.open_video)
        self.ui.closeVideo.clicked.connect(self.close_video)
        self.ui.startAnalyze.clicked.connect(self.start_analyze)
        self.ui.stopAnalyze.clicked.connect(self.stop_analyze)

        # style
        self.ui.mainLayout.setContentsMargins(10, 10, 10, 10)
        self.ui.algorithmList.setFixedSize(200, 35)
        # self.ui.algorithmList.setStyleSheet(
        #     """
        #     width: 200px;
        #     """
        # )

        # fill data
        for key in modelDict:
            self.ui.algorithmList.addItem(key)

        # debug
        # self.ui.videoSource.setText("rtsp://admin:ROTANAVA2019@192.168.0.101:554/h265/ch0/main/av_stream")
        self.ui.serviceUrl.setText("http://192.168.0.165:8866")
        self.ui.username.setText("username")
        self.ui.password.setText("password")


        # Thread in charge of updating the image
        self.th = Thread(self)
        # self.th.finished.connect(self.close)
        self.th.updateFrame.connect(self.setImage)

        self.ui.centralwidget.setLayout(self.ui.mainLayout)
        self.show()

    @Slot()
    def open_video(self):
        print("Starting thread...")
        self.th.status = True
        self.th.start()
        self.ui.closeVideo.setEnabled(True)
        print("Thread started.")

    @Slot()
    def close_video(self):
        print("Finishing thread...")
        self.status = False
        print("Closing video...")
        time.sleep(1)
        self.th.cap.release()
        time.sleep(1)
        print("Video release.")
        self.th.terminate()
        time.sleep(1)
        print("Thread finished.")
        self.ui.video.setText("视频已关闭")
        self.ui.closeVideo.setEnabled(False)

    def set_serviceUrl(self, text):
        # print("设置服务地址:{}".format(text))
        pass

    def set_videoSource(self, text):
        # print("设置视频源:{}".format(text))
        pass

    @Slot()
    def set_model(self, text):
        print("选择算法:{}".format(text))
        self.ui.startAnalyze.setEnabled(True)
        self.th.model = text


    @Slot()
    def setImage(self, image):
        self.ui.video.setPixmap(QPixmap.fromImage(image))

    @Slot()
    def start_analyze(self):
        self.th.analyze = True
        global serviceUrl
        global basic_auth
        serviceUrl = self.ui.serviceUrl.text() + '/predict/'
        basic_auth = HTTPBasicAuth(self.ui.username.text(), self.ui.password.text())
        self.ui.stopAnalyze.setEnabled(True)

    @Slot()
    def stop_analyze(self):
        self.th.analyze = False
        self.ui.stopAnalyze.setEnabled(False)



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
    apply_stylesheet(app, theme='dark_teal.xml')
    sys.exit(app.exec())

