# encoding=utf-8

import sys
import cv2
import numpy as np
import threading
import time
#from multiprocessing import Queue
from queue import Queue

from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow,
    QGroupBox, QVBoxLayout, QHBoxLayout,
    QPushButton, QCheckBox
)
from PyQt5 import QtGui, QtCore, uic
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QPoint



# -------------------------------
# ---------- CONSTANTS ----------
# -------------------------------



# -------------------------------
# ---------- VARIABLES ----------
# -------------------------------
runnning = False
capture_thread = None
form_class = uic.loadUiType("simple.ui")[0]
q = Queue()



# -----------------------------
# ---------- METHODS ----------
# -----------------------------
def grab(cam, queue, width, height, fps):
    global running
    capture = cv2.VideoCapture(cam)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    capture.set(cv2.CAP_PROP_FPS, fps)

    while(running):
        frame = {}
        capture.grab()
        retval, img = capture.retrieve(0)
        frame["img"] = img

        print(frame)

        if queue.qsize() < 10:
            queue.put(frame)
        else:
            print(queue.qsize())



# -----------------------------
# ---------- CLASSES ----------
# -----------------------------
class OwnImageWidget(QWidget):
    def __init__(self, parent=None):
        super(OwnImageWidget, self).__init__(parent)
        self.image = None
    
    def setImage(self, image):
        self.image = image
        sz = image.size()
        self.setMinimumSize(sz)
        self.update()

    def printEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        print(self.image)
        if self.image:
            qp.drawImage(QPoint(0, 0), self.image)
        qp.end()


class MyWindowClass(QMainWindow, form_class):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.startButton.clicked.connect(self.start_clicked)
        
        self.window_width = self.ImgWidget.frameSize().width()
        self.window_height = self.ImgWidget.frameSize().height()
        self.ImgWidget = OwnImageWidget(self.ImgWidget)       

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1)

    def start_clicked(self):
        global running
        running = True
        capture_thread.start()
        self.startButton.setEnabled(False)
        self.startButton.setText('Starting...')

    def update_frame(self):
        if not q.empty():
            self.startButton.setText('Camera is live')
            frame = q.get()
            img = frame["img"]

            img_height, img_width, img_colors = img.shape
            scale_w = float(self.window_width) / float(img_width)
            scale_h = float(self.window_height) / float(img_height)
            scale = min([scale_w, scale_h])

            if scale == 0:
                scale = 1
            
            img = cv2.resize(img, None, fx=scale, fy=scale, interpolation = cv2.INTER_CUBIC)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            height, width, bpc = img.shape
            bpl = bpc * width
            image = QtGui.QImage(img.data, width, height, bpl, QtGui.QImage.Format_RGB888)
            self.ImgWidget.setImage(image)

    def closeEvent(self, event):
        global running
        running = False




# ----------------------------------
# ---------- MAIN METHODS ----------
# ----------------------------------



# --------------------------
# ---------- MAIN ----------
# --------------------------
capture_thread = threading.Thread(target=grab, args = (0, q, 1920, 1080, 30))

app = QApplication(sys.argv)
w = MyWindowClass(None)
w.setWindowTitle('Kurokesu PyQT OpenCV USB camera test panel')
w.show()
app.exec_()
