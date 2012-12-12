"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import warnings
import time

from django.test import TestCase
from django.contrib.auth.models import User

from scooby.shortcuts import send, queue
from scooby.models import *


def check_celery_not_installed():
    try:
        import celery
    except ImportError:
        warnings.warn('Not testing queue() function as celery is not installed.')
        return True


class Tests(TestCase):

    def setUp(self):
        self.notice_type = NoticeType(name="test_notice")
        self.notice_type.save()

    def test_create_notice_type(self):
        created = NoticeType.objects.get(name="test_notice")
        self.assertEquals(created, self.notice_type)
        self.assertEquals(created.name, "test_notice")

    def test_send_html_notification(self):
        user = User.objects.create(email='test@example.com')

        send('test_notice', user,
             {'test_message': 'Great message!'},
             'sender@example.com')

        from django.core.mail import outbox

        email = outbox[0]
        self.assertEquals(email.from_email, 'sender@example.com')
        self.assertEquals(email.to, ['test@example.com'])
        self.assertEquals(len(email.alternatives), 1)
        self.assertEquals(email.alternatives[0][1], 'text/html')

    def test_queue(self):
        if any([check_celery_not_installed()]):
            return

        user = User.objects.create(email='test@example.com')

        result = queue('test_notice', user,
                       {'test_message': 'Great message!'},
                       'sender@example.com')

        # Make sure task runs successfully
        self.assertEquals(len(result), 1)
        result = result[0]
        self.assertTrue(result.successful())

        # Make sure it was marked as sent
        notice = result.get()
        self.assertTrue(notice.sent)

        # Check the actual email on the outbox
        from django.core.mail import outbox
        email = outbox[0]
        self.assertEquals(email.from_email, 'sender@example.com')
        self.assertEquals(email.to, ['test@example.com'])
        self.assertEquals(len(email.alternatives), 1)
        self.assertEquals(email.alternatives[0][1], 'text/html')
