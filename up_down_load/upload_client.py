# coding=utf-8

import requests
import qrcode

# -------------------------------
# ---------- CONSTANTS ----------
# -------------------------------

filename = './data/google.png'
UPLOAD_URL = 'http://krlab.info.kochi-tech.ac.jp/~matsumoto/snow_project/upload_server.php'
#DOWNLOAD_URL = 'http://krlab.info.kochi-tech.ac.jp/~matsumoto/snow_project/'
#UPLOAD_URL = 'http://krlab.info.kochi-tech.ac.jp/snow_project/upload_server.php'
DOWNLOAD_URL = 'http://krlab.info.kochi-tech.ac.jp/snow_project/'



# ----------------------------
# ---------- METHODS ----------
# ----------------------------

# 画像のアップロードと画像IDの取得
def upload(filename):
    imgdata = open(filename, 'rb')
    files = {'img' : ('output.png', imgdata, 'image/png')}
    #files = {'img':imgdata}
    r = requests.post(UPLOAD_URL, files=files)

    return r.text


# 画像ダウンロードページのQR codeの表示
def show_qrcode(ID):
    img = qrcode.make(DOWNLOAD_URL + '?id=' + ID)

    # OS の Viewer を使用 (Mac だと Preview.app)
    img.show()






# --------------------------
# ---------- MAIN ----------
# --------------------------

if __name__ == '__main__':
    ID = upload(filename=filename)
    show_qrcode(ID)

