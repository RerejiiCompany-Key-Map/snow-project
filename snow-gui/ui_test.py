# coding=utf-8

import sys
import cv2

from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QGroupBox, QVBoxLayout, QHBoxLayout,
    QPushButton, QCheckBox,
    QGraphicsView, QGraphicsScene, QGraphicsItem)
from PyQt5.QtCore import QCoreApplication

# -------------------------------
# ---------- CONSTANTS ----------
# -------------------------------



# -------------------------------
# ---------- VARIABLES ----------
# -------------------------------
a = 10
loop = True



# -----------------------------
# ---------- CLASSES ----------
# -----------------------------
class SnowWindow():
    ...



# -----------------------------
# ---------- METHODS ----------
# -----------------------------




# ----------------------------------
# ---------- MAIN METHODS ----------
# ----------------------------------
def main():
    """ UI """
    ### camera
    # カメラキャプチャ
    cap = cv2.VideoCapture(0) # 0はデバイス番号
    loop = True
    # 映像 (start)
    def disp():
        while loop:
            # retは画像取得成功フラグ
            if cap is None: return
            ret, frame = cap.read()
            if ret is False: return
            H, W = frame.shape[:2]

            # フレームの表示
            cv2.imshow('snow', frame)

            key = cv2.waitKey(100)
        cv2.destroyAllWindows()
    # finish
    def take():
        ...
    def finish():
        global loop
        loop = False
        QCoreApplication.instance().quit()
        #cap.release()
        #sys.exit(app.exec_())


    ### UI
    app = QApplication(sys.argv)
    window = QWidget()
    vbox_window = QHBoxLayout()   # window layout
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
    btn00.clicked.connect(disp)
    btn01.clicked.connect(take)
    btn04.clicked.connect(finish)
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


def main2():
    return



# --------------------------
# ---------- MAIN ----------
# --------------------------

if __name__ == '__main__':
    #main()
    main2()
