from TagManagement.models import *
import TagBasedFileSystem.path_variables as path
from django.utils import timezone
import os

def getTagListForFile(complete_file_path):
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

def saveFiletoDB(filepath):
    stat = os.stat(filepath)
    inode_number = stat.st_ino
    file_row = file_info.objects.filter(inode_number=inode_number)

    if not file_row :
        mtime = timezone.make_aware(datetime.datetime.fromtimestamp(stat.st_mtime))
        file_row = file_info(inode_number=inode_number,file_name=filepath,mtime=mtime)
    else :
        file_row = file_row[0]
        file_row.file_name = filepath

    file_row.save()
    print file_row
    return file_row

def saveTagtoDB(tag):
    tag_row = tag_info.objects.filter(tag_name=tag)
    
    if tag_row :
        tag_row = tag_row[0]
        tag_row.frequency = tag_row.frequency + 1
    else :
        tag_row = tag_info(tag_name=tag,frequency=1)
    tag_row.save()
    return tag_row

def addTagToFile(tag,filename):
    tag_row = saveTagtoDB(tag)
    file_row = getFileRecordfromFilepath(filename)

    f = file_tag(file_id=file_row,tag_id=tag_row)
    f.save() 

def getTagnameFromTagid(tag_id):
    return tag_info.objects.filter(id=tag_id)[0].tag_name

def getTagRowFromTagname(tag_name):
    return tag_info.objects.filter(tag_name=tag_name)[0]

def getListofUntaggedModifiedFiles():
    list_of_modified_files = file_info.objects.filter(mtime__gt = timezone.now()-datetime.timedelta(hours=path.SAVE_NOTIFICATION_FOR_X_HOURS),tagged_status=False)
    return list_of_modified_files

def getFileRecordfromFilepath(filepath):
    stat = os.stat(filepath)
    inode_number = stat.st_ino
    file_row = file_info.objects.filter(inode_number=inode_number)

    #if file renamed
    if file_row:
        if filepath != file_row[0].file_name:
            f = file_row[0]
            f.file_name = filepath
            f.save()
        return file_row[0]

    else:
        return None
def getFileRowsForTag(tag):
    tag_row = getTagRowFromTagname(tag)
    file_rows = file_tag.objects.filter(tag_id=tag_row)
    return file_rows

def updateFileTaggedStatus(filepath):
    file_row = getFileRecordfromFilepath(filepath)
    if file_row:
        file_row.tagged_status = True
        print "Set file tagged status of",filepath," to True"
        file_row.save()
    else:
        raise Exception("No such File Found, file might have been renamed in the process of assigning tags")
