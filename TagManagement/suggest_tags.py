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
import itertools
import mimetypes
import os
import urllib
import pickle
import random
import eyed3
import utility
from fbrecog import recognize

THRESHOLD_FOR_SUGGESTIONS = 5

def createInputForApriori():
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

def findLinkedTags(assigned_tags,intent):
    assigned_tags = [ a.lower() for a in assigned_tags ]
    mytags = assigned_tags
    suggested_tags = set()
    myfile = open("./resources/rules.pkl","rb")
    association_rules = pickle.load(myfile)
    print assigned_tags,intent
    if intent == "suggest":
            combos = []
            for L in range(0, len(assigned_tags)+1):
              for subset in itertools.combinations(assigned_tags, L):
                combos.append(subset)
            combos.reverse()

            for assigned_tags in combos[:-1]:   
                if len(suggested_tags) > THRESHOLD_FOR_SUGGESTIONS:
                    break
                assigned_tags = tuple(sorted(assigned_tags))        
                try :
                    # print "assigned",assigned_tags,"suggested",suggested_tags
                    suggested_tags=suggested_tags.union((association_rules[assigned_tags]))
                except :
                    continue
            
    elif intent == "search" :
            try:
                assigned_tags = tuple(sorted(assigned_tags))
                suggested_tags = association_rules[assigned_tags]
            except:
                pass
    else:
        print "invalid input",assigned_tags,intent
    myfile.close()

    print "suggested_tags", list(suggested_tags - set(mytags))
    return list(suggested_tags - set(mytags))

def createGraphFord3js(mytags):
    suggested_tags = findLinkedTags(mytags,"search")
    len_source = len(mytags)
    len_target = len(suggested_tags)
    graph = {}
    graph['nodes'] = [{'name':t,'group':1} for t in mytags]
    graph['nodes'].extend([{'name':t,'group':2} for t in suggested_tags])
    graph['links'] = [{'source': i, 'target': i+1} for i in range(len(mytags)-1)]
    graph['links'].extend([{'source':random.choice(range(len_source)),'target':t} for t in range(len_source,len_source+len_target) ])
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
        word = word_tag[0].lower().strip()
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
        tags.extend([artist.lower().strip() for artist in artistlist])

    if audiofile.tag.album:
        album = audiofile.tag.album.replace(' ','-').lower().strip()
        tags.append(album)

    if audiofile.tag.album_artist:
        album_artist = audiofile.tag.album_artist.replace(' ','-').lower().strip()
        tags.append(album_artist)

    if audiofile.tag.recording_date and audiofile.tag.recording_date.year:
        tags.append(str(audiofile.tag.recording_date.year))

    if audiofile.tag.genre.name:
        genre = audiofile.tag.genre.name.replace(' ','-').lower().strip()
        tags.append(genre)
    return list(set(tags))

def findPeopleinImages(filename):
    tags = []
    access_token = "EAACEdEose0cBAK9K6pkwC14OcUmTJZCJsvTEp0ZCWAHNrvX1T5DcDE6ysYLssauZBXLZAm5csnd0CqIkfhhPybxJZBakrQZCyhZBfkRRautFDmmK9ZCHPyagHlJ36AEo7HzbfFJZCRLvEwCZAZCdDVMvO1ZAHu2NisienktAWZCI0Qo5BvdPFHZBrXHryZANtF7Isl7GOUZD"
    cookie = "sb=WGkHVw7DP8963aSs596mv06E; lu=TgbS1igAiSpQSJvk0jM4y2Ww; act=1494163402652/20; datr=Pr_WVU8EmTgHw73XLNithP2p; dats=1; c_user=100001779640836; xs=67:b5JJui_l7Dgcnw:2:1485616283:18409; fr=0yC3EEcA81Cj99RAi.AWV8ShvRPxm3JJ6Js9XX8Aqt1bc.BVvlmD.Gi.FkH.0.0.BZDwTz.AWWXT3Zr; presence=EDvF3EtimeF1494156981EuserFA21B01779640836A2EstateFDt3F"
    fb_dtsg = "AQFt-IPOJOAd:AQGLu1alNmDy"
    taglist = recognize(filename,access_token,cookie,fb_dtsg)
    for person in taglist:
        tags.append(person['name'].lower().strip())
            
    print "find people-",tags

    return tags