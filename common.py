import datetime
def is_pic(ext):
    return ext.lower() in ['.jpg', '.jpeg', '.gif', '.png', '.tif']

def is_music(ext):
    return ext.lower() in ['.mp3', '.flac', '.m4p', '.wma', '.wav', '.aif']

def is_docs(ext):
    return ext.lower() in ['.xls', '.xlsx', '.doc', '.docx', '.odt', '.pdf', '.rtf', '.txt', '.ppt']

def is_movies(ext):
    return ext.lower() in ['.mp4', '.wmv', '.3gp', '.avi', '.mkv', '.mov', '.mpg']

def get_type_from_ext(ext):
    if is_pic(ext):
        return 'pic'
    elif is_music(ext):
        return 'music'
    elif is_docs(ext):
        return 'doc'
    elif is_movies(ext):
        return 'movie'
    else:
        return 'other'

def get_date(ts):
    try:
        return datetime.datetime.fromtimestamp(ts)
    except ValueError:
        return datetime.datetime.now()

