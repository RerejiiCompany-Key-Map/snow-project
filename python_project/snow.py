# -*- coding: utf-8 -*-
import cv2

def capture_camera(mirror=True, size=None):
    """Capture video from camera"""
    # カメラをキャプチャする
    cap = cv2.VideoCapture(0) # 0はカメラのデバイス番号
    #HAAR分類器の顔検出用の特徴量
    cascade_path = "haarcascade_frontalface_alt.xml"
    color = (255, 255, 255) #白
    #カスケード分類器の特徴量を取得する
    cascade = cv2.CascadeClassifier(cascade_path)

    while True:
        count = 0 #参照フレームのカウント
        # retは画像を取得成功フラグ
        ret, frame = cap.read()

        # 鏡のように映るか否か
        if mirror is True:
            frame = frame[:,::-1]

        # フレームをリサイズ
        # sizeは例えば(800, 600)
        if size is not None and len(size) == 2:
            frame = cv2.resize(frame, size)

        #if count == 10 or count == 0: # 参照フレーム軽減
        if True:
            ret, frame = cap.read() # ここで参照しないとバグる
            #グレースケール変換
            image_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #物体認識（顔認識）の実行
            facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=1, minSize=(1, 1))
            count = 1
        else:
            count = count + 1

        if len(facerect) > 0:
            #検出した顔を囲む矩形の作成
            print ("face rectangle")
            print (facerect)
            for rect in facerect:
                cv2.rectangle(frame, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), color, thickness=2)
                print('check')

        # フレームを表示する
        cv2.imshow('camera capture', frame)

        k = cv2.waitKey(1) # 1msec待つ

        if k == 13: # Enterキーで保存
            cv2.imwrite("test.png", frame)

        if k == 27: # ESCキーで終了
            break

    # キャプチャを解放する
    cap.release()
    cv2.destroyAllWindows()

capture_camera()
