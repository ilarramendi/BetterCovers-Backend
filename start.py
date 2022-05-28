import pickle
import os
import json
from sys import path
from flask import jsonify, Flask, request, send_file, abort
import urllib

path.insert(1, './BetterCovers')
import src.functions

src.functions.logFile = './workdir/logs.log'
src.functions.logLevel = 10

items = {}
with open('./BetterCovers/config/metadata.pickle', 'rb') as file:
    items = pickle.load(file)['items']
app = Flask(__name__)

@app.route("/getImage")
def summary():
    js = request.args
    if js['folder'] in items:
        metadata = items[urllib.parse.unquote(js['folder'])]
        if metadata.type != 'episode':
            if src.functions.process(
                        metadata,
                        {'template': urllib.parse.unquote(js['template']), 'out': []},
                        'web',
                        os.path.abspath('./workdir'),
                        "/usr/bin/wkhtmltoimage",
                        urllib.parse.unquote(js['image']),
                        urllib.parse.unquote(js['languagesOrder'])
                    ):
                return send_file('./workdir/threads/web.jpg')
            else: abort(501)
app.run(host="0.0.0.0")