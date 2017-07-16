# coding=utf-8

import cv2
import dlib
import sys


# -------------------------------
# ---------- CONSTANTS ----------
# -------------------------------
H, W = 900, 1600
predictor_path = './shape_predictor_68_face_landmarks.dat'

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)

resize_rate = 1

# -----------------------------
# ---------- METHODS ----------
# -----------------------------

def facedetector_dlib(img):
    try:
        # RGB変換 (opencv形式からskimage形式に変換)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # frontal_face_detectorクラスは矩形, スコア, サブ検出器の結果を返す
        dets, scores, idx = detector.run(img_rgb, 1)
        # 矩形の色
        color = (0, 0, 255)
        s = ''
        if len(dets) > 0:
            # 顔画像ありと判断された場合
            for i, rect in enumerate(dets):
                # detsが矩形, scoreはスコア, idxはサブ検出器の結果 (0.0がメインで数が大きい程弱い)
                # print rect, scores[i], idx[i]
                top, bottom, left, right = rect.top(), rect.bottom(), rect.left(), rect.right()
                cv2.rectangle(img, (left, top), (right, bottom), color, thickness=10)
                s += 'top, bottom, left, right = %d %d %d %d (score : %f)' % (top, bottom, left, right, scores[i])
        # 矩形が書き込まれた画像と s = 'x1 y1 x2 y2 x1 y1 x2 y2 (file_name)'
        # 顔が無ければ s = '' が返る
        return img, s
    except:
        # メモリエラーの時など
        return img, ""


def facepredictor_dlib(img):
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

                    if shape_point_count < 17: # [0-16]:輪郭
                        cv2.circle(img, (int(shape_point.x * resize_rate), int(shape_point.y * resize_rate)), 2, (0, 0, 255), -1)
                    elif shape_point_count < 22: # [17-21]眉（右）
                        cv2.circle(img, (int(shape_point.x * resize_rate), int(shape_point.y * resize_rate)), 2, (0, 255, 0), -1)
                    elif shape_point_count < 27: # [22-26]眉（左）
                        cv2.circle(img, (int(shape_point.x * resize_rate), int(shape_point.y * resize_rate)), 2, (255, 0, 0), -1)
                    elif shape_point_count < 31: # [27-30]鼻背
                        cv2.circle(img, (int(shape_point.x * resize_rate), int(shape_point.y * resize_rate)), 2, (0, 255, 255), -1)
                    elif shape_point_count < 36: # [31-35]鼻翼、鼻尖
                        cv2.circle(img, (int(shape_point.x * resize_rate), int(shape_point.y * resize_rate)), 2, (255, 255, 0), -1)
                    elif shape_point_count < 42: # [36-4142目47）
                        cv2.circle(img, (int(shape_point.x * resize_rate), int(shape_point.y * resize_rate)), 2, (255, 0, 255), -1)
                    elif shape_point_count < 48: # [42-47]目（左）
                        cv2.circle(img, (int(shape_point.x * resize_rate), int(shape_point.y * resize_rate)), 2, (0, 0, 128), -1)
                    elif shape_point_count < 55: # [48-54]上唇（上側輪郭）
                        cv2.circle(img, (int(shape_point.x * resize_rate), int(shape_point.y * resize_rate)), 2, (0, 128, 0), -1)
                    elif shape_point_count < 60: # [54-59]下唇（下側輪郭）
                        cv2.circle(img, (int(shape_point.x * resize_rate), int(shape_point.y * resize_rate)), 2, (128, 0, 0), -1)
                    elif shape_point_count < 65: # [60-64]上唇（下側輪郭）
                        cv2.circle(img, (int(shape_point.x * resize_rate), int(shape_point.y * resize_rate)), 2, (0, 128, 255), -1)
                    elif shape_point_count < 68: # [65-67]下唇（上側輪郭）
                        cv2.circle(img, (int(shape_point.x * resize_rate), int(shape_point.y * resize_rate)), 2, (128, 255, 0), -1)
        return img
    
    except:
        return img




# ----------------------------------
# ---------- MAIN METHODS ----------
# ----------------------------------

def test1():
    ### カメラカプチャ
    cap = cv2.VideoCapture(0) # 0はデバイス番号

    while True:
        # retは画像取得成功フラグ
        ret, frame = cap.read()

        # 鏡映り
        frame = frame[:, ::-1]

        # resize
        frame = cv2.resize(frame, (W//4,H//4))

        # 顔検出
        """
        frame, s = facedetector_dlib(frame)
        print(s)
        """
        frame = facepredictor_dlib(frame)

        # フレームの表示
        cv2.imshow('camera capture', frame)

        key = cv2.waitKey(1)
        if key == 27: # ESCキーで終了
            break
    
    # キャプチャを解放する
    cap.release()
    cv2.destroyAllWindows()



def test2():
    img = cv2.imread('data/Lenna.png')
    img, s = facedetector_dlib(img)

    cv2.imshow('img', img)
    print(s)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



# --------------------------
# ---------- MAIN ----------
# --------------------------

if __name__ == '__main__':
    n = 1
    if len(sys.argv) > 1:
        n = int(sys.argv[1])

    exec("test%d()" % n)
