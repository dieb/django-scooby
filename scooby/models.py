# -*- coding: utf-8 -*-
import os
import smtplib
import datetime
import logging

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, EmailMultiAlternatives

from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string, get_template

from django.utils.translation import ugettext_noop as _

from .context import NoticeContext

log = logging.getLogger(__name__)


__all__ = ('NoticeType', 'Notice')


class NoticeType(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

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
    email_txt_body = models.TextField(blank=True, null=True)
    email_html_body = models.TextField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    send_date = models.DateTimeField(blank=True, null=True)

    objects = NoticeManager()

    @property
    def sent(self):
        return self.send_date != None

    def __unicode__(self):
        return u'%s (%s)' % (self.notice_type.name, self.recipient.username)

    class Meta:
        verbose_name = _("notice")
        verbose_name_plural = _("notices")

    def send(self, passed_context):
        context = NoticeContext({'recipient': self.recipient})
        context.update(passed_context)

        if hasattr(settings, 'EMAIL_NOTIFICATION_SUBJECT_PREFIX'):
            subject_prefix = settings.EMAIL_NOTIFICATION_SUBJECT_PREFIX
        else:
            subject_prefix = ''

        recipients = [self.recipient.email]

        txt_subject  = os.path.join(self.notice_type.templates_path, 'subject.txt')
        txt_body     = os.path.join(self.notice_type.templates_path, 'body.txt')
        html_body    = os.path.join(self.notice_type.templates_path, 'body.html')

        self.email_subject  = (subject_prefix + render_to_string(txt_subject, context)).strip()
        self.email_txt_body = render_to_string(txt_body, context)

        try:
            get_template(html_body)
            has_html_body = True
        except TemplateDoesNotExist:
            has_html_body = False

        if has_html_body:
            self.email_html_body = render_to_string(html_body, context)
            email = EmailMultiAlternatives(self.email_subject, self.email_txt_body,
                                           self.sender, recipients)
            email.attach_alternative(self.email_html_body, "text/html")
        else:
            email = EmailMessage(self.email_subject, self.email_txt_body,
                                 self.sender, recipients)

        try:
            email.send()
            self.send_date = datetime.datetime.now()
            self.save()
        except smtplib.SMTPException as why:
            log.exception(why)

        return self.sent

    def queue(self, passed_context):
        from django.conf import settings
        assert 'djcelery' in settings.INSTALLED_APPS, "'djcelery' must be installed on your app before using queue()."
        from scooby.celery.tasks import send_notice

        return send_notice.delay(self, passed_context)