from keras.models import load_model
from PIL import Image, ImageOps
import cv2
import numpy as np
import glob
from flask import Flask, render_template, Response, url_for, redirect
import os

app = Flask(__name__)

class AI():
    def __init__(self):
        self.model_dic = {"鳥居": "torii.h5",
                          "森島": "morishima.h5",
                          "偏ったAI": "bias.h5"}

        self.file_dic = {
            "モナリザ": "monarisa.jpg",
            "ガスマスク": "gasmask.jpg",
            "スケキヨ": "sukekiyo.jpg",
            "男塾死天王 卍丸": "manjimaru.jpg",
            "蛇柱 伊黒小芭内": "hebi.jpg",
            "歯を見せて笑う": "tooth.jpg",
            "おでこに冷えピタ": "hiepita.jpg",
            "大坂なおみ": "naomi.jpg",
            "口が印刷されたマスク": "smile.jpg",
            "あごマスク": "ago.jpg",
            "普通のマスクだが横向き": "mask_yoko.jpg",
            "透明マスク": "toumei.jpg",
            "口が四角い": "sikaku.jpg",
            "千の顔を持つ男 ミル・マスカラス": "maskman.jpg",
            "初代タイガーマスク": "tiger.jpg",
            "大口を開けて食べる": "cake.jpg",
            }


        path = ".\\static\\images\\"
        self.cnt = len(self.file_dic)
        self.page = 0
        self.files = []
        self.titles = []
        self.players = []
        self.results = []

        for key, value in self.file_dic.items():
            self.titles.append(key)
            self.files.append(value)

        for key, item in self.model_dic.items():
            self.players.append(key)
            model = load_model(item)
            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
            man_result = []

            for i, file in enumerate(self.files):
                image = Image.open(path + file)
                size = (224, 224)
                image = ImageOps.fit(image, size, Image.ANTIALIAS)

                image_array = np.asarray(image)
                normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
                data[0] = normalized_image_array

                prediction = model.predict(data)
                pred_mask = float(f"{prediction[0][0]:.5f}")*100
                pred_no_mask = float(f"{prediction[0][1]:.5f}")*100

                man_result.append([pred_mask, pred_no_mask])
            self.results.append(man_result)
        
        print(self.results)

@app.route("/index")
def result0():
    return render_template("result.html", titles=ai.titles, files=ai.files, results=ai.results)

@app.route("/")
def result():
    page = ai.page + 1
    title = ai.titles[ai.page]
    file = ai.files[ai.page]
    players = ai.players
    cnt = len(players)

    results = []
    for i in range(cnt):
        results.append(ai.results[i][ai.page])
    return render_template("result.html", page=page, cnt=cnt, title=title, players=players, file=file, results=results)

@app.route("/nextpage")
def nextpage():
    ai.page = ai.page+1 if ai.page < ai.cnt-1 else 0
    return redirect(url_for("result"))

@app.route("/prevpage")
def prevpage():
    ai.page = ai.page-1 if ai.page > 0 else ai.cnt-1
    return redirect(url_for("result"))


ai = AI()
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")