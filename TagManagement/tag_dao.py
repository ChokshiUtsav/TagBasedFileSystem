from TagManagement.models import *
import os

def getTagListForFile(request, complete_file_path):

	inode_number = os.stat(complete_file_path).st_ino
	file_rows = file_info.objects.filter(inode_number=inode_number)
	print file_rows
	tag_dict = {}

	if len(file_rows) > 0:
		file_id = file_rows[0].id
		tag_rows = file_tag.objects.filter(file_id=file_rows[0])
		print tag_rows
		for tr in tag_rows:
			tag = tag_info.objects.filter(id=tr.tag_id.id)[0].tag_name
			tag_dict[tag] = 1

	return tag_dict

'''
f = file_info(inode_number=inode_number,file_name=file_name)
f.save()
'''


def getTagnameFromTagid(tag_id):
	return tag_info.objects.filter(id=tag_id)[0].tag_name

def getTagidFromTagname(tag_name):
	return tag_info.objects.filter(tag_name=tag_name)[0].id
