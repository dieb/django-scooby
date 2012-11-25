# -*- coin
import os
import smtplib
import datetime
import logging

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.mail.message import EmailMessage
from django.template.loader import render_to_string
from django.utils.translation import ugettext_noop as _

from .context import NoticeContext

log = logging.getLogger(__name__)


class NoticeType(models.Model):
    name = models.CharField(max_length=100)

    @property
    def templates_path(self):
        return 'notices/%s/' % self.name

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("notice type")
        verbose_name_plural = _("notice types")


class NoticeManager(models.Manager):

    def create_notice(self, notice_type, recipient, sender=None):
        if sender is None:
            sender = settings.DEFAULT_FROM_EMAIL

        notice = self.model(notice_type=notice_type,
                            recipient=recipient,
                            sender=sender)
        notice.save()
        return notice


class Notice(models.Model):
    notice_type = models.ForeignKey(NoticeType)

    recipient = models.ForeignKey(User)
    sender = models.EmailField(blank=True, null=True)

    email_subject = models.TextField(blank=True, null=True)
    email_body = models.TextField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    send_date = models.DateTimeField(blank=True, null=True)

    objects = NoticeManager()

    @property
    def sent(self):
        return self.send_date != None

    @property
    def subject_template_path(self):
        return os.path.join(self.notice_type.templates_path, 'subject.txt')

    @property
    def subject_body_path(self):
        return os.path.join(self.notice_type.templates_path, 'subject.txt')

    def __unicode__(self):
        return u'%s (%s)' % (self.notice_type.name, self.recipient.username)

    class Meta:
        verbose_name = _("notice")
        verbose_name_plural = _("notices")

    def send(self, passed_context):
        context = NoticeContext({'recipient': self.recipient})
        context.update(passed_context)

        self.email_subject = render_to_string(self.subject_template_path, context)
        self.email_body    = render_to_string(self.subject_body_path, context)
        self.save()

        email = EmailMessage(self.email_subject,
                             self.email_body,
                             self.sender,
                             [self.recipient.email])
        try:
            email.send()
            self.send_date = datetime.datetime.now()
            self.save()
        except smtplib.SMTPException as why:
            log.exception(why)

        return self.sent