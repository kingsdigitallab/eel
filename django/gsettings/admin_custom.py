# auto generated from an XMI file
# this file can be edit, 
# make sure it is renamed into "admin_custom.py" (without the underscore at the beginning)
from models import *
from admin_generic import *
from django.contrib import admin
 

#
class Global_VarAdmin(Global_VarAdmin):
	#form = Global_Var_TypeForm
	
	save_on_top = True
	
	fieldsets = (
		('Value', {'fields' : ('name', 'value')}),
		('Metadata', {'fields' : ('label', 'unit', 'description', 'global_var_type', 'global_var_category', )}),
	)
	
	ordering = ('name',)

	#inlines = (Global_Var_CategoryInline,)
	
	# translator? author? director?
	list_display = ('id', 'global_var_category', 'label', 'name', 'value', 'unit')
	list_display_links = list_display
		
	search_fields = ['name', 'global_var_category__name', 'value', ]
	
	# TODO: improve date of birth selection
	list_filter = ['global_var_category']

#
class Global_Var_CategoryAdmin(Global_Var_CategoryAdmin):
	pass
	
#
class Global_Var_TypeAdmin(Global_Var_TypeAdmin):
	pass