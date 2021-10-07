from django import forms

class LoginForm(forms.Form):
    login_name = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    
    def clean(self):
        super(LoginForm, self).clean()
        if self.is_valid():
            user = None
            from django.contrib.auth import authenticate
            candidate_user = self.get_user_from_email_or_name(self.cleaned_data['login_name'])
            if candidate_user:
                user = authenticate(username=candidate_user.username, password=self.cleaned_data['password'])
            if user is None:
                raise forms.ValidationError('Incorrect password or email address. Please try again.')
            else:
                self.user = user
        return self.cleaned_data
    
    def getUser(self):
        ''' Returns the user which has entered its proper details '''
        return getattr(self, 'user', None)

    def get_user_from_email_or_name(self, identifier):
        ret = None
        from django.contrib.auth.models import User
        users = User.objects.filter(email=identifier)
        if users.count() == 0:
            users = User.objects.filter(username=identifier)
        if users.count():
            ret = users[0]
        return ret
            
class ResetPasswordForm(forms.Form):
    login_name = forms.CharField(max_length=100)
    
    def clean_login_name(self):
        from django.contrib.auth.models import User
        users = User.objects.filter(email=self.cleaned_data['login_name'])
        if users.count() != 1:
            raise forms.ValidationError('No user is registered with this email address. Please make sure your address is spelled correctly.')
        else:
            self.user = users[0]
        return self.cleaned_data['login_name']

    def getUser(self):
        ''' Returns the user which has entered its proper details '''
        return getattr(self, 'user', None)

class ProfileForm(forms.Form):
    display_name = forms.CharField(max_length=30)
    password1 = forms.CharField(required=False, max_length=20, widget=forms.PasswordInput)
    password2 = forms.CharField(required=False, max_length=20, widget=forms.PasswordInput)
    first_name = forms.CharField(required=False, max_length=50)
    last_name = forms.CharField(required=False, max_length=50)
    affiliation = forms.CharField(required=False, max_length=255)
    biography = forms.CharField(required=False, max_length=1024, widget=forms.Textarea)
    directories = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple)
    contactable = forms.BooleanField(required=False)
    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.setDirectoriesChoices() 
    
    def setDirectoriesChoices(self):
        from models import User_Directory
        self.fields['directories'].choices = [[dir.id, u'%s directory' % dir.name] for dir in User_Directory.objects.all().order_by('name')]

    def clean(self):
        super(ProfileForm, self).clean()
        if self.is_valid():
            if len(self.cleaned_data['password1']) > 0 and self.cleaned_data['password2'] != self.cleaned_data['password1']:
                raise forms.ValidationError('Both passwords must match.')
            else:
                #self.user = user
                pass
        return self.cleaned_data
    
