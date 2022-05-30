import urllib
import re
import random
import pickle
import os
import json
from time import sleep
from sys import path
from flask import jsonify, Flask, request, send_file, abort, redirect

import logging

import base64
#log = logging.getLogger('werkzeug')
#log.setLevel(logging.ERROR)

# TODO remove files created by /.g

path.insert(1, './BetterCovers')
import src.functions

src.functions.imageCache = os.path.abspath('BetterCovers/config/cache/imageCache')
src.functions.logFile = 'BetterCovers/config/logs//web.log'
src.functions.logLevel = 10

items = {}
with open('./BetterCovers/config/metadata.pickle', 'rb') as file:
    items = pickle.load(file)['items']
app = Flask(__name__)

@app.route("/imageCache/<url>")
def downloadImage(url):
    if src.functions.getImage(url.rpartition('.')[0]):
        return redirect(f"http://192.168.1.71:3333/static/cache/imageCache/{url}") # Redirect AGAIN to nginx for speeeeed babyyyyy (the more functionality in nginx the better)
    else: return abort(403)

@app.route("/getImage")
def getImage():
    js = request.args
    if js['folder'] in items:
        metadata = items[urllib.parse.unquote(js['folder'])]
        thread = str(random.randint(0, 99999))
        if metadata.type != 'episode':
            if src.functions.process(
                metadata,
                {'template': urllib.parse.unquote(js['template']), 'out': []},
                thread,
                os.path.abspath('BetterCovers/config'),
                "/usr/bin/wkhtmltoimage",
                src.functions.getImage(base64.b64encode(urllib.parse.unquote(js['image']).encode('ascii'))),
                urllib.parse.unquote(js['languagesOrder'])
            ): return send_file(f'BetterCovers/config/threads/{thread}.jpg')
            else: abort(501)

app.run(host="0.0.0.0")