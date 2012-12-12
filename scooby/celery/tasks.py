# -*- coding: utf-8 -*-

from django.conf import settings
from celery import Celery

celery = Celery('scooby', backend='amqp', broker='amqp://guest@localhost//')

if getattr(settings, 'CELERY_ALWAYS_EAGER'):
    del celery
    celery = Celery('scooby') # Rewrite
    celery.conf.update(CELERY_ALWAYS_EAGER=True)

@celery.task
def send_notice(notice, passed_context):
    """ Sends a pending notice
    """
    assert not notice.sent, 'Notice already sent!'
    notice.send(passed_context) # Notice saves when it send succcesfuly.
    return notice