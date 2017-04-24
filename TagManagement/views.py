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
from django.contrib import messages

import os
import urllib
import pickle
import random
import utility
import eyed3
from tag_dao import *
import suggest_tags

def findMostPopularTags():
    most_popular_tag_rows = tag_info.objects.all()
    most_popular_tag_list = [ row.tag_name for row in most_popular_tag_rows ]
    return most_popular_tag_list[:6]

def index(request):
    return render(request,'index.html', {})

def findSuggestedTags(request):
    filename = request.session['complete_file_path']
    ftype = utility.findFileType(filename)
    assigned_tag_list = request.session['assigned_tag_list'].keys()

    tags = []
    tags.append(ftype)
    tags.extend(suggest_tags.find_linked_tags(assigned_tag_list))
    #print tags
    print ftype
    if ftype == "text":
        entities = suggest_tags.findNamedEntities(filename)
    elif ftype == "audio":
        entities = suggest_tags.findMetadataforMusic(filename)
    # elif ftype == "video":

    tags.extend(entities)

    print tags
    request.session['suggested_tag_list'] = tags
    eval_str ='$("#suggested_tags").html(\''+renderTagsAsButtons(tags)+'\');'
    return eval_str


def findAutoCompleteTags(partial_tag_input):
    auto_complete_tags_list = []

    if partial_tag_input:
       #tag_input =  "%" + str(partial_tag_input).lower() + "%"         
       auto_complete_tags_list = tag_info.objects.filter(tag_name__istartswith = partial_tag_input).order_by('frequency').reverse()
       print auto_complete_tags_list
       auto_complete_tags_list = [row.tag_name for row in auto_complete_tags_list]
       print auto_complete_tags_list

    return auto_complete_tags_list [:6]   

def renderAutoCompleteBox(auto_complete_list):
    rendered_output = ""
    if len(auto_complete_list) != 0:
        for i in auto_complete_list:
            rendered_output = rendered_output + '<button type="button" class="list-group-item list-group-item-info">' + str(i) +  '</button>' 
    return HttpResponse(rendered_output)

def autoCompleteTags(request):
    print request.POST
    auto_complete_tags_list = findAutoCompleteTags(request.POST['tag_search'])

    return renderAutoCompleteBox(auto_complete_tags_list)

def findAutoCompleteFiles(partial_file_name_input):

    auto_complete_files_list = []
    parent_dir_path = os.path.dirname(partial_file_name_input)
    file_name = os.path.basename(partial_file_name_input).lower()
    if file_name:
       auto_complete_files_list = os.listdir(parent_dir_path)
       auto_complete_files_list = [f for f in auto_complete_files_list if f.lower().startswith(file_name)]
    return auto_complete_files_list[:6]

def autoCompleteFilePath(request):
    file_list = findAutoCompleteFiles(request.session['user_dir'] + request.POST['file_path'])
    return renderAutoCompleteBox(file_list)

def renderTagsAsLabels(tag_list):
    rendered_output = ""

    count = 0
    if len(tag_list) != 0:
        for tag in tag_list:
            if tag :
                rendered_output = rendered_output + '<span class="label label-info" style="font-size:16px; margin-right:10px">' + tag + '<a class="btn btn-default-small" href="#" role="button" name="'+ tag + '"> <span class="glyphicon glyphicon glyphicon-remove" aria-hidden="true"></span></a></span>'            
                count = count + 1
                if count%2 == 0:
                    rendered_output += "<br/>"
    return rendered_output

def renderTagsAsButtons(tag_list):
    rendered_output = ""

    if len(tag_list) != 0:
        for tag in tag_list:
            if tag :
                rendered_output = rendered_output + '<button class="btn btn-primary" type="button" style="margin-bottom:10px;margin-right:3px;"> '+ tag +' </button>'             
    return rendered_output
    
def updateView(request):
    eval_str = "$('#assigned_tags').html(\'"+renderTagsAsLabels(request.session['assigned_tag_list'].keys())+"\');"
    eval_str += findSuggestedTags(request)
    # print eval_str
    return eval_str


def maintainAssignedTags(request):
    key=str(request.POST['tag']).lower().strip()
    if 'assigned_tag_list' not in request.session:
        request.session['assigned_tag_list']={}
    request.session['assigned_tag_list'][key]=1
    findSuggestedTags(request)
    request.session.modified = True
    
    return HttpResponse(updateView(request))

