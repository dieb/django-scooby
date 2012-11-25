# -*- coding: utf-8 -*-

from django.contrib import admin

from scooby.models import NoticeType, Notice

admin.site.register(NoticeType)
admin.site.register(Notice)