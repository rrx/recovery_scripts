import sys
import os
import datetime
import shutil

if __name__ == '__main__':
    for i, line in enumerate(sys.stdin):
        filename = line.strip()
        directory = os.path.dirname(filename)
        basename = os.path.basename(filename)
        out_directory = os.path.join(directory, basename[:2])
        if not os.path.exists(out_directory):
            os.makedirs(out_directory)
        out_filename = os.path.join(out_directory, basename)
        print(i, "move", filename, out_filename)
        shutil.move(filename, out_filename)

