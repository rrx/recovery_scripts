import mutagen
from mutagen.id3 import ID3, ID3NoHeaderError
from mutagen.easyid3 import EasyID3
import sys
from cachier import cachier
import csv
import os

def id3(filename):
    f = EasyID3(filename)
    return dict(f)

def load(filename):
    f = mutagen.File(filename)
    return dict(f)

def sanitize(f):
    f = dict(f)
    remove = [
        'GEOB:S', 'TSSE', 'encodedby', 'organization', 'genre',
        'TXXX', 'PRIV', 'TCON',
        '©too',
        '©gen',
        '---',
        'covr',
        'date', 'disknumber',
    ]
    to_remove = set()
    for k in f.keys():
        for r in remove:
            if k.startswith(r):
                to_remove.add(k)
    for k in to_remove:
        f.pop(k)

    return dict([(k.lower(), v) for k, v in f.items()])

def main(filename):
    path, filen = os.path.split(filename)
    basename, ext = os.path.splitext(filen)
    untagged = os.path.join("Untagged", basename)
    try:
        x = id3(filename)
        f = sanitize(x)
        d = dict(
            artist = parse_artist(f),
            album = parse_album(f).strip(),
            title = parse_title(f).strip(),
            track = parse_trkn(f).strip(),
        )
        parts = [d[k] for k in ['album', 'title', 'track'] if not is_empty(d[k])]
        if len(parts) > 0:
            d['name'] = " - ".join(parts)
            return f, "%(artist)s/%(name)s" % d
        else:
            return second_try(filename)

    except ID3NoHeaderError as e:
        pass
        # return second_try(filename)
        # f = sanitize(load(filename))
        # if len(f.keys()) == 0:
            # return f, untagged
        # else:
            # return f, str(e)

    except mutagen.mp3.HeaderNotFoundError as e:
        return f, str(e)

    return second_try(filename)

def parse_trkn(f):
    track = f.get('trkn')
    if track:
        return "%s of %s" % track[0]

    track = f.get('tracknumber')
    if track:
        return track[0].replace("/", " of ")

    track = f.get('wm/tracknumber')
    if track:
        return "%s" % track[0]

    return ""

def parse_title(f):
    title = f.get('©nam')
    wm_title = f.get('title')
    title2 = f.get('tit2')
    if title:
        return title[0]
    elif wm_title:
        return str(wm_title[0])
    elif title2:
        return title2[0]
    else:
        return ""

def is_empty(a):
    if a is None:
        return True
    elif len(a) == 0:
        return True
    elif len(str(a[0])) == 0:
        return True
    else:
        return False

def parse_artist(f):
    artist = f.get('artist')
    if not is_empty(artist):
        return artist[0]
    artist = f.get('tpe1')
    if artist:
        artist = list(artist)[0]
        return artist
    artist = f.get('©art')
    if not is_empty(artist):
        return artist[0]
    artist = f.get('wm/albumartist')
    if not is_empty(artist):
        return str(artist[0])
    return 'Unknown'


def parse_album(f):
    album = f.get('album')
    if album:
        return album[0]
    album = f.get('talb')
    if album:
        return list(album)[0]
    album = f.get('©alb')
    if album:
        return album[0]
    album = f.get('wm/albumname')
    if album:
        return album[0]
    return ""


def second_try(filename):
    path, filen = os.path.split(filename)
    basename, ext = os.path.splitext(filen)
    untagged = os.path.join("Untagged", basename)

    f = sanitize(load(filename))
    keys = list(f.keys())
    d = dict(
        artist = parse_artist(f).strip(),
        album = parse_album(f).strip(),
        title = parse_title(f).strip(),
        track = parse_trkn(f).strip(),
    )
    parts = [d.get(k) for k in ['album', 'title', 'track'] if not is_empty(d.get(k))]
    if keys == ['tsse']:
        return f, untagged
    elif not is_empty(d.get('artist')):
        if len(parts) > 0:
            d['name'] = " - ".join(parts)
            return f, "%(artist)s/%(name)s" % d
        else:
            return f, "%(artist)s/Unknown" % d
    else:
        return f, untagged

def sane_filename(src, dst, i):
    _, ext = os.path.splitext(src)
    dst = dst.replace(":", "-")
    dst = dst.replace("'", "")
    dst = dst.replace("\"", "")
    dst = dst.replace("&", "and")
    dst = dst.replace("?", "")
    si = " - F%05d" % i
    out = dst + si + ext

    def clean_part(s):
        return s.strip().replace("/", "-")

    parts = [clean_part(x) for x in out.split("/")]
    return os.path.join(*parts)

if __name__ == '__main__':
    output_filename = sys.argv[1]
    with open(output_filename, 'w') as fp:
        writer = csv.writer(fp)
        count = 0
        for line in sys.stdin:
            filename = line.strip()
            print('filename', filename)
            a, b = main(filename)
            out = sane_filename(filename, b, count)
            print(out, a)
            count += 1
            writer.writerow([out, a, filename])
            fp.flush()