def addAllToAssignedTags(request):
    key = str(request.POST['type']).lower()
    if key == 'popular':
        for tag in request.session['most_popular_tag_list']:
            request.session['assigned_tag_list'][tag] = 1
    elif key == 'suggest':
        for tag in request.session['suggested_tag_list']:
            request.session['assigned_tag_list'][tag] = 1
    return HttpResponse(updateView(request))


def removeAssignedTags(request):
    key=str(request.POST['tag']).lower()

    if not 'assigned_tag_list' in request.session.keys():
        request.session['assigned_tag_list']={}
    else:
        if key in request.session['assigned_tag_list'].keys():
           del request.session['assigned_tag_list'][key]
           request.session.modified = True

    return HttpResponse(updateView(request))

def clearTagLists(request):
    request.session['assigned_tag_list']={}
    request.session['most_popular_tag_list'] = []
    request.session['suggested_tag_list'] = []
    request.session['extracted_assigned_tag_list'] = {}
    return ""        

def storeFilePath(request):
    complete_file_path = request.session['user_dir'] + request.POST['file_path'][:-1]
    eval_str = ""

    if os.path.isfile(complete_file_path):

        #jquery to be evaluated on client side
        eval_str =  '$("#file_path").prop("disabled",true);'
        eval_str += '$("#tag_div").find(":input").prop("disabled",false);'
        eval_str += '$("#suggestion_div").find(":input").prop("disabled",false);'
        eval_str += '$("#assign_div").find(":input").prop("disabled",false);'
        eval_str += '$("#file_path_error").prop("hidden",true);'

        #save complete file path
        request.session['complete_file_path'] = complete_file_path

        #retrieve already assigned tags for file, if any
        assigned_tag_dict = getTagListForFile(request, complete_file_path)
        request.session['assigned_tag_list'] = assigned_tag_dict
        if len(assigned_tag_dict.keys()) > 0:
            request.session['extracted_assigned_tag_list'] = request.session['assigned_tag_list']
        eval_str += updateView(request)
    else:
        eval_str += '$("#file_path_error").prop("hidden",false)';

    return HttpResponse(eval_str)


def assignTags(request):
    #messages.add_message(request, messages.INFO, 'All items on this page have free shipping.')
    clearTagLists(request)
    user_dir = "/home/deeksha/"
    request.session['user_dir'] = user_dir    
    most_popular_tag_list  = findMostPopularTags()
    request.session['most_popular_tag_list'] = most_popular_tag_list
    return render(request,'assignTags.html', locals())

def settings():
    return "Settings"

def user(request):
    return HttpResponse("nothing here")

def assignTagsToFile(request):

    #extract file id
    inode_number = os.stat(request.session['complete_file_path']).st_ino

    file_row = file_info.objects.filter(inode_number=inode_number)
    if not file_row :
        file_row = file_info(inode_number=inode_number,file_name=request.session['complete_file_path'])
        file_row.save()
    else:
        file_row = file_row[0]
    file_id = file_row.id

    tag_list_1 = set(request.session['assigned_tag_list'])                             # tags needs to be added
    tag_list_2 = set(request.session['extracted_assigned_tag_list'])                   # tags needs to be deleted  
    tag_list_1, tag_list_2 = (tag_list_1-tag_list_2), (tag_list_2-tag_list_1)   
    
    for tag in tag_list_2:
        tag_row = tag_info.objects.filter(tag_name=tag)[0]
        tag_id = tag_row.id
        file_tag.objects.filter(file_id = file_row,tag_id=tag_row).delete()

        tag_row.frequency = tag_row.frequency - 1
        tag_row.save()   
        
    for tag in tag_list_1:
        tag_row = tag_info.objects.filter(tag_name=tag)
        print tag_row
        if tag_row:
            tag_row = tag_row[0]
            tag_row.frequency = tag_row.frequency + 1
        else:
            tag_row = tag_info(tag_name=tag,frequency=1)
        tag_row.save()
        tag_id = tag_row.id
        f = file_tag(file_id=file_row,tag_id=tag_row)
        f.save() 

    messages.add_message(request, messages.INFO, 'Tags are assigned to file : ' + request.session['complete_file_path'])

    return HttpResponse("Assigned Tags")
