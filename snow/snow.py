# coding-utf-8

import sys
import numpy as np
import scipy.misc
import psutil

import cv2
import dlib
from tkinter import (
    Tk,
    BooleanVar, StringVar,
    LabelFrame, Button, Checkbutton, Label
)

sys.path.append('../up_down_load')
import upload_client

# -------------------------------
# ---------- CONSTANTS ----------
# -------------------------------
FRAME_WIDTH, FRAME_HEIGHT = 400, 300
INTERVAL = 20

BTN_TEXTS = ["start", "take", "send", "clear", "finish"]
CHECK_TEXTS = [
    "KUT logo", "krlab logo",
    "detected face rectangle", "detected face predictor",
]
CHECK_INIT = [
    True, True,
    False, True,
]

# load KUT logo
a = cv2.imread('./data/KUT_logo.png', cv2.IMREAD_UNCHANGED)
h, w = a.shape[:2]
w_ = FRAME_WIDTH/4
h_ = h * (w_/w)
KUT_W, KUT_H = int(w_), int(h_)
KUT_LOGO = cv2.resize(a, (KUT_W, KUT_H))
KUT_MASK = KUT_LOGO[:, :, 3] # アルファチャンネルだけを抜き出す
KUT_MASK = cv2.cvtColor(KUT_MASK, cv2.COLOR_GRAY2BGR) # 3色分に増やす
KUT_MASK = KUT_MASK / 255.0 # 0-255 -> 0.0-0.1
KUT_LOGO = KUT_LOGO[:, :, :3] # アルファチャンネル除去

# load krlab logo
a = cv2.imread('./data/krlab_logo.png', cv2.IMREAD_UNCHANGED)
h, w = a.shape[:2]
w_ = FRAME_WIDTH/3
h_ = h * (w_/w)
KRLAB_W, KRLAB_H = int(w_), int(h_)
KRLAB_LOGO = cv2.resize(a, (KRLAB_W, KRLAB_H))
KRLAB_MASK = KRLAB_LOGO[:, :, 3] # アルファチャンネルだけを抜き出す
KRLAB_MASK = cv2.cvtColor(KRLAB_MASK, cv2.COLOR_GRAY2BGR) # 3色分に増やす
KRLAB_MASK = KRLAB_MASK / 255.0 # 0-255 -> 0.0-0.1
KRLAB_LOGO = KRLAB_LOGO[:, :, :3] # アルファチャンネル除去
del a, h, w, w_, h_

# dlib
predictor_path = './data/shape_predictor_68_face_landmarks.dat'
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)

# Button states
BTN_STATES = [
    None,
    [0, 1, 0, 0, 1],    # start
    [1, 0, 1, 1, 1],    # take(stop)
    [0, 0, 0, 1, 1],    # send
    [1, 0, 0, 1, 1],    # clear(same init)
    None                # finish
]
BTN_STATE_INIT, BTN_STATE_START, BTN_STATE_TAKE, BTN_STATE_SEND, BTN_STATE_CLEAR = 4, 1, 2, 3, 4

# OUTPUT FILE
OUT_FILE = 'out.png'



# -------------------------------
# ---------- VARIABLES ----------
# -------------------------------
root = None     # main window
cap = None      # video capture
loop = False    # loop capture

frame = None
IDvar = None

# basic operation buttons
BOBs = []

checked_boolvars = []



# -----------------------------
# ---------- METHODS ----------
# -----------------------------
### Design
def kutlogo(img):
    o = 20
    img[o:o+KUT_H, o:o+KUT_W] = (img[o:o+KUT_H, o:o+KUT_W] * (1 - KUT_MASK)) // 1 # 透過率に応じて元の画像を暗くする
    img[o:o+KUT_H, o:o+KUT_W] = (img[o:o+KUT_H, o:o+KUT_W] + KUT_LOGO * KUT_MASK) // 1 # 貼り付ける方の画像に透過率をかけて加算
    return img

def krlablogo(img):
    o = 20
    img[-KRLAB_H-o:-o, -KRLAB_W-o:-o] = (img[-KRLAB_H-o:-o, -KRLAB_W-o:-o] * (1 - KRLAB_MASK)) // 1
    img[-KRLAB_H-o:-o, -KRLAB_W-o:-o] = (img[-KRLAB_H-o:-o, -KRLAB_W-o:-o] + KRLAB_LOGO * KRLAB_MASK) // 1
    return img

def detected_rectangle(img, dets):
    for rect in dets:
        top, bottom, left, right = rect.top(), rect.bottom(), rect.left(), rect.right()
        cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), thickness=10)
    return img

