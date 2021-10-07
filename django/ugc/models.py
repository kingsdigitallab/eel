# -*- coding: utf-8 -*-
# auto generated from an XMI file
# from django.db import models
import datetime
import random
import re

from django.conf import settings
from models_generic import *
from managers import RegistrationManager
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
#from ootw.ugc.models import Web_User as RegistrationProfile
import split_record_ids

# Nasty hack. 
# object attribute should be defined in the model class.
# however this is not supported by uml-to-django.
# so we do it after the class has been declared.
# Problem is... django casts does some python black magic during the model class creation
# so we reproduce it here with contribute_to_class(). 
# Without that call the manager would not have a model attribute pointing to the model class.
Web_User.objects = RegistrationManager()
Web_User.objects.contribute_to_class(Web_User, 'objects')

Web_User.ACTIVATED = u"ALREADY_ACTIVATED"

def RegistrationManager_from_user(self, user):
    ''' Works like get_profile() except that if the profile does not exist, it will be created '''
    ret = self.none()
    if user is not None:
        ret = self.filter(user = user)
        if ret.count() == 0:
            # create the missing web user record and activate it
            ret = self.create_profile(user)
            ret.activation_key = self.model.ACTIVATED
            ret.save()
        else:
            ret = ret[0]
    return ret

RegistrationManager.fromUser = RegistrationManager_from_user

def web_user_get_directories(self):
    return User_Directory.objects.filter(web_user = self)
Web_User.getDirectories = web_user_get_directories

def web_user_activation_key_expired(self):
    """
    Determine whether this ``RegistrationProfile``'s activation
    key has expired, returning a boolean -- ``True`` if the key
    has expired.
    
    Key expiration is determined by a two-step process:
    
    1. If the user has already activated, the key will have been
       reset to the string constant ``ACTIVATED``. Re-activating
       is not permitted, and so this method returns ``True`` in
       this case.

    2. Otherwise, the date the user signed up is incremented by
       the number of days specified in the setting
       ``ACCOUNT_ACTIVATION_DAYS`` (which should be the number of
       days after signup during which a user is allowed to
       activate their account); if the result is less than or
       equal to the current date, the key has expired and this
       method returns ``True``.
    
    """
    expiration_date = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
    return self.activation_key == self.ACTIVATED or \
           (self.user.date_joined + expiration_date <= datetime.datetime.now())
web_user_activation_key_expired.boolean = True

def web_user_send_activation_email(self, site):
    """
    Send an activation email to the user associated with this
    ``RegistrationProfile``.
    
    The activation email will make use of two templates:

    ``registration/activation_email_subject.txt``
        This template will be used for the subject line of the
        email. Because it is used as the subject line of an email,
        this template's output **must** be only a single line of
        text; output longer than one line will be forcibly joined
        into only a single line.

    ``registration/activation_email.txt``
        This template will be used for the body of the email.

    These templates will each receive the following context
    variables:

    ``activation_key``
        The activation key for the new account.

    ``expiration_days``
        The number of days remaining during which the account may
        be activated.

    ``site``
        An object representing the site on which the user
        registered; depending on whether ``django.contrib.sites``
        is installed, this may be an instance of either
        ``django.contrib.sites.models.Site`` (if the sites
        application is installed) or
        ``django.contrib.sites.models.RequestSite`` (if
        not). Consult the documentation for the Django sites
        framework for details regarding these objects' interfaces.

    """
    from gsettings.context_processor import _get_vars_as_context
    ctx_dict = { 'activation_key': self.activation_key,
                 'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                 'site': site,
                 'gsettings': _get_vars_as_context()}
    subject = render_to_string('registration/activation_email_subject.txt',
                               ctx_dict)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    
    message = render_to_string('registration/activation_email.txt',
                               ctx_dict)
    
    self.user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

Web_User.activation_key_expired = web_user_activation_key_expired
Web_User.send_activation_email = web_user_send_activation_email
