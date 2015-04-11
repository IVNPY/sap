from django.forms import ModelForm
from django.forms import Select
from django.forms import HiddenInput
from django.forms import IntegerField
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.forms import PasswordInput

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'permissions')


        
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','password','email','first_name','last_name' ]
        widgets = {'password':PasswordInput()}
        
        labels = {
            'username': 'Usuario',
            'password ':'Contrasenha',
            'email' : 'Email',
            'first_name' : 'Nombre' ,
            'last_name' : 'Apellido' 
        }
        help_texts = {
            'username': '',
            'password ':'',
            'email' : '',
            'first_name' : '' ,
            'last_name' : '' 
        }


class PermisosRolesForm(ModelForm):
    class Meta:
        model = Group
        fields =['permissions']


class UsuarioRolForm(ModelForm):
    class Meta:
        model = User
        fields =['groups']
        labels = {
            'groups':'Roles'
        }
        help_texts = {
            'groups':''
        }

