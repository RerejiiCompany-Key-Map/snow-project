# encoding=utf-8

import sys
import cv2
import threading
import time
from subprocess import Popen

from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow,
    QGroupBox, QVBoxLayout, QHBoxLayout,
    QPushButton, QCheckBox
)
from PyQt5.QtCore import QCoreApplication

# -------------------------------
# ---------- CONSTANTS ----------
# -------------------------------
FRAME_WIDTH, FRAME_HEIGHT = 400, 300

CMD = 'python snow.py 1'



# -------------------------------
# ---------- VARIABLES ----------
# -------------------------------
proc = None



# -----------------------------
# ---------- METHODS ----------
# -----------------------------
def UI_start():
    global proc
    proc = Popen(CMD, shell=True)



# ----------------------------------
# ---------- MAIN METHODS ----------
# ----------------------------------
def UI():
    """ UI """
    app = QApplication(sys.argv)
    window = QWidget()
    vbox_window = QVBoxLayout()   # window layout
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
    # set
    for btn in [btn00, btn01, btn02, btn03, btn04]: vbox0.addWidget(btn) # add button to layout
    groupbox0.setLayout(vbox0) # set layout to group
    vbox_window.addWidget(groupbox0) # set group to window layout

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
    vbox_window.addWidget(groupbox1) # set groupt o window layout

    ### 表示 & 終了
    window.show()
    sys.exit(app.exec_())


def camera():
    cap = cv2.VidepCapture(0)

    while 



# --------------------------
# ---------- MAIN ----------
# --------------------------
if __name__ == '__main__':
    n = 0
    if len(sys.argv):
        try: 
            n = int(sys.argv[1])
        except:
            pass
    FUNC_ARRAY = [
        UI,
    ]
    FUNC_ARRAY[n]()
