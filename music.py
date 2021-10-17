import sys
import os
import datetime
import shutil

if __name__ == '__main__':
    for line in sys.stdin:
        parts = line.strip().split(",")
        h, filename, _, _, _, ext = parts
        if ext.lower() == '.mp3':
            out_filename = "/media/rrx/d/Music/%s.mp3" % h
            if not os.path.exists(out_filename):
                print("copy", filename, out_filename)
                shutil.copy(filename, out_filename)

        else:
            assert(False)


