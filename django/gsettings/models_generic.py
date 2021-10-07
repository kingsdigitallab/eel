# -*- coding: utf-8 -*-
# auto generated from an XMI file
from django.db import models

from django.utils.encoding import force_unicode


def getUnicode(object):
	if (object == None):
		return u""
	else:
		return force_unicode(object)
		

#
class Global_Var(models.Model):
	name = models.CharField(max_length=128, null=False, default="", blank=False, help_text=ur'''Internal name of the variable. This name is used by the API to identify a variable.''', )
	label = models.CharField(max_length=128, null=False, default="", blank=True, help_text=ur'''Display name of the variable. This name is displayed in the simple edit interface.''', )
	value = models.CharField(max_length=1024, null=False, default="", blank=True, help_text=ur'''Value of this variable. Please make sure its format is compatible with the type of the variable.''', )
	unit = models.CharField(max_length=32, null=False, default="", blank=True, help_text=ur'''Unit of the value. (e.g. seconds, Bytes)''', )
	description = models.CharField(max_length=1024, null=False, default="", blank=True, help_text=ur'''This description is displayed in the simple edit interface.''', )
	global_var_category = models.ForeignKey('Global_Var_Category', blank=False, null=False, default=1, )
 	global_var_type = models.ForeignKey('Global_Var_Type', blank=False, null=False, default=1, )
 
	class Meta:
		verbose_name = 'Global Var'
		verbose_name_plural = 'Global Vars'
		unique_together = (( 'name', ),)
	
	def __unicode__(self):
		return getUnicode(self.name)

	table_group = ''


#
class Global_Var_Category(models.Model):
	name = models.CharField(max_length=128, null=False, default="", blank=False, help_text=ur'''''', )
	description = models.CharField(max_length=1024, null=False, default="", blank=True, )

	class Meta:
		verbose_name = 'Global Var Category'
		verbose_name_plural = 'Global Var Categories'
		unique_together = (( 'name', ),)
	
	def __unicode__(self):
		return getUnicode(self.name)

	table_group = ''


#
class Global_Var_Type(models.Model):
	name = models.CharField(max_length=32, null=False, default="", blank=False, )

	class Meta:
		verbose_name = 'Global Var Type'
		verbose_name_plural = 'Global Var Types'
		unique_together = (( 'name', ),)
	
	def __unicode__(self):
		return getUnicode(self.name)

	table_group = ''


# Many To Many Tables 
