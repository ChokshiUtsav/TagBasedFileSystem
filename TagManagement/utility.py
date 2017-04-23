from nltk import word_tokenize as wtok
from nltk.tag import pos_tag
from collections import defaultdict
import mimetypes

def isTextfile(filename):
    # if filetype text or None, return True
    if mimetypes.guess_type(filename,strict=True)[0] == 'text/plain' or not mimetypes.guess_type(filename,strict=True)[0]:
        return True
    else:
        return False
def findFileType(filename):
    ftype = mimetypes.guess_type(filename,strict=True)[0]
    if ftype:
        p = ftype.split("/")
        if p[0] == "text":
            return p[1]
        else:
            return p[0]
    else: # if file type is null, return text tag for file
        return "text"
