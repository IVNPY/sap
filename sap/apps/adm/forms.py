from django.forms import ModelForm
from django.forms import Select
from django.forms import HiddenInput
from django.forms import IntegerField
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.forms import PasswordInput
from django.forms import ModelMultipleChoiceField
from django.contrib.auth.models import Permission
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from apps.adm.models import *
from apps.adm.utils import *

def get_permisos_sistema():
    perms = Permission.objects.all()
    perms = perms.exclude(content_type__app_label="auth")
    perms = perms.exclude(content_type__app_label="sessions")
    perms = perms.exclude(content_type__app_label="registration")
    perms = perms.exclude(content_type__app_label="contenttypes")
    perms = perms.exclude(content_type__app_label="admin")

    perms = perms.exclude(content_type__app_label="adm", content_type__model="permisosproyecto")

    perms = perms.exclude(content_type__app_label="adm", codename="add_permisossistema")
    perms = perms.exclude(content_type__app_label="adm", codename="change_permisossistema")
    perms = perms.exclude(content_type__app_label="adm", codename="delete_permisossistema")

    return perms

class RolSistemaForm(ModelForm):

    class Meta:
        model = Group

    permissions = ModelMultipleChoiceField(
        get_permisos_sistema(),
        widget=admin.widgets.FilteredSelectMultiple(('permissions'), False)
    )



"""
class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'permissions')
        widgets = {'permissions':ModelMultipleChoiceField(get_permisos_sistema(),widget=admin.widgets.FilteredSelectMultiple(('permissions'), False))}
"""
   
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
            'last_name' : 'Apellido' ,
            #'domicilio' : 'Domicilio',
            #'fechaNac' : 'Fecha de Nacimiento',
            #'telefono': 'Telefono',
            #'roles': 'Roles',
            'cliente':'Cliente'
        }
        help_texts = {
            'username': '',
            'password ':'',
            'email' : '',
            'first_name' : '' ,
            'last_name' : '' ,
            #'domicilio' : '',
            #'fechaNac' : '',
            #'telefono': '',
            #'roles': '',
            #'cliente':''
        }

class UserEditForm(ModelForm):
     class Meta:
        model = User
        fields = ['username','email','first_name','last_name' ]

        labels = {
            'username': 'Usuario',
            'email' : 'Email',
            'first_name' : 'Nombre' ,
            'last_name' : 'Apellido',
           # 'domicilio' : 'Domicilio',
            #'fechaNac' : 'Fecha de Nacimiento',
            #'telefono': 'Telefono',
           # 'roles': 'Roles',
            #'cliente':'Cliente'
        }
        help_texts = {
            'username': '',
            'email' : '',
            'first_name' : '' ,
            'last_name' : '' ,
            #'domicilio' : '',
           # 'fechaNac' : '',
           #  'telefono': '',
           # 'roles': '',
           # 'cliente':''
       }
     def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['username'].widget.attrs['readonly'] = True

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

class UserStoryForm(ModelForm):
    class Meta:
        model = UserStory
        fields = ['nombre','descripcion','detalle','valNegocio','valTecnico','usuario','prioridad','horasAcumuladas',
                  'estimacion']


        labels = {
            'nombre': 'Nombre',
            'descripcion ':'Descripcion',
            'detalle' : 'Detalle',
            #'sprint' : 'Sprint' ,
            'valNegocio' : 'Valor para el negocio',
            'valTecnico': 'Valor Tecnico',
            'usuario':'Usuario',
            'prioridad':'Prioridad',
            'horasAcumuladas':'Horas Acumuladas'
        }
        help_texts = {
            'nombre': '',
            'descripcion':'',
            'detalle' : '',
           # 'sprint' : '' ,
            'valNegocio' : '',
            'valTecnico' :'',
            'usuario':'',
            'prioridad':'',
            'horasAcumuladas':'',
            'estimacion':'',
            #'flujo':'',


        }

class UserStoryEditForm(ModelForm):
    class Meta:
        model = UserStory
        fields = ['nombre','descripcion','detalle','valNegocio','valTecnico','usuario','prioridad','horasAcumuladas',
                  'estimacion']


        labels = {
            'nombre': 'Nombre',
            'descripcion ':'Descripcion',
            'detalle' : 'Detalle',
            #'sprint' : 'Sprint' ,
            'valNegocio' : 'Valor para el negocio',
            'valTecnico': 'Valor Tecnico',
            'usuario':'Usuario',
            'prioridad':'Prioridad',
            'horasAcumuladas':'Horas Acumuladas'
        }
        help_texts = {
            'nombre': '',
            'descripcion':'',
            'detalle' : '',
            #'sprint' : '' ,
            'valNegocio' : '',
            'valTecnico' :'',
            'usuario':'',
            'prioridad':'',
            'horasAcumuladas':'',
            'estimacion':'',
            #'flujo':'',


        }

        def __init__(self, *args, **kwargs):
            super(UserStoryEditForm, self).__init__(*args, **kwargs)
            instance = getattr(self, 'instance', None)
            if instance and instance.pk:
                self.fields['usuario'].widget.attrs['readonly'] = True


