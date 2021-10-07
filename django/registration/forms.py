"""
GN customisation of registraion form. The original code is in forms_reg.html

"""
from forms_reg import *

class RegistrationForm(RegistrationForm):
    terms = forms.BooleanField(required=True, )
    antispam = forms.CharField(required=False,)
    terms_fake = forms.BooleanField(required=False, )
    
    def clean_email(self):
        #ret = super(RegistrationForm, self).clean_email()
        from django.contrib.auth.models import User
        email = self.cleaned_data['email']
        users = User.objects.filter(email = email)
        if users.count() > 0:
            raise forms.ValidationError("This email address is already in use.")
        return email

    def clean_antispam(self):
        if self.cleaned_data['antispam']:
            raise forms.ValidationError("Please leave this field empty.")
        return self.cleaned_data['antispam']
            
    def clean_terms_fake(self):
        if self.cleaned_data['terms_fake']:
            raise forms.ValidationError("Please untick this checkbox.")
        return self.cleaned_data['terms_fake']
            
    def clean_terms(self):
        if not self.cleaned_data['terms']:
            raise forms.ValidationError("You must agree with the terms and conditions to create an account.")
        return self.cleaned_data['terms']

