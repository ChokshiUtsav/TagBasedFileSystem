from django.shortcuts import render
from FileSearch.models import *
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
from TagManagement.suggest_tags import *

def browseAndSearch(request):
	return render(request,'browseAndSearch.html', locals())

def getGraphData(request):
    tag = str(request.POST['tag']).lower().strip()
    tag_list = []
    tag_list.append(tag)

    json_str = create_graph_for_d3js(tag_list)
    json_str = str(json_str).replace("'",'"')

    print json_str

    return HttpResponse(json_str)
    

def getFilteredFiles(request):
	return HttpResponse("OK")