from flask import Flask, render_template, send_from_directory
from flask import stream_with_context
from flask import request, Response
from helper import list_movies
import os

movies = {}
list_movies('D:\\Movie', movies)
app = Flask(__name__)

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
  # size = os.path.getsize(movies[movie])
  def serve_movie():
    with open(movies[movie], 'rb') as f:
      while True:
        data = f.read(16777216)
        if not data: break
        yield data
  return Response(stream_with_context(serve_movie()), direct_passthrough=True)

@app.route('/icons/<path:image>')
def images(image):
  return send_from_directory('icons', image)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)