django-scooby: email notifications
==================================

django-scooby is a minimalistic Django application for sending email notifications.

Features
--------

- Sending notification emails on plain text and HTML
- Management of sent notices
- Sending emails on the background (powered by celery)

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

Run ``manage.py syncdb`` afterwards so that required models are created.

Setup `email settings <https://docs.djangoproject.com/en/dev/topics/email/>`_ if you havent already:

.. code-block:: python

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'your_email_host'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = 'your_user'
    EMAIL_HOST_PASSWORD = 'your_password'
    EMAIL_NOTIFICATION_SUBJECT_PREFIX = '[MyApp] '
    DEFAULT_FROM_EMAIL = 'notices@mydomain.com'

Usage
-----

Suppose you have an application called ``announcements`` and you want to send email
notifications whenever a new announcement is added. First lets name the notice, say ``announcement_added``.

Where to put the templates
~~~~~~~~~~~~~~~~~~~~~~~~~~

The email templates must be inside ``appname/templates/notices/notice_name``. For instance, in our example we must have: ::

    » cd announcements && tree
    .
    ├── __init__.py
    ├── admin.py
    ├── forms.py
    ├── models.py
    ├── templates
    │   └── notices
    │       └── announcement_added
    │           ├── body.txt             <--- Body of the email in plain text
    │           ├── body.html            <--- Body of the email (HTML version) (optional)
    │           └── subject.txt          <--- Subject of the email
    ├── tests.py
    ├── urls.py
    ├── views.py

Notice the ``templates/notices/announcement_added`` folder. In our example, we may simply create it with: ::

    $ cd announcements
    $ mkdir -p templates/notices/announcement_added

Template variables
~~~~~~~~~~~~~~~~~~

The templates have access the following variables:

- ``recipient``: the User receiving this notification.
- ``site``: name of the current ``Site``
- ``site_url``: URL for the current ``Site`` (e.g. http://www.example.com)
- ``STATIC_URL`` and ``MEDIA_URL`` (just like Django)
- Any extra variables can be passed on the ``context`` parameter of ``scooby.send()``

With this in mind, we write a simple email for our notification as follows.

subject.txt:

::

    New announcement


body.txt:

::

    Hello {{ recipient.get_full_name }},

    A new announcement was just published:

    {{ announcement.text }}

    View it online: {{ site_url }}{% url announcements.views.show announcement.id %}


``body.html`` is optional and ommited here.


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

Send functions (API)
--------------------

``scooby.send(notice_type_name, recipient[, context[, sender=None]])``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Blocking call that sends a notification to a single user or a list of users.

- ``notice_type_name``: name of the notice. Should match a folder 'notice/<notice_type_name>' on the template path
- ``recipient``: User instance or list of User instances
- ``context``: context data dict passed to the notice template. Pass extra variables to the template here.
- ``sender``: email's from field. If not present, notices will use settings.DEFAULT_FROM_EMAIL

``scooby.queue(notice_type_name, recipient[, context[, sender=None]])``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Background call that sends a notification to a single user or a list of users.

- ``notice_type_name``: name of the notice. Should match a folder 'notice/<notice_type_name>' on the template path
- ``recipient``: User instance or list of User instances
- ``context``: context data dict passed to the notice template. Pass extra variables to the template here.
- ``sender``: email's from field. If not present, notices will use settings.DEFAULT_FROM_EMAIL

Requirements:
- `django-celery <https://github.com/celery/django-celery/>`_ must be installed appropriately.
- RabbitMQ must be running on localhost
- There must be at least one worker running for 'scooby.celery.tasks': ::

  ``python manage.py celery -A scooby.celery.tasks worker --loglevel=INFO``.

Credits
-------

This project was highly inspired and based on `jtauber <https://github.com/jtauber/django-notification>`_ and `synasius <https://github.com/synasius/django-notification>`_ django-notification projects.
