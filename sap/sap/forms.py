from django import forms

class LoginForm(forms.Form):
    ''' Clase encargada del formulario de login '''
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
