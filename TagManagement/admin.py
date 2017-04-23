# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from TagManagement.models import tag_info, file_info, file_tag

admin.site.register(tag_info)
admin.site.register(file_info)
admin.site.register(file_tag)

