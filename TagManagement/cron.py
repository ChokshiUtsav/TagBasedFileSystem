from django_cron import CronJobBase, Schedule
from django.utils import timezone
from datetime import datetime
from models import *
import os
from sys import platform as _platform
import sys
import TagBasedFileSystem.path_variables as path
from tag_dao import *

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 120  # every 120 minutes
    # RUN_AT_TIMES = ['15:48']
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'tag.Apriori' # a unique code
    
    def do(self):
        print path.HOME
        f = open(path.HOME+"resources/input1.csv","w+")
        flist = file_info.objects.values('id')  # get all files in system
        for myfile in flist:
            mytags = file_tag.objects.filter(file_id=myfile['id']) #get all tags for file
            mytags = ",".join([str(tag_info.objects.filter(id = int(m.tag_id.id))[0].tag_name) for m in mytags ]) #get tagname against tagid
            print mytags
            f.write(str(mytags)+"\n")
        f.close()
        #os.system("python "+path.HOME+"resources/Apriori.py")
        import resources.Apriori

class MyCronJob1(CronJobBase): # finding files created in last 24 hours
    RUN_EVERY_MINS = 120  # every 120 minutes
    # RUN_AT_TIMES = ['15:48']
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'file.NewFiles' # a unique code
    
    def do(self):
        # linux
        if _platform == "linux" or _platform == "linux2":
           fileslist = os.system("find ~/[a-zA-Z0-9]* -mtime 0 -type f > "+path.HOME+"resources/modifiedFiles.txt")
         # MAC OS X
        elif _platform == "darwin":
           fileslist = ""

        # Windows
        elif _platform == "win32":
            fileslist = ""

        f = open(path.HOME+"resources/modifiedFiles.txt","r")
        for fle in f.readlines():
            file_row = saveFiletoDB(fle)
            mtime = timezone.make_aware(datetime.fromtimestamp(os.stat(fle).st_mtime))

            if mtime > file_row.mtime :
                file_row.tagged_status = False
                file_row.mtime = mtime
            else : 
                file_row.tagged_status = True
            file_row.save()



                    



            