import os

def list_movies(dir, movies):
  file_names = os.listdir(dir)
  for file_name in file_names:
    file_path = os.path.join(dir, file_name)
    if os.path.isdir(file_path):
      list_movies(file_path, movies)
    elif os.path.isfile(file_path) and file_name[-3:].lower() in ['mkv', 'mp4']:
      movies[file_name] = file_path

