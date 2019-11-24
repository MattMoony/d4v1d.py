import os
import json
import pystache
from flask import Flask, send_file, send_from_directory, abort

# GLOBAL CONSTANTS ------------------------- #

HOSTNAME    = 'localhost'
PORT        = 8080

# ------------------------------------------ #

def get_crawled(base_path):
    return [d for d in os.listdir(os.path.join(base_path, 'results')) if os.path.isdir(os.path.join(base_path, 'results', d))]

def init(base_path):
    app = Flask(__name__, static_url_path='')

    @app.route('/')
    def index():
        us = get_crawled(base_path)
        with open(os.path.join(base_path, 'web', 'index.html'), 'r') as f:
            return pystache.render(f.read(), dict(u_count=len(us), users=map(lambda u: dict(name=u), us)))

    @app.route('/view/<string:uname>')
    def view(uname):
        jpath = os.path.join(base_path, 'results', uname, uname+'.json')
        if not os.path.isfile(jpath):
            abort(404)
        with open(os.path.join(base_path, 'web', 'view.html'), 'r') as f:
            with open(jpath, 'r') as j:
                print(jpath)
                return pystache.render(f.read(), dict(uname=uname, raw_json=j.read()))

    @app.route('/style/<path:fname>')
    def style(fname):
        return send_from_directory(os.path.join(base_path, 'web', 'style'), fname)

    @app.route('/script/<path:fname>')
    def script(fname):
        return send_from_directory(os.path.join(base_path, 'web', 'script'), fname)

    app.run(host=HOSTNAME, port=PORT)

if __name__ == '__main__':
    init(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))