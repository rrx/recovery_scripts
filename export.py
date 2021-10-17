import sys
import os
import datetime
import shutil
from common import *

if __name__ == '__main__':
    choose_filetype = sys.argv[1]
    base = sys.argv[2]
    assert(choose_filetype in ['pic', 'music', 'movie', 'doc', 'other'])

    for i, line in enumerate(sys.stdin):
        h, filename, year, month, day, ext, size, _ = line.strip().split(',')
        filetype = get_type_from_ext(ext)

        name = os.path.basename(filename)
        if name == 'report.xml':
            continue

        if choose_filetype != filetype:
            continue

        if filetype == 'pic':
            ts = os.path.getmtime(filename)
            prefix = name[0]
            # check assumptions
            assert(prefix in ['t', 'f'])
            if prefix == 't':
                assert(ext == '.jpg')
                # skip thumbnails
                continue

            out_name = "%s%s" % (h, ext)

            d = get_date(ts)
            year = "%04d" % d.year
            month = "%02d" % d.month
            day = "%02d" % d.day
            directory = os.path.join(base, "Pictures/%s-%s-%s" % (year, month, day))
            if not os.path.exists(directory):
                os.makedirs(directory)
            out_filename = os.path.join(directory, out_name)

            if not os.path.exists(out_filename):
                print(i, "copy", filename, out_filename)
                shutil.copy(filename, out_filename)
            # shutil.copystat(filename, out_filename)
            os.utime(out_filename, (ts, ts))

        elif filetype == 'music':
            directory = os.path.join(base, "Music/%s" % (h[:2]))
            if not os.path.exists(directory):
                os.makedirs(directory)
            out_filename = os.path.join(directory, "%s%s" % (h, ext))
            if not os.path.exists(out_filename):
                print(i, "copy", filename, out_filename)
                shutil.copy(filename, out_filename)

        elif filetype == 'movie':
            ts = os.path.getmtime(filename)
            directory = os.path.join(base, "Movies/%s" % (h[:1]))
            if not os.path.exists(directory):
                os.makedirs(directory)
            out_filename = os.path.join(directory, "%s%s" % (h, ext))
            if not os.path.exists(out_filename):
                print(i, "copy", filename, out_filename)
                shutil.copy(filename, out_filename)
            os.utime(out_filename, (ts, ts))

        elif filetype == 'doc':
            ts = os.path.getmtime(filename)
            d = get_date(ts)
            year = "%04d" % d.year
            month = "%02d" % d.month
            day = "%02d" % d.day
            directory = os.path.join(base, "Documents/%s-%s-%s" % (year, month, day))
            if not os.path.exists(directory):
                os.makedirs(directory)
            out_filename = os.path.join(directory, name)
            if not os.path.exists(out_filename):
                print(i, "copy", filename, out_filename)
                shutil.copy(filename, out_filename)

        else:
            if ext.startswith("."):
                ext = ext[1:]
            elif ext == "":
                ext = "unknown"
            else:
                assert(False)

            ts = os.path.getmtime(filename)
            d = get_date(ts)
            year = "%04d" % d.year
            month = "%02d" % d.month
            day = "%02d" % d.day
            directory = os.path.join(base, "Other/%s/%s/%s" % (ext, year, h[:2]))
            if not os.path.exists(directory):
                os.makedirs(directory)
            out_filename = os.path.join(directory, "%s.%s" % (h, ext))
            if not os.path.exists(out_filename):
                print(i, "copy", filename, out_filename)
                shutil.copy(filename, out_filename)

