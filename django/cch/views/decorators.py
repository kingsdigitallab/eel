from django.http import HttpResponseRedirect

def member_required(view_func):
    """
    Decorator for views that checks that the user is logged in, 
    displaying the login page if necessary.
    """
    def _checklogin(request, *args, **kwargs):
        if request.user.is_authenticated():
            # The user is valid. Continue to the admin page.
            return view_func(request, *args, **kwargs)

        # TODO: include ?r= in the url
        return HttpResponseRedirect('/users/login?r=%s' % request.get_full_path())

    return _checklogin