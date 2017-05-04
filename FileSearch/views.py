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
import json
from TagManagement.suggest_tags import *
from TagManagement.tag_dao import *


def browseAndSearch(request):
	request.session['selected_tag_list'] = {}
	return render(request,'browseAndSearch.html', locals())

def getGraphData(request):
	action = str(request.POST['action']).lower().strip()
	tag = str(request.POST['tag']).lower().strip()
	first_entry = str(request.POST['empty_tag_list']).lower().strip()

	if first_entry == 'true':
		request.session['selected_tag_list'] = {}		
	
	if action == 'add':
		request.session['selected_tag_list'][tag] = 1
	elif action == 'remove':
		del request.session['selected_tag_list'][tag]

	json_str = createGraphFord3js(request.session['selected_tag_list'].keys())

	return HttpResponse(json.dumps(json_str))

def getFilteredFiles(request):

	filtered_file_rows = set()

	for tag in request.session['selected_tag_list'].keys():
		file_rows = getFileRowsForTag(tag)
		if len(filtered_file_rows) == 0:
			filtered_file_rows = set([fr.file_id for fr in file_rows])
		else :
			file_rows =  set([fr.file_id for fr in file_rows])
			filtered_file_rows = filtered_file_rows & file_rows

		if len(filtered_file_rows) == 0:
			break

	file_dict = [{"Id": i+1,"Title":ffr.file_name} for i, ffr in zip(range(len(filtered_file_rows)), filtered_file_rows)]

	return HttpResponse(json.dumps(file_dict))