# -*- coding: utf-8 -*-

from django.contrib.auth.models import User

from .models import NoticeType, Notice

def send(notice_type_name, recipient, context={}, sender=None):
    notice_type = NoticeType.objects.get_or_create(name=notice_type_name)[0]

    if isinstance(recipient, User):
        recipient = [recipient]

    notices = []

    for rec in recipient:
        notice = Notice.objects.create_notice(notice_type, recipient=rec, sender=sender)
        notice.send(context)
        notices.append(notice)

    return notices