from flask import Flask, render_template, request, send_file, abort, make_response, redirect
import requests
import os, subprocess
import unicodedata
import time
import json, ast
import zipfile
from zipfile import ZipFile
import uuid
from werkzeug.utils import secure_filename
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
    localUuid = uuid.uuid1()
    print(localUuid)
    os.system('rm *.zip')
    print(request.method)
    render_template('converters.html')
    if request.method == 'POST':
        print(request.files)
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
            filename = filename.split('.')[0]
            #cutycapt --url=file:/home/kali/HTML-to-image/HTML-to-PNG-converter-/instance/uploads/web_game/html/index.html --out=./outfilep.png --min-width=1920 --min-height=10000 //  ana l path
            os.system("cutycapt --url=file:{} --out=./images/{}.png --min-width=1920 --min-height=10000".format(path, filename.split('.')[0]))
            zipObj.write('./images/{}.png'.format(filename))
            count -= 1
            time.sleep(1)
        zipObj.close()
        os.system('rm -rf ./instance/uploads/* && rm -rf ./images/* '.format(ziped.filename))
    return send_file('./{}'.format(ziped.filename), as_attachment=True)

if __name__ == "__main__":
    app.run()