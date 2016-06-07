from os import listdir
from os.path import isfile, join
from motion import *
import cred

path = cred.path

files = []

suffix = '_tmp.jpg'

for f in listdir(path):
    if isfile(join(path, f)) and f.find(suffix) > -1:
        files.append(int(f.replace(suffix, '')))

files = sorted(files)

print files


def get_file_full_path(timestamp):
    return path + '/' + str(timestamp) + suffix


def get_image_obj(timestamp):
    return Image.open(get_file_full_path(timestamp))


for i in range(0, len(files) - 1):
    compared = compare_images(get_image_obj(files[i]), get_image_obj(files[i + 1]))
    print files[i],compared

