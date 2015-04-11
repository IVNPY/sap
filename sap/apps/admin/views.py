# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth import authenticate, login ,logout

#Models del modulo de autenticacion de django
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User

# Views de tipo clase de django
from django.views.generic import ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.core.urlresolvers import  reverse
from django.db.models import Q

from datetime import date

from apps.admin.forms import UsuarioRolForm
from apps.admin.forms import UserForm
from apps.admin.forms import GroupForm

from apps.admin.utils import *


#TEMPL_LOGINFORM = 'admin/form_login.html'
#TEMPL_PROYECTOFORM = 'admin/form_proyecto.html'
#TEMPL_PROYECTOLISTA = 'admin/lista_proyectos.html'
#TEMPL_FASEFORM ='admin/form_fase.html'
#TEMP_PERM_LIST ='admin/lista_permisos.html'
#TEMPL_USERFORM = 'admin/form_user.html'
#TEMPL_LIST_USER = 'admin/listar_usuarios.html'
#TEMPL_ROLPERMS_FORM = "admin/form_rolespermisos.html" 
#TEMPL_ROLES_LIST = "admin/lista_roles.html"
#TEMPL_ASIG_ROL_USER = 'admin/form_asignarol.html'
#TEMPL_DELCONFIRM = 'form_confirm_delete.html'
#ABM_ACCIONES = ('editar', 'eliminar', 'crear')
#nombre de la variable de sesion que almacena los permisos
#SESS_PERMS = 'permisos'


class CrearUsuarioView(CreateView):
    """
    Despliega el formulario para la carga de usuarios y 
    persiste un nuevo usuario.
    
    """
    model= User
    template_name = 'admin/crear_usuario.html'
    form_class = UserForm
    templ_base_error = None
    next = 'listar_usuario'
    
    def get_success_url(self):
        return reverse(self.next)
    
    def get_context_data(self, **kwargs):
        context = super(CrearUsuarioView, self).get_context_data(**kwargs)
        context['action'] = reverse('crear_usuario')
        if self.templ_base_error:
            context['nodefault'] = self.templ_base_error
        return context

    def form_invalid(self, form):
        self.templ_base_error = "__panel.html"
        return CreateView.form_invalid(self, form)
        
    def form_valid(self, form):
        #user = User.objects.create_user('x', 'x.com', self.request.POST.get('password'))
        form.instance.set_password(self.request.POST.get('password'))
        return CreateView.form_valid(self, form)


class EliminarUsuarioView(DeleteView):
    """    
    Solicita confirmacion para eliminar y elimina el usuario
    """
    model = User
    template_name = 'admin/eliminar_usuario.html'

    def get_success_url(self):
        return reverse('listar_usuario')

    def get_context_data(self, **kwargs):
        context = DeleteView.get_context_data(self, **kwargs)
        context['action'] = reverse('eliminar_usuario',kwargs={'pk':self.kwargs['pk']})
        return context


class ModificarUsuarioView(UpdateView):
    """
    Permite modificar los atributos del usuario.
    """
    model = User
    form_class = UserForm
    template_name = 'admin/modificar_usuario.html'
    templ_base_error = None
    next = 'listar_usuario'

    def get_success_url(self):
        return reverse(self.next)
    
    def form_invalid(self, form):
        self.templ_base_error = "__panel.html"
        return UpdateView.form_invalid(self, form)

    def get_context_data(self, **kwargs):
        context = UpdateView.get_context_data(self, **kwargs)
        context['action'] = reverse('modificar_usuario',kwargs={'pk':self.kwargs['pk']})
        if self.templ_base_error:
            context['nodefault'] = self.templ_base_error
        return context


class ListarUsuarioView(ListView):
    """
    Despliega una lista de usuarios registrados en el sistema.
    Puede emitir una lista completa o bien una lista acotada por la busqueda 
    de usuarios por nombre y apellido.
    """
    model= User
    template_name = 'admin/listar_usuarios.html'

    def get_queryset(self):
        busqueda = self.request.GET.get('busqueda','')
        if (busqueda != ''):
            object_list = self.model.objects.filter(Q(first_name__icontains=busqueda) | 
                                              Q(last_name__icontains=busqueda))
            if object_list.count > 1:
                messages.info(self.request, 'Resultados con : ' + busqueda)
        else:
            object_list = self.model.objects.all()
        return object_list

@login_required
def consultarUsuario(request, pk):
    """
    Consulta los datos de un usuario.
    Que Roles posee , y que permisos tiene asignados por medio de esos roles.
    """
    context = RequestContext(request)
    usuario = get_object_or_404(User, pk=pk)
    return render_to_response('admin/detalle_usuario.html', {'usuario': usuario}, context)

@login_required
def crearRol(request):
    """
    Funcion para crear un rol.
    Retorna la pagina con el formulario correspondiente para la creacion
    del rol.
    """
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        group_form = GroupForm(data=request.POST)
        if group_form.is_valid():
            group = group_form.save()
            group.save()
            registered = True
        else:
            print group_form.errors

    else:
        group_form = GroupForm()

    return render_to_response('admin/crear_rol.html', {'group_form': group_form, 'registered': registered}, context)

@login_required
def modificarRol(request, pk):
    context = RequestContext(request)
    group = get_object_or_404(Group, pk=pk)
    group_form = GroupForm(request.POST or None, instance=group)
    if group_form.is_valid():
        group_form.save()
        return redirect('listar_rol')

    return render_to_response('admin/modificar_rol.html', {'groupform': group_form}, context)

@login_required
def eliminarRol(request, pk):
    """Funcion para Eliminar un rol.

    :param request: Parametro a ser procesado.
    :param pk: Parametro a ser procesado el identificador del rol que va a eliminarse.
    :type request: HttpRequest.
    :type pk: int.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    context = RequestContext(request)
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        group.delete()
        return redirect('listar_rol')

    return render_to_response('admin/eliminar_rol.html', {'object':group}, context)

@login_required
def listarRol(request):
    """
    Funcion para listar roles.
    Retorna la pagina correspondiente con la lista de roles registrados.
    """

    context = RequestContext(request)
    group_list = get_group_list()
    context_dict = {}
    context_dict['object_list'] = group_list

    return render_to_response('admin/listar_rol.html', context_dict, context)

@login_required
def consultarRol(request, pk):

    context = RequestContext(request)
    rol = get_object_or_404(Group, pk=pk)
    context_dict = {'rol': rol}

    return render_to_response('admin/detalle_rol.html', context_dict, context)


class AsignarRolesSistema(UpdateView):
    """   
    Permite asignar o desasignar roles de sistema a un usuario.
    """
    model = User
    form_class = UsuarioRolForm
#    TEMPL_ASIG_ROL_USER = 'admin/form_asignarol.html'
    template_name = 'admin/asignar_roles_sistema.html'
    next = 'listar_usuario'

    def get_success_url(self):
        return reverse(self.next)
    
    def get_context_data(self, **kwargs):
        context = UpdateView.get_context_data(self, **kwargs)
        context['idgrupo'] = self.kwargs['pk']
        return context




