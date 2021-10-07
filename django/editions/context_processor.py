from django.conf import settings
#from ootw.debug import log


def settings_vars(request):
    #menu_man.setRequest(request)
    userid = 0
    if request and request.user and request.user.id > 0:
        userid = request.user.id
    return {
        'custom_admin_media_prefix': settings.CUSTOM_ADMIN_MEDIA_PREFIX,
        'custom_web_media_prefix': settings.CUSTOM_WEB_MEDIA_PREFIX,
        'DJANGO_WEBPATH_PREFIX': '/' + settings.DJANGO_WEBPATH_PREFIX,
        #'menu_manager': menu_man,
        'DJANGO_WEBPATH_PREFIX_MEMBERS': '/' + settings.DJANGO_WEBPATH_PREFIX_MEMBERS,
        'UGC_ENABLED': settings.UGC_ENABLED,
        'ADMINS': settings.ADMINS,
        'request': request,
        'userid': userid,
    }
