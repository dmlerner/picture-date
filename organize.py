import datetime
import exif
import glob
import os
import shutil

HOURS_OFFSET = 0
KEEP_ORIGINAL = True


def offset(d, hours):
    # This is hacky, and I am ashamed.
    assert -23 <= hours <= 23
    new_hour = d.hour + hours
    replaced = d.replace(hour=new_hour % 23)
    one_day = datetime.timedelta(1)
    if new_hour > 23:
        return replaced + one_day
    if new_hour < 0:
        return replaced - one_day
    return replaced


images = []
filenames = glob.glob('*.JPG')
for filename in filenames:
    print(filename)
    with open(filename, 'rb') as f:
        images.append(exif.Image(f))
    images[-1].filename = filename
    print(images[-1].datetime)
for i in images:
    i._datetime = datetime.datetime.strptime(i.datetime, '%Y:%m:%d %H:%M:%S')
    i._datetime = offset(i._datetime, HOURS_OFFSET)
    i.folder = i._datetime.strftime('%Y:%m:%d')
images.sort(key=lambda i: i._datetime)
for i in images:
    if not os.path.exists(i.folder):
        os.mkdir(i.folder)
    target_path = os.path.join(i.folder, i.filename)
    if not os.path.exists(target_path):
        if KEEP_ORIGINAL:
            shutil.copy(i.filename, target_path)
        else:
            shutil.move(i.filename, target_path)
