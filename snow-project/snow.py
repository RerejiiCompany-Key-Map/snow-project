# coding=utf-8

import cv2
import dlib
import matplotlib.pyplot as plt
import scipy.misc
import sys

sys.path.append('../up_down_load')
sys.path.append('../face_detection')
import upload_client
import face

# -------------------------------
# ---------- CONSTANTS ----------
# -------------------------------
resize_rate = 2

predictor_path = './shape_predictor_68_face_landmarks.dat'
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)

OUT_FILE = 'out.png'



# -----------------------------
# ---------- METHODS ----------
# -----------------------------

def design_det1(img, rect):
    top, bottom, left, right = rect.top(), rect.bottom(), rect.left(), rect.right()
    cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), thickness=10)
    return img


def design_pre1(img, shape):
    """ サンプルのように顔の輪郭をそのまま表示 """
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


def decorate_predictor(img, design=design_pre1):
    try:
        # RGB変換 (opencv形式からskimage形式に変換)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # frontal_face_detectorクラスは矩形, スコア, サブ検出器の結果を返す
        dets, scores, idx = detector.run(img_rgb, 1)

        if len(dets) > 0:
            for i, rect in enumerate(dets):
                shape = predictor(img, rect)

                for shape_point_count in range(shape.num_parts):
                    shape_point = shape.part(shape_point_count)

                    img = design(img, shape)
        return img
    
    except:
        return img


def decorate_detector(img, design):
    try:
        # RGB変換 (opencv形式からskimage形式に変換)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # frontal_face_detectorクラスは矩形, スコア, サブ検出器の結果を返す
        dets, scores, idx = detector.run(img_rgb, 1)

        if len(dets) > 0:
            for i, rect in enumerate(dets):
                img = design_det1(img, rect)

        return img

    except:
        return img



# ----------------------------------
# ---------- MAIN METHODS ----------
# ----------------------------------

def main():
    ### カメラカプチャ
    cap = cv2.VideoCapture(0) # 0はデバイス番号
    while True:
        # retは画像取得成功フラグ
        ret, frame = cap.read()
        H, W = frame.shape[:2]


        # 鏡映り
        frame = frame[:, ::-1]

        # resize
        resize = cv2.resize(frame, (W//resize_rate,H//resize_rate))
        #img = frame.copy()

        # 顔検出 & デザイン
        out = decorate_predictor(img=resize, design=design_pre1)
        #out = decorate_detector(img=resize, design=design_det1)
        #out = face.facepredictor_dlib(resize)

        # フレームの表示
        cv2.imshow('camera capture', out)

        key = cv2.waitKey(100)
        if key != 255: # ボタンを押したら(?)
            break
    
    # キャプチャを解放する
    cap.release()
    cv2.destroyAllWindows()

    # 保存
    out = out[:, :, ::-1]
    scipy.misc.imsave(OUT_FILE, out)

    # 送信 & QRcode表示
    ID = upload_client.upload(OUT_FILE)
    upload_client.show_qrcode(ID)

    return



# --------------------------
# ---------- MAIN ----------
# --------------------------

if __name__ == '__main__':
    main()
