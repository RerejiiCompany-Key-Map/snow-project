# encoding=utf-8

import sys
import cv2
import threading
import time

from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow,
    QGroupBox, QVBoxLayout, QHBoxLayout,
    QPushButton, QCheckBox
)
from PyQt5.QtCore import QCoreApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# -------------------------------
# ---------- CONSTANTS ----------
# -------------------------------
FRAME_WIDTH, FRAME_HEIGHT = 400, 300
DIR = ['right', 'left', 'top', 'bottom']

# -------------------------------
# ---------- VARIABLES ----------
# -------------------------------
#capture_thread = None
loop = False
cap = None
m = None

# -----------------------------
# ---------- METHODS ----------
# -----------------------------
def start():
    global loop, capture
    loop = True
    capture_thread = threading.Thread(target=capture)
    capture_thread.start()

def stop():
    global loop
    loop = False

def finish():
    global loop
    loop = False
    QCoreApplication.instance().quit()


def capture():
    global loop
    while loop:
        m.imshow()
        time.sleep(0.01)

# -----------------------------
# ---------- CLASSES ----------
# -----------------------------
class ImshowCanvas(FigureCanvas):

    def __init__(self, parent=None, width=FRAME_WIDTH//100, height=FRAME_HEIGHT//100):
        fig = Figure(figsize=(width, height))
        fig.subplots_adjust(wspace=0, hspace=0)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        self.figure.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)
        self.ax = self.figure.add_subplot(111)
        for dir in DIR: self.ax.spines[dir].set_visible(False)
        self.ax.set_xticks([])
        self.ax.set_yticks([])

        """
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        """
        #self.imshow()
    
    def imshow(self):
        global cap
        ret, frame = cap.read()
        self.ax.imshow(frame[:, ::-1, ::-1])
        self.draw()


# --------------------------
# ---------- MAIN ----------
# --------------------------
### thread


### camera
# カメラキャプチャ
cap = cv2.VideoCapture(0) # 0はデバイス番号
cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

### UI
app = QApplication(sys.argv)
window = QWidget()
vbox_window = QHBoxLayout()   # window layout
groupbox_op = QGroupBox()     # operation group
vbox_op = QVBoxLayout()       # operation layout
groupbox_op.setLayout(vbox_op)
window.setLayout(vbox_window) # set layout to window

# MARK: #0
### 基本操作グループ (basic operation)
groupbox0 = QGroupBox('Basic operation')
vbox0 = QVBoxLayout() # 縦方向に並べる
# content
btn00 = QPushButton('start')  # start
btn01 = QPushButton('take')   # take a picture
btn02 = QPushButton('clear')  # clear data
btn03 = QPushButton('send')   # send picture to server
btn04 = QPushButton('finish') # finish app
btn00.clicked.connect(start)
btn01.clicked.connect(stop)
btn04.clicked.connect(finish)
# set
for btn in [btn00, btn01, btn02, btn03, btn04]: vbox0.addWidget(btn) # add button to layout
groupbox0.setLayout(vbox0) # set layout to group
vbox_op.addWidget(groupbox0) # set group to window layout

# MARK: #1
### 詳細設定 (Advanced setting)
groupbox1 = QGroupBox('Advanced setting (dislpay)')
vbox1 = QVBoxLayout() # 縦方向に並べる
# content
check00 = QCheckBox('KUT logo')
check01 = QCheckBox('krlab logo')
check02 = QCheckBox('detected face predictor')
check03 = QCheckBox('detected face rectangle')
# set
for check in [check00, check01, check02, check03]: vbox1.addWidget(check) # add check to layout
groupbox1.setLayout(vbox1) # set layout to gruop
vbox_op.addWidget(groupbox1) # set groupt o window layout

# MARK: #2
m = ImshowCanvas(window)
vbox_window.addWidget(m)
vbox_window.addWidget(groupbox_op)

### 表示 & 終了
window.show()
#capture_thread.start()
sys.exit(app.exec_())