def mark_predictor(img, shapes):
    """ サンプルのように顔の輪郭をそのまま表示 """
    for shape in shapes:
        for shape_point_count in range(shape.num_parts):
            shape_point = shape.part(shape_point_count)

            if shape_point_count < 17: # [0-16]:輪郭
                cv2.circle(img, (shape_point.x, shape_point.y), 2, (0, 0, 255), -1)
            elif shape_point_count < 22: # [17-21]眉（右）
                cv2.circle(img, (shape_point.x, shape_point.y), 2, (0, 255, 0), -1)
            elif shape_point_count < 27: # [22-26]眉（左）
                cv2.circle(img, (shape_point.x, shape_point.y), 2, (255, 0, 0), -1)
            elif shape_point_count < 31: # [27-30]鼻背
                cv2.circle(img, (shape_point.x, shape_point.y), 2, (0, 255, 255), -1)
            elif shape_point_count < 36: # [31-35]鼻翼、鼻尖
                cv2.circle(img, (shape_point.x, shape_point.y), 2, (255, 255, 0), -1)
            elif shape_point_count < 42: # [36-4142目47）
                cv2.circle(img, (shape_point.x, shape_point.y), 2, (255, 0, 255), -1)
            elif shape_point_count < 48: # [42-47]目（左）
                cv2.circle(img, (shape_point.x, shape_point.y), 2, (0, 0, 128), -1)
            elif shape_point_count < 55: # [48-54]上唇（上側輪郭）
                cv2.circle(img, (shape_point.x, shape_point.y), 2, (0, 128, 0), -1)
            elif shape_point_count < 60: # [54-59]下唇（下側輪郭）
                cv2.circle(img, (shape_point.x, shape_point.y), 2, (128, 0, 0), -1)
            elif shape_point_count < 65: # [60-64]上唇（下側輪郭）
                cv2.circle(img, (shape_point.x, shape_point.y), 2, (0, 128, 255), -1)
            elif shape_point_count < 68: # [65-67]下唇（上側輪郭）
                cv2.circle(img, (shape_point.x, shape_point.y), 2, (128, 255, 0), -1)
    return img


### Button Actions
def start():
    global loop
    loop = True
    btn_state(BTN_STATE_START)
    display()

def display():
    global root, cap, loop, frame
    # load capture
    ret, frame = cap.read()

    frame = frame[:, ::-1, :] # x方向鏡映

    # detect face
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # RGB変換 (opencv形式からskimage形式に変換)
    dets, scores, idx = detector.run(img_rgb, 1) # frontal_face_detectorクラスは矩形, スコア, サブ検出器の結果を返す
    shapes = [predictor(img_rgb, rect) for rect in dets]

    # design
    if checked_boolvars[0].get():
        frame = kutlogo(frame)
    if checked_boolvars[1].get():
        frame = krlablogo(frame)
    if checked_boolvars[2].get():
        frame = detected_rectangle(frame.copy(), dets)
    if checked_boolvars[3].get():
        frame = mark_predictor(frame.copy(), shapes)

    # show image
    cv2.imshow('camera', frame)
    # loop
    if loop:
        root.after(INTERVAL, display)

def stop():
    global loop
    loop = False
    btn_state(BTN_STATE_TAKE)

def send():
    global frame
    btn_state(BTN_STATE_SEND)
    # 保存
    out = frame[:, :, ::-1]
    scipy.misc.imsave(OUT_FILE, out)
    # 送信 & QRcode表示
    ID = upload_client.upload(OUT_FILE)
    IDvar.set(ID)
    upload_client.show_qrcode(ID).show()

def clear():
    btn_state(BTN_STATE_CLEAR)
    cv2.destroyAllWindows()
    IDvar.set("")
    for proc in psutil.process_iter():
        if proc.name() == "Preview":
            proc.kill()

def finish():
    cap.release()
    cv2.destroyAllWindows()
    for proc in psutil.process_iter():
        if proc.name() == "Preview":
            proc.kill()
    sys.exit(1)


### Button state
def btn_state(n=4):
    """ n = 
        //* 0 : init
        * 1 : start
        * 2 : take
        * 3 : send
        * 4 : clear (init)
        //* 5 : finish
    """
    a = ['disable', 'normal']

    states = BTN_STATES[n]
    for i, s in enumerate(states):
        BOBs[i]['state'] = a[s]



# ----------------------------------
# ---------- MAIN METHODS ----------
# ----------------------------------

# --------------------------
# ---------- MAIN ----------
# --------------------------

### カメラキャプチャ
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

### Main Frame
root = Tk()
root.title("krlab snow")
#root.geometry("300x300")

### 基本操作 (basic operation)
frame1 = LabelFrame(root, bd=2, relief='ridge', text='Basic operation')
frame1.pack(fill='x', padx=10, pady=10)
BTN_FUNCS = [start, stop, send, clear, finish]
for (text, func) in zip(BTN_TEXTS, BTN_FUNCS):
    b = Button(frame1, text=text, command=func)
    b.pack(fill='x', padx=4, pady=2)
    BOBs.append(b)

### 詳細設定 (advanced setting)
frame2 = LabelFrame(root, bd=2, relief='ridge', text='Advanced setting')
frame2.pack(fill='x', padx=10, pady=10)
for (text, ini) in zip(CHECK_TEXTS, CHECK_INIT):
    val = BooleanVar()
    val.set(ini)
    checked_boolvars.append(val)
    Checkbutton(frame2, text=text, variable=val).pack(anchor='w', padx=4, pady=2)
#Button(frame2, text="set", command=set).pack(side='right', padx=4, pady=2)

### ID表示
frame3 = LabelFrame(root, bd=2, relief='ridge', text='ID')
frame3.pack(fill='x', padx=10, pady=10)
IDvar = StringVar()
IDvar.set("")
Label(frame3, textvariable=IDvar).pack()

btn_state(BTN_STATE_INIT)

root.mainloop()
