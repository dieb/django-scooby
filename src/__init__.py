# -*- coding: utf-8 -*-

from .models import NoticeType, Notice

def send(notice_type_name, to, context):
    notice_type = NoticeType.objects.get(name=notice_type_name)
    notice = Notice.objects.create(notice_type, recipient=to)
    return notice.send(context)
