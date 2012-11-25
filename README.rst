django-scooby: email notifications
==================================

django-scooby is a minimalistic Django application for sending email notifications.

Features
--------

- Sending notification emails
- No dependencies

Installation
------------

For now please clone and add the 'scooby' folder to your PYTHONPATH. Once it reaches some stability I will definitely make it available via pip.

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

    DEFAULT_FROM_EMAIL = 'no-reply@mydomain.com'

This will be used when you don't specify the sender when sending notifications.

Usage
-----

Suppose you have an application in your project called ``announcements`` and you want to send email
notifications whenever a new announcement is added.

First you need to name your notice, say ``announcement_added``.

Where to put the templates
~~~~~~~~~~~~~~~~~~~~~~~~~~

Scooby works with a fixed folder for the emails, which is ``appname/templates/notices/notice_name``. For instance, in our example, we must have: ::

    » cd announcements && tree
    .
    ├── __init__.py
    ├── admin.py
    ├── forms.py
    ├── models.py
    ├── templates
    │   └── notices
    │       └── announcement_added
    │           ├── body.txt
    │           └── subject.txt
    ├── tests.py
    ├── urls.py
    ├── views.py

Notice the ``templates/notices/announcement_added`` folder. In our example, we may simply create it with: ::

    $ cd announcements
    $ mkdir -p templates/notices/announcement_added
    $ vi templates/notices/announcement_added/subject.txt
    $ vi templates/notices/announcement_added/body.txt

Template variables
~~~~~~~~~~~~~~~~~~

The templates (subject.txt, body.txt) have access the following variables:

- ``recipient``: the User receiving this notification.
- ``site``: name of the current ``Site``
- ``site_url``: URL for the current ``Site`` (e.g. http://www.example.com)
- ``STATIC_URL`` and ``MEDIA_URL`` (just like Django)
- Extra variables can be passed on the ``scooby.send()``

With this in mind, we can write a simple email for our notification as follows.

subject.txt:

::

    New announcement


body.txt:

::

    Hello {{ recipient.get_full_name }},

    A new announcement was just published:

    {{ announcement.text }}

    View it online: {{ site_url }}{% url announcements.views.show announcement.id %}

Wiring it up
~~~~~~~~~~~~

With the templates on the correct folder, you may send the notifications with:

.. code-block:: python

    # views.py
    from scooby import send as notification_send

    def announcement_new(request):
        announcement = Announcement()
        announcement.save()

        notification_send('announcement_added',
                          user,
                          {'announcement': announcement})

Note that you can pass extra data to the template (such as ``announcement``).