from flask import Flask, render_template, request, send_file, abort, make_response, redirect
import requests
import os, subprocess
import unicodedata
import time
import json, ast
import zipfile
from zipfile import ZipFile
import glob
from werkzeug.utils import secure_filename
import imgkit
from rarfile import RarFile
app= Flask(__name__)

uploads_dir = os.path.join(app.instance_path, 'uploads')
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)

@app.route('/')
def index():
    return render_template('converter.html')



@app.route('/upload', methods=['POST'])
def upload():
    os.system('rm *.zip')
    if request.method == 'POST':
        ziped = request.files['html']
        #unzip / unrar compressed file :
        if ziped.filename.endswith('.zip'):
            with zipfile.ZipFile(ziped, 'r') as zip_ref:
                zip_ref.extractall(uploads_dir)
        elif ziped.filename.endswith('.rar'):
            with RarFile(ziped) as file:
                    file.extractall(uploads_dir)
                    print(ziped.filename)
        else:
            return 'UNKNOWN FILE TYPE'
        
        count = 0
        print(uploads_dir)
        htmlPaths = []
        for root, dirs, files in os.walk(uploads_dir):
            for file in files:
                if file.endswith(".html"):
                    htmlPaths.append(os.path.join(root, file))
                    count += 1
        zipObj = ZipFile('{}'.format(ziped.filename), 'w')
        for path in htmlPaths:
            tmp = path.split('/')
            filename = tmp[-1]
            print(filename)
            os.system("google-chrome -headless --screenshot='./images/{}.png' --window-size=1920,10000 --default-background-color=0 {}".format(filename.split('.')[0], path))
            zipObj.write('./images/{}.png'.format(filename.split('.'))[0])
            count -= 1
            time.sleep(1)
        zipObj.close()
        os.system('rm -rf ./instance/uploads/* && rm -rf ./images/* '.format(ziped.filename))
    return send_file('./{}'.format(ziped.filename), as_attachment=True)

if __name__ == "__main__":
    app.run()