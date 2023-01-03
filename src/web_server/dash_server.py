import os
import random
import glob
import sys
import binascii
import argparse
from flask import Flask, request, render_template, send_from_directory
from flask_cors import CORS, cross_origin
import flask.scaffold  # hack for flask_restful
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask_restful import Resource, Api
from json import dumps
from flask import jsonify

app = Flask(__name__)
api = Api(app)

app.config['IMAGE_EXTS'] = [".png", ".jpg", ".jpeg", ".gif", ".tiff"]

CORS(app)

def encode(x):
    return binascii.hexlify(x.encode('utf-8')).decode()

def decode(x):
    return binascii.unhexlify(x.encode('utf-8')).decode()

def random_image():
    """
    Return a random image from the ones in the static/ directory
    """
    img_dir = "./static/map-images"
    img_list = os.listdir(img_dir)
    return random.choice(img_list)

@app.route("/")
def home():
    root_dir = "./static/map-images" #app.config['ROOT_DIR']
    image_paths = []
    for root,dirs,files in os.walk(root_dir):
        for file in files:
            if any(file.endswith(ext) for ext in app.config['IMAGE_EXTS']):
                image_paths.append(encode(os.path.join(root,file)))
    return render_template('index.html', paths=image_paths)

@app.route('/cdn/<path:filepath>')
def download_file(filepath):
    dir,filename = os.path.split(decode(filepath))
    return send_from_directory(dir, filename, as_attachment=False)

@app.route('/add')
def add():
    # Checking that both parameters have been supplied
    for param in ['x', 'y']:
        if not param in request.args:
            result = { 
                'type': '%s value is missing' % param, 
                'content': '', 
                'status': 'REQUEST_DENIED'
            }
            return jsonify(result)
    
    # Make sure they are numbers too
    try:
        x = float(request.args['x'])
        y = float(request.args['y'])
    except:
        return "x and y should be numbers"
    
    result = { 
        'type': 'result', 
        'content': x+y, 
        'status': 'REQUEST_OK'
    }   
    return jsonify(result)

@app.route('/image')
def myapp():
    image = random_image()
    #print('generated url: ', flask.url_for('static/images', filename=random_image))
    return render_template('img_test.html', random_image=image)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Usage: %prog [options]')
    parser.add_argument('root_dir', help='Gallery root directory path')
    parser.add_argument('-l', '--listen', dest='host', default='127.0.0.1', \
                                    help='address to listen on [127.0.0.1]')
    parser.add_argument('-p', '--port', metavar='PORT', dest='port', type=int, \
                                default=5000, help='port to listen on [5000]')
    args = parser.parse_args()
    app.config['ROOT_DIR'] = 'static/map-images' #args.root_dir
    app.run(host=args.host, port=args.port, debug=True)
  #app.run(debug=True, port=5002)