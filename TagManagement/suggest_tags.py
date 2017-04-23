from django.shortcuts import render
from TagManagement.models import *
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import admin
from django.core import serializers
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from nltk import word_tokenize as wtok
from nltk.tag import pos_tag
from collections import defaultdict
import mimetypes
import os
import urllib
import pickle
import random


def create_input_for_apriori(request):
    f = open("./resources/input1.csv","w+")
    flist = file_info.objects.values('id')  # get all files in system
    for myfile in flist:
        mytags = file_tag.objects.filter(file_id=myfile['id']) #get all tags for file
        mytags = ",".join([str(tag_info.objects.filter(id = int(m.tag_id.id))[0].tag_name) for m in mytags ]) #get tagname against tagid
        print mytags
        f.write(str(mytags)+"\n")
    f.close()
    os.system("python ./resources/Apriori.py")
    return HttpResponse("hello")

def find_linked_tags(assigned_tags):
    mytags = assigned_tags
    assigned_tags = tuple(sorted(assigned_tags))
    myfile = open("./applications/TagBasedFileSystem/resources/rules.txt","rb")
    association_rules = pickle.load(myfile)
    #print association_rules[0]
    try :
        suggested_tags = list(association_rules[assigned_tags])
    except :
        suggested_tags = []
    print suggested_tags
    return suggested_tags

def create_graph_for_d3js(mytags):
    suggested_tags = find_linked_tags(mytags)
    len_source = len(mytags)
    len_target = len(suggested_tags)
    graph = {}
    graph['nodes'] = [{'name':t,'group':1} for t in mytags]
    graph['nodes'].extend([{'name':t,'group':2} for t in suggested_tags])
    graph['links']=[{'source':random.choice(range(len_source)),'target':t} for t in range(len_source,len_source+len_target) ]
    print graph
    return graph

def findNamedEntities(filename):
    f = open(filename,'r')
    content = f.read()
    content = wtok(content)
    content = pos_tag(content)
    full_text_NNPS = defaultdict( int )
    save = ""
    #noun chunking
    for word_tag in content:
        word = word_tag[0]
        postag = word_tag[1]

        if postag == "NNP" or postag == "NN" or postag == "NNS":
            save += word+"-"
       
        else:
            if len(save)>0:
                full_text_NNPS[save[:-1]] += 1
                save = ""

    return full_text_NNPS

def findFileType(filename):
    return "hello"
    print str(db().select(db.tag_info.ALL, orderby=db.tag_info.tag_name, limitby=(0,6)).as_list())
    ftype = mimetypes.guess_type(filename,strict=True)[0]
    if ftype:
        p = ftype.split("/")
        #session.flash = p
        if p[0] == "text":
            return p[1]
        else:
            return p[0]
    else: # if file type is null, return text tag for file
        return "text"
    
def isTextfile(filename):
    # if filetype text or None, return True
    if mimetypes.guess_type(filename,strict=True)[0] == 'text/plain' or not mimetypes.guess_type(filename,strict=True)[0]:
        return True
    else:
        return False
