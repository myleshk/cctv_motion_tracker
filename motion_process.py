from os import listdir
from os.path import isfile, join
from motion import *
import cred

path = cred.path
files = []
DEBUG = False

suffix = '_tmp.jpg'

for f in listdir(path):
    if isfile(join(path, f)) and f.find(suffix) > -1:
        files.append(int(f.replace(suffix, '')))

files = sorted(files)
file_count = len(files)

if DEBUG:
    print files


def get_file_full_path(timestamp):
    return path + '/' + str(timestamp) + suffix


def get_image_obj(timestamp):
    return Image.open(get_file_full_path(timestamp))


def prevent_from_deletion(index):
    global toDelete
    min = index - 60 if index > 60 else 0
    max = index+60 if index+60 < file_count else file_count
    max = index
    for i in range(min, max + 1):
        try:
            toDelete.remove(files[i])
        except ValueError:
            continue


count = 0
toDelete = []
motionIndexes = []
for i in range(0, file_count - 1):
    compared = compare_images(get_image_obj(files[i]), get_image_obj(files[i + 1]))
    if float(compared) > 0.6:
        print files[i], compared
        motionIndexes.append(i)
    else:
        toDelete.append(files[i])
        count += 1

for index in motionIndexes:
    prevent_from_deletion(index)

print "No motion for %d image(s) of total %d" % (count, file_count)
print "Delete List (count %d): \n" % len(toDelete), repr(toDelete)
