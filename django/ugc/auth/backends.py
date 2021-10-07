from django.contrib.auth.backends import ModelBackend 

class EmailAuth(ModelBackend):

    def authenticate(self, username=None, password=None):
        user = None
        from django.contrib.auth.models import User
        users = User.objects.filter(email = username, web_user__isnull=False)
        if users.count() == 1:
            user = users[0]
            user = ModelBackend.authenticate(self, username=user.username, password=password)
        return user
    
    def get_user(self, user_id):
        return ModelBackend.get_user(self, user_id)
        