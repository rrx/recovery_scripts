Import sys
import os
import datetime
import shutil
from common import *

if __name__ == '__main__':
    for line in sys.stdin:
        parts = line.strip().split()
        h = parts[0]
        filename = parts[1][1:]
        ts = os.path.getmtime(filename)
        size = os.stat(filename).st_size

        try:
            d = datetime.datetime.fromtimestamp(ts)
        except ValueError:
            d = datetime.datetime.fromtimestamp(0)

        _, ext = os.path.splitext(filename)
        out = [h,filename,"%04d" % d.year, "%02d" % d.month, "%02d" % d.day, ext, "%d" % size, get_type_from_ext(ext)]
        print(",".join(out))
