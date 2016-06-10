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
    assert type(a) == type(b) == list
    return list(set(a + b))


# Main procedure

# Initiate variables
path = cred.path
files = []
obsolete_files = []
DEBUG = False
suffix = '_tmp.jpg'
files_to_delete = []
files_with_motion = []

# Search for image files and check timestamp for obsolete items
for f in listdir(path):
    if isfile(join(path, f)) and f.find(suffix) > -1:
        if is_obsolete(f, 1800):
            obsolete_files.append(filename2index(f))
        files.append(filename2index(f))

# Sort list of files and obsolete files
files = sorted(files)
obsolete_files = sorted(obsolete_files)

# Get total count of image files to be processed
file_count = len(files)

# Debug stuff
if DEBUG:
    print files

no_motion_count = 0
for i in range(0, file_count - 1):
    compared = compare_images(get_image_obj(files[i]), get_image_obj(files[i + 1]))
    if float(compared) > 0.6:
        print files[i], compared
        files_with_motion.append(i)
    else:
        files_to_delete.append(files[i])
        no_motion_count += 1

for index in files_with_motion:
    prevent_from_deletion(index)

# TODO: backup obsolete files somewhere
print "Obsoletes: ", len(obsolete_files)
files_to_delete = concat(files_to_delete, obsolete_files)

print "No motion for %d image(s) of total %d" % (no_motion_count, file_count)

# Debug
if DEBUG:
    print "Delete List: \n" % repr(files_to_delete)

if len(files_to_delete) > 0:
    print "Deleting files"

    deleted_count = 0
    for timestamp in files_to_delete:
        # remove(get_file_full_path(timestamp))
        deleted_count += 1
    print "%d files deleted" % deleted_count
