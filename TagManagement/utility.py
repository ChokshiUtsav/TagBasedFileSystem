from nltk import word_tokenize as wtok
from nltk.tag import pos_tag
from collections import defaultdict
import mimetypes

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

def getTopNDictItems(dct,n):    # extract n most frequent named entities from file
    print "topn",[pair[0] for pair in sorted(dct.items(), key=lambda dct: dct[1], reverse = True)][:n]

    return [pair[0] for pair in sorted(dct.items(), key=lambda dct: dct[1], reverse = True)][:n]
