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
import eyed3
import utility


def create_input_for_apriori():
    f = open("./resources/input1.csv","w+")
    flist = file_info.objects.values('id')  # get all files in system
    for myfile in flist:
        mytags = file_tag.objects.filter(file_id=myfile['id']) #get all tags for file
        mytags = ",".join([str(tag_info.objects.filter(id = int(m.tag_id.id))[0].tag_name) for m in mytags ]) #get tagname against tagid
        print mytags
        f.write(str(mytags)+"\n")
    f.close()
    os.system("python ./resources/Apriori.py")
    return "hello"

def find_linked_tags(assigned_tags):
    mytags = assigned_tags
    assigned_tags = tuple(sorted(assigned_tags))
    myfile = open("./resources/rules.txt","rb")
    association_rules = pickle.load(myfile)
    # print "rule1:",association_rules
    try :
        suggested_tags = list(association_rules[assigned_tags])
    except :
        suggested_tags = []
    print "suggested_tags", suggested_tags
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

    return utility.getTopNDictItems(full_text_NNPS,5)

def findMetadataforMusic(filename): 
    tags = []  
    # 'album', 'album_artist', 'album_type', 'artist', 'artist_origin', 'artist_url', 'audio_file_url', 
    #'audio_source_url', 'best_release_date', 'bpm', 'cd_id', 'chapters', 'clear', 'comments', 'commercial_url',
    # 'copyright_url', 'disc_num', 'encoding_date', 'extended_header', 'file_info', 'frame_set', 'frameiter', 
    #'genre', 'getBestDate', 'getTextFrame', 'header', 'images', 'internet_radio_url', 'isV1', 'isV2', 'lyrics',
    # 'objects', 'play_count', 'publisher', 'recording_date', 'release_date', 'save',
    # 'title', 'track_num', 'unique_file_ids',  'version'
    audiofile = eyed3.load(filename)
    if audiofile.tag.artist:
        artistlist = audiofile.tag.artist.replace(' ','-').split(',')
        tags.extend([artist for artist in artistlist])

    if audiofile.tag.album:
        album = audiofile.tag.album.replace(' ','-')
        tags.append(album)

    if audiofile.tag.album_artist:
        album_artist = audiofile.tag.album_artist.replace(' ','-')
        tags.append(album_artist)

    if audiofile.tag.recording_date and audiofile.tag.recording_date.year:
        tags.append(str(audiofile.tag.recording_date.year))

    if audiofile.tag.genre.name:
        genre = audiofile.tag.genre.name.replace(' ','-')
        tags.append(genre)
    return list(set(tags))





   