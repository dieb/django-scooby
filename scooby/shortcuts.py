# -*- coding: utf-8 -*-

from .models import NoticeType, Notice

def send(notice_type_name, recipient, context={}, sender=None):
    notice_type = NoticeType.objects.get_or_create(name=notice_type_name)
    notice = Notice.objects.create_notice(notice_type, recipient=recipient, sender=sender)
    return notice.send(context)