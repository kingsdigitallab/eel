# -*- coding: utf-8 -*-
# auto generated from an XMI file
from django.db import models

from django.utils.encoding import force_unicode

# Referenced by a foreign key 
import django.contrib.auth.models

def getUnicode(object):
	if (object == None):
		return u""
	else:
		return force_unicode(object)
		

#
class Web_User(models.Model):
	affiliations = models.CharField(max_length=255, null=False, default="", blank=True, )
	biography = models.XMLField(null=False, default="", blank=True, )
	user = models.ForeignKey(django.contrib.auth.models.User, unique=True, )
	activation_key = models.CharField(max_length=128, null=False, default="", blank=True, )
	contactable = models.BooleanField(default=False, null=False, blank=False, )

	class Meta:
		verbose_name = 'Web User'
		verbose_name_plural = 'Web Users'
		

	table_group = ''


#
class User_Directory(models.Model):
	name = models.CharField(max_length=128, null=False, default="", blank=False, )
	css_class = models.CharField(max_length=32, null=False, default="", blank=True, )
	web_user = models.ManyToManyField('Web_User', blank=True, null=True, through='Web_User_User_Directory', )
 
	class Meta:
		verbose_name = 'User Directory'
		verbose_name_plural = 'User Directories'
		unique_together = (( 'name', ),)
	
	def __unicode__(self):
		return getUnicode(self.name)

	table_group = ''


# Many To Many Tables 

#
class Web_User_User_Directory(models.Model):
	web_user = models.ForeignKey('Web_User')
	user_directory = models.ForeignKey('User_Directory')
