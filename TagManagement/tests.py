# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from TagManagement.models import *
# Create your tests here.
from django.http import HttpResponse, HttpResponseRedirect
import TagManagement.tag_dao as td
import TagBasedFileSystem.path_variables as path
import TagManagement.views as view


def makeDB():
	# crons job file is always modified in 24 hours
	filename = path.MOUNT_DIR+"crons.log"
	td.saveFiletoDB(filename)

class tag_daoTesting(TestCase):

	def testsaveFiletoDB(self):
		# crons job file is always modified in 24 hours
		filename = path.MOUNT_DIR+"crons.log"
		td.saveFiletoDB(filename)
		self.assertEqual(1,file_info.objects.all().count(),"saveFiletoDB failed")

	def testgetFileRecordfromFilepath(self):
		makeDB()
		filename = path.MOUNT_DIR+"crons.log"
		x = td.getFileRecordfromFilepath(filename)
		self.assertEqual(filename,x.file_name,"getFileRecordfromFilepath failed")

	def testaddtagtoFile(self):
		makeDB()
		filename = path.MOUNT_DIR+"crons.log"
		td.addTagToFile("newtag",filename)
		self.assertEqual(tag_info.objects.filter(tag_name="newtag")[0].frequency,1,"tag not added to file")
		self.assertEqual(td.getFileRowsForTag("newtag").count(),1,"no file added for newtag")

	def testremoveTagFromFile(self):
		makeDB()
		filename = path.MOUNT_DIR+"crons.log"
		td.addTagToFile("newtag",filename)
		td.removeTagFromFile("newtag",filename)
		self.assertEqual(tag_info.objects.filter(tag_name="newtag")[0].frequency,0,"tag not removed file")
		self.assertEqual(td.getFileRowsForTag("newtag").count(),0,"no file removed for newtag")

	def testremoveFileFromDB(self):
		makeDB()
		filepath = path.MOUNT_DIR+"crons.log"
		td.removeFileFromDB(filepath)
		self.assertEqual(file_info.objects.all().count(),0,"file not removed")


class viewsTesting(TestCase):

	def testretrieveFileInfo(self):
		makeDB()
		filename = path.MOUNT_DIR+"somenonexistentfile"
		try:
			view.retrieveFileInfo(filename)
			msg = "record found"
		except:
			msg = "no record"
		self.assertEqual(msg,"no record","retrieveFile failed")

		filename = path.MOUNT_DIR+"crons.log"
		view.retrieveFileInfo(filename)
		try:
			rec = view.retrieveFileInfo(filename)
			self.assertEqual(filename,rec.file_name,"retrieveFile failed")
			msg = "record found"
		except:
			msg = "no record"
		self.assertEqual(msg,"record found","retrieveFile failed")






