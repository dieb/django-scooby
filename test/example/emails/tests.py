"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.contrib.auth.models import User

from scooby.shortcuts import send as send_notification
from scooby.models import *


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
        send_notification('test_notice', user,
                          {'test_message': 'Great message!'},
                          'sender@example.com')
        from django.core.mail import outbox

        email = outbox[0]
        self.assertEquals(email.from_email, 'sender@example.com')
        self.assertEquals(email.to, ['test@example.com'])
        self.assertEquals(len(email.alternatives), 1)
        self.assertEquals(email.alternatives[0][1], 'text/html')
