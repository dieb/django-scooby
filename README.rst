django-scooby: email notifications
==================================

django-scooby is a minimalistic Django application for sending email notifications.

Features
--------

- Sending notification emails
- No dependencies

Installation
------------

Add it to your PYTHONPATH

Settings
--------

Add ``scooby`` to the ``INSTALLED_APPS`` in your settings.py file of your project.

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django.contrib.sessions',
        'django.contrib.sites',
        ...

        'scooby',
        )

Set a default from address for sending emails in your settings.py:

.. code-block:: python

    DEFAULT_FROM_EMAIL = 'no-repy@mydomain.com'

This will be used when you don't specify the sender when sending notifications.

Usage
-----

Suppose you have an application in your project called ``announcements`` and you want to send email
notifications whenever a new announcement is added.

First you need to name your notice, say ``announcement_added``.

Scooby works with a fixed folder structure for the emails. Simply create it with: ::

    $ cd announcements
    $ mkdir -p templates/notices/announcement_added
    $ vi templates/notices/announcement_added/subject.txt
    $ vi templates/notices/announcement_added/body.txt

Note that ``subject.txt`` will be your email subject title and of course ``body.txt`` the body.

These templates receive at least one variable named ``recepient`` which contains the User receiving this notification.

They also receive extra variables you pass when creating the new notification:

.. code-block:: python

    # views.py
    from scooby import send as notification_send

    def announcement_new(request):
        announcement = Announcement()
        announcement.save()

        notification_send('announcement_added', user, {'announcement': announcement})


Now write a pretty subject.txt:

::

    New announcement


Also a body:

::

    Hello {{ recipient.get_full_name }},

    A new announcement was just published:

    {{ announcement.text }}

    View it online: http://{{ current_site }}{% url announcements.views.show announcement.id %}


And that's all.