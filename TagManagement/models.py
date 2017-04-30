from __future__ import unicode_literals
from django.db import models
from django.forms import ModelForm
import datetime
import os
from django.utils import timezone

# Create your models here.

class tag_info(models.Model):
    frequency = models.IntegerField(default=0)
    tag_name = models.CharField(max_length=100)

    def __str__(self):
       return str(self.tag_name)+"\t"+str(self.frequency)

class file_info(models.Model):
    inode_number = models.IntegerField(default=0)
    file_name = models.CharField(max_length=256)
    mtime = models.DateTimeField(default = timezone.now)
    tagged_status = models.BooleanField(default=False)

    def __str__(self):
       return str(self.file_name)+"\t"+str(self.inode_number)


class file_tag(models.Model):
    file_id = models.ForeignKey(file_info, on_delete=models.CASCADE)
    tag_id = models.ForeignKey(tag_info, on_delete=models.CASCADE)
    def __str__(self):
       return str(self.file_id)+"\t"+str(self.tag_id)
