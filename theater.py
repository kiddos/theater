from flask import Flask, render_template, send_from_directory, send_file
from flask import stream_with_context
from flask import request, Response
from helper import list_movies
import os
import json
import re


# setup json config
config_path = 'config.json'
if not os.path.isfile(config_path):
  config = {
    'movie_path': 'D:\\Movie'
  }
  with open(config_path, 'w') as f:
    json.dump(config, f)
else:
  with open(config_path, 'r') as f:
    config = json.load(f)

movies = {}
list_movies(config['movie_path'], movies)
app = Flask(__name__)

# routing
@app.route('/')
def index():
  return render_template('index.html', movies=movies)

@app.route('/js/<path:path>')
def js(path):
  return send_from_directory('js', path)

@app.route('/css/<path:path>')
def css(path):
  return send_from_directory('css', path)

@app.route('/movie/<path:movie>')
def movie(movie):
  range_header = request.headers.get('Range', None)
  if not range_header:
    return send_file(movies[movie])

  total_size = os.path.getsize(movies[movie])
  match = re.search('(\d+)-(\d*)', range_header)
  g = match.groups()
  byte1 = 0
  byte2 = None
  if g[0]: byte1 = int(g[0])
  if g[1]: byte2 = int(g[1])

  length = total_size - byte1
  if byte2 is not None:
    length = byte2 - byte1

  data = None
  with open(movies[movie], 'rb') as f:
    f.seek(byte1)
    data = f.read(length)
  res = Response(data, 206, mimetype='video/mp4', direct_passthrough=True)
  res.headers.add('Content-Range', 'bytes %d-%d/%d' %
      (byte1, byte1 + length - 1, total_size))
  return res

@app.route('/icons/<path:image>')
def images(image):
  return send_from_directory('icons', image)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)
