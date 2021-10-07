#from django.conf import settings
#from django.template import Context, loader
import re
from django import http, template
from django.template.context import Context
from django.shortcuts import render_to_response
import ugc.forms as ugc_forms
from models import Web_User, User_Directory, Web_User_User_Directory
from django.http import HttpResponseRedirect
from cch.views.decorators import member_required

def login_view(request):
    template_name = 'login'
    form = None
    if request.method == 'POST':
        form = ugc_forms.LoginForm(request.POST)
        if form.is_valid():
            from django.contrib.auth import login
            # log the user in
            user = form.getUser()
            login(request, user)
            redirect = '/'
            if 'r' in request.REQUEST:
                redirect = request.REQUEST['r']
                if re.search('/(logout|login)/?$', redirect):
                    redirect = '/'
            return HttpResponseRedirect(redirect)
    else:
        form = ugc_forms.LoginForm()

    context = {'form': form}
    return get_template('registration/%s' % template_name, context, request)

def reset_password_view(request):
    template = 'registration/reset_password'
    if request.method == 'POST':
        form = ugc_forms.ResetPasswordForm(request.POST)
        if form.is_valid():
            # reset the password
            password = get_random_password()
            user = form.getUser()
            user.set_password(password)
            user.save()
            # send it via email
            from django.core.mail import send_mail
            message = '''
Your password has been reset. 

Here are your new connection details:

email address: %s
password: %s
            ''' % (form.getUser().email, password)
            send_mail('Your new password on Early English Laws', message, 'noreply@ootw.org', [user.email], fail_silently=False)
            # show confirmation screen
            template = 'registration/reset_password_confirmation'
    else:
        form = ugc_forms.ResetPasswordForm()
    return get_template(template, {'form': form}, request)

def get_random_password():
    righthand = 'qwertasdfgzxcb'
    lefthand = 'yphjklnm'
    from random import Random
    rnd = Random()
    ret = ''
    for i in range(8):
        if i%2:
            ret = ret + rnd.choice(lefthand)
        else:
            ret = ret + rnd.choice(righthand)
    return ret

def terms_view(request):
    return get_template('registration/terms', {}, request)

@member_required
def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return get_template('registration/logout', {}, request)

@member_required
def profile_view(request):
    form = None
    user = request.user    
    web_user = Web_User.objects.fromUser(user)
    user_to_directories = Web_User_User_Directory.objects.filter(web_user = web_user)
    
    if request.method == 'POST':
        if 'logout' in request.POST and request.POST['logout']:
            return logout_view(request)
        form = ugc_forms.ProfileForm(request.POST)
        if form.is_valid():
            # update the user
            password = form.cleaned_data['password1']
            if password is not None and len(password): 
                user.set_password(password)
            user.username = form.cleaned_data['display_name']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            
            web_user.contactable = form.cleaned_data['contactable']
            web_user.affiliations = form.cleaned_data['affiliation']
            web_user.biography = form.cleaned_data['biography']
            web_user.save()
            
            user_to_directories.delete()
            for dir in User_Directory.objects.filter(id__in=form.cleaned_data['directories']):
                user_to_dir = Web_User_User_Directory()
                user_to_dir.web_user = web_user
                user_to_dir.user_directory = dir
                user_to_dir.save()
            
            form.success = True
#            try:
#                user.save()
#            except:
#                form.
    else:
        form = ugc_forms.ProfileForm(initial={
                                              'display_name': user.username,
                                              'password1': '',
                                              'password2': '',
                                              'first_name': user.first_name,
                                              'last_name': user.last_name,
                                              'affiliation': web_user.affiliations,
                                              'biography': web_user.biography,
                                              'directories': [user_to_dir.user_directory.id for user_to_dir in user_to_directories],
                                              'contactable': web_user.contactable,
                                              })

    return get_template('registration/profile', {'form': form}, request)

'''
@member_required
def directory_view(request, url=None, record_type='author'):
    context = {'filters': []}
    
    # 1 Filters
    from ootw.plays.page_filters import Filter, FilterOption
    filters = context['filters']
    
    role = Filter('Role', 'role', request, 'link')
    FilterOption('Any', 0, role)
    for dir in User_Directory.objects.all().order_by('name'):
        FilterOption(dir.name, dir.id, role)
    filters.append(role)
    
    # 2 pagination
    # TODO: don't underline the pages which don't have any records under them.
#    context['pages'] = Filter('pages', 'pg', request, 'az')
#    for letter in [chr(i) for i in range(ord('A'), ord('Z') + 1)]:
#        FilterOption(letter, letter, context['pages'])
    
    # 2 Query
    context['records'] = None
    # role
    dirid = int(role.get_value())
    if dirid == 0:
        context['records'] = Web_User.objects.filter(user_directory__id__gt = 0).distinct()
    else:
        context['records'] = Web_User.objects.filter(user_directory__id = dirid)
    
    # pagination filter
    context['pages'] = get_az_filter(request, context['records'].filter(user__last_name__isnull = False), 'last_name') 
    
    # last name starts with
    context['records'] = context['records'].filter(user__last_name__istartswith = context['pages'].get_value())
    
    # order
    context['records'] = context['records'].order_by('user__last_name')
    
    return get_template('directory/directory', context, request)

@member_required
def dashboard_view(request):
    context = {}
    from ootw.plays.page_filters import FilterWebPath
    tabs = FilterWebPath('Tabs', '/dashboard', request, 'tab', (
                                                         ('Recently viewed', ''),
                                                         ('My bookmarks', 'bookmarks'),
                                                         ('My comments', 'comments'),
                                                         ('My submissions', 'submissions'),
                                                         ))
    context['tabs'] = tabs
    
    if tabs.get_value() == '':
        from ootw.ugc.activity_cookie import ActivityCookie
        context['activity'] = ActivityCookie(request)

    if tabs.get_value() == 'bookmarks':
        from ootw.user_bookmark.models import UserBookmark
        
        if 'rbm' in request.REQUEST:
            bookmarkid = int(request.REQUEST['rbm'])
            UserBookmark.objects.filter(user = request.user, id = bookmarkid).delete()
        
        context['records'] = UserBookmark.objects.filter(user = request.user).order_by('-create_timestamp')
    
    if tabs.get_value() == 'comments':
        from ootw.comments_section.models import CommentSection
        
        context['records'] = CommentSection.objects.filter(user = request.user).order_by('-submit_date')
        for record in context['records']:
            if len(record.section) > 0:
                record.play_tab_path = u'/' + record.section

    if tabs.get_value() == 'submissions':
        from ootw.plays.models import User_Submission
        context['records'] = User_Submission.objects.filter(user = request.user).order_by('-creation_date')

    template_name = tabs.get_value()
    if len(template_name) == 0: template_name = 'activity'

    return get_template('dashboard/%s' % template_name, context, request)    
'''

def get_template(path, context, request):
    return render_to_response(path+'.html', Context(context), context_instance=template.RequestContext(request))

