from os import listdir, remove
from os.path import isfile, join
from motion import *
import cred
import time


def is_obsolete(filename, delta_seconds):
    ts = int(filename2index(filename))
    current_ts = int(time.time() * 10)
    return (current_ts - ts) > (delta_seconds * 10)


def get_file_full_path(timestamp):
    return path + '/' + str(timestamp) + suffix


def get_image_obj(timestamp):
    return Image.open(get_file_full_path(timestamp))


def prevent_from_deletion(index):
    global files_to_delete
    min_index = index - 60 if index > 60 else 0
    max_index = index + 60 if index + 60 < file_count else file_count
    for i in range(min_index, max_index):
        try:
            files_to_delete.remove(files[i])
        except ValueError:
            continue
        except IndexError:
            print "IndexError for index %d" % i


def filename2index(filename):
    return int(filename.replace(suffix, ''))


def concat(a, b):
    for item in a:
        if item not in b:
            b.append(item)
    return b


path = cred.path
files = []
obsolete_files = []
DEBUG = False

suffix = '_tmp.jpg'

for f in listdir(path):
    if isfile(join(path, f)) and f.find(suffix) > -1:
        if is_obsolete(f, 1800):
            obsolete_files.append(filename2index(f))
        files.append(filename2index(f))

files = sorted(files)
obsolete_files = sorted(obsolete_files)
file_count = len(files)

if DEBUG:
    print files

count = 0
files_to_delete = []
motionIndexes = []
for i in range(0, file_count - 1):
    compared = compare_images(get_image_obj(files[i]), get_image_obj(files[i + 1]))
    if float(compared) > 0.6:
        print files[i], compared
        motionIndexes.append(i)
    else:
        files_to_delete.append(files[i])
        count += 1

for index in motionIndexes:
    prevent_from_deletion(index)

# TODO: backup obsolete files somewhere
print "Obsoletes: ", len(obsolete_files)
files_to_delete = concat(files_to_delete, obsolete_files)

print "No motion for %d image(s) of total %d" % (count, file_count)
print "Delete List (count %d): \n" % len(files_to_delete), repr(files_to_delete)

if len(files_to_delete) > 0:
    print "Deleting files"

    count = 0
    for timestamp in files_to_delete:
        # remove(get_file_full_path(timestamp))
        count += 1
    print "%d files deleted" % count
