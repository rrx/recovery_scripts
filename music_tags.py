import csv
import sys
import shutil
import os

if __name__ == '__main__':
    path = sys.argv[2]
    tags = sys.argv[1]
    csv.field_size_limit(1024*1024)
    with open(tags, 'r') as fp:
        reader = csv.reader(fp)
        i = 0
        for dst, _, src in reader:
            dst2 = os.path.join(path, dst).replace("\"", "").replace("./", "/").replace("  ", " ").replace('|', '').replace('*', '-').replace("\\", "-").replace(">","").replace("<","")

            print(src, dst2)
            i += 1
            directory = os.path.split(dst2)[0]
            if not os.path.exists(directory):
                os.makedirs(directory)
            if not os.path.exists(dst2):
                print(i, "copy", src, dst2)
                shutil.copy(src, dst2)
