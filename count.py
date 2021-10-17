import sys
import os
import datetime
import shutil
import collections
import humanize

if __name__ == '__main__':
    exts = collections.defaultdict(set)
    sizes = collections.defaultdict(int)
    total = 0
    for line in sys.stdin:
        h, filename, year, month, day, ext, size, filetype = line.strip().split(',')
        basename = os.path.basename(filename)
        if basename == 'report.xml':
            continue

        prefix = basename[0]
        parts = basename.split(".")

        # check assumptions
        assert(prefix in ['b', 't', 'f'])
        if prefix == 't':
            assert(ext == '.jpg')

        # make sure we don't have any broken files
        assert(prefix != 'b')

        if h not in exts[filetype]:
            sizes[filetype] += int(size)
        exts[filetype].add(h)
        total += 1

    for k,v in sorted(sizes.items(), key=lambda x: x[1]):
        print(k, len(exts[k]), humanize.naturalsize(sizes[k]))
    print('total', total, humanize.naturalsize(sum(sizes.values())))

