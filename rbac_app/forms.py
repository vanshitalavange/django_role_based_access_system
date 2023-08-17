from django import forms 

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=100)
    mobile = forms.IntegerField()
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.CharField(max_length=20)
    # confirm_password = forms.CharField(widget=forms.PasswordInput)

class UpdateUserForm(forms.Form):
    username = forms.CharField(max_length=100,required=False,initial=None)
    mobile = forms.IntegerField(required=False,initial=None)
    password = forms.CharField(widget=forms.PasswordInput,required=False,initial=None)
    role = forms.CharField(max_length=20,required=False)
    user_id = forms.IntegerField()

class DeletionForm(forms.Form):
    id = forms.IntegerField()


class AddAPIForm(forms.Form):
    name = forms.CharField(max_length=200)
    description = forms.CharField(max_length=200)
    endpoint = forms.CharField(max_length=100)
    method = forms.CharField(max_length=10)

class UpdateAPIForm(forms.Form):
    name = forms.CharField(max_length=200,required=False)
    description = forms.CharField(max_length=200,required=False)
    endpoint = forms.CharField(max_length=100,required=False)
    method = forms.CharField(max_length=10,required=False)
    api_id = forms.IntegerField()

class MapAPIForm(forms.Form):
    user_id = forms.IntegerField()
    api_id = forms.IntegerField()