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

from apps.adm.forms import *
from apps.adm.models import *
from apps.adm.utils import *

class CrearUsuarioView(CreateView):
    """
    Despliega el formulario para la carga de usuarios y 
    persiste un nuevo usuario.
    
    """
    model= User
    template_name = 'adm/crear_usuario.html'
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
    template_name = 'adm/eliminar_usuario.html'

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
    form_class = UserEditForm
    template_name = 'adm/modificar_usuario.html'
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
    template_name = 'adm/listar_usuarios.html'

    def get_queryset(self):
        busqueda = self.request.GET.get('busqueda','')
        if (busqueda != ''):
            object_list = self.model.objects.filter(Q(username__icontains=busqueda) | 
                                                    Q(first_name__icontains=busqueda) | 
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
    return render_to_response('adm/detalle_usuario.html', {'usuario': usuario}, context)

@login_required
def crearRol(request):
    """
    Funcion para crear un rol.
    Retorna la pagina con el formulario correspondiente para la creacion
    del rol.
    """
    context = RequestContext(request)
    if request.method == 'POST':
        group_form = RolSistemaForm(data=request.POST)
        if group_form.is_valid():
            group = group_form.save()
            group.save()
            return redirect('listar_rol')
        else:
            print group_form.errors
    else:
        group_form = RolSistemaForm()

    return render_to_response('adm/crear_rol.html', {'group_form': group_form}, context)

@login_required
def modificarRol(request, pk):
    context = RequestContext(request)
    group = get_object_or_404(Group, pk=pk)
    group_form = RolSistemaForm(request.POST or None, instance=group)
    if group_form.is_valid():
        group_form.save()
        return redirect('listar_rol')

    return render_to_response('adm/modificar_rol.html', {'groupform': group_form}, context)

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

    return render_to_response('adm/eliminar_rol.html', {'object':group}, context)

class ListarRolView(ListView):
    """
    
    Lista todos los roles o el resultado de una busqueda. 
    La busqueda se realiza por el nombre del rol 
    
    """
    model = Group
    template_name = 'adm/listar_rol.html'

    def get_queryset(self):
        busqueda = self.request.GET.get('busqueda','')
        if (busqueda != ''):
            object_list = self.model.objects.filter(name__icontains=busqueda)
            if object_list.count > 1:
                messages.info(self.request, 'Resultados con : ' + busqueda)
        else:
            object_list = self.model.objects.all()
        return object_list

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        return context

@login_required
def consultarRol(request, pk):

    context = RequestContext(request)
    rol = get_object_or_404(Group, pk=pk)
    context_dict = {'rol': rol}

    return render_to_response('adm/detalle_rol.html', context_dict, context)

class ListarUsuariosAsignarRolSistemaView(ListView):
    """
    Despliega una lista de usuarios registrados en el sistema.
    Puede emitir una lista completa o bien una lista acotada por la busqueda 
    de usuarios por nombre y apellido.
    """
    model= User
    template_name = 'adm/listar_usuarios_asignar_rol_sistema.html'

    def get_queryset(self):
        busqueda = self.request.GET.get('busqueda','')
        if (busqueda != ''):
            object_list = self.model.objects.filter(Q(first_name__icontains=busqueda) |
                                                    Q(last_name__icontains=busqueda) |
                                                    Q(username__icontains=busqueda))
            if object_list.count > 1:
                messages.info(self.request, 'Resultados con : ' + busqueda)
        else:
            object_list = self.model.objects.all()
        return object_list


class AsignarRolesSistema(UpdateView):
    """   
    Permite asignar o desasignar roles de sistema a un usuario.
    """
    model = User
    form_class = UsuarioRolForm
    template_name = 'adm/asignar_roles_sistema.html'
    next = 'listar_usuario_asignar_rol_sistema'

    def get_success_url(self):
        return reverse(self.next)
    
    def get_context_data(self, **kwargs):
        context = UpdateView.get_context_data(self, **kwargs)
        context['idgrupo'] = self.kwargs['pk']
        return context

#Para User Story


class ListarUserStoryView(ListView):
    """

    Lista todos los user stories o el resultado de una busqueda.
    La busqueda se realiza por el nombre del user story

    """
    model = UserStory
    template_name = 'adm/listar_user_story.html'

    def get_queryset(self):
        busqueda = self.request.GET.get('busqueda','')
        if (busqueda != ''):
            object_list = self.model.objects.filter(nombre__icontains=busqueda)
            if object_list.count > 1:
                messages.info(self.request, 'Resultados con : ' + busqueda)
        else:
            object_list = self.model.objects.all()
        return object_list

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        return context

@login_required
def crearUserStory(request):
    """
    Funcion para crear un user story.
    Retorna la página con el formulario correspondiente para la creación
    del user story.
    """
    context = RequestContext(request)
    if request.method == 'POST':
        group_form = UserStoryForm(data=request.POST)
        if group_form.is_valid():
            group = group_form.save()
            group.save()
            return redirect('listar_user_story')
        else:
            print group_form.errors
    else:
        group_form = UserStoryForm()

    return render_to_response('adm/crear_user_story.html', {'group_form': group_form}, context)


class ModificarUserStoryView(UpdateView):
    """
    Permite modificar los atributos del User Story
    """
    model = UserStory
    form_class = UserStoryEditForm
    template_name = 'adm/modificar_user_story.html'
    templ_base_error = None
    next = 'listar_user_story'

    def get_success_url(self):
        return reverse(self.next)

    def form_invalid(self, form):
        self.templ_base_error = "__panel.html"
        return UpdateView.form_invalid(self, form)

    def get_context_data(self, **kwargs):
        context = UpdateView.get_context_data(self, **kwargs)
        context['action'] = reverse('modificar_user_story',kwargs={'pk':self.kwargs['pk']})
        if self.templ_base_error:
            context['nodefault'] = self.templ_base_error
        return context



@login_required
def eliminarUserStory(request, pk):
    """Funcion para Eliminar un rol.

    :param request: Parametro a ser procesado.
    :param pk: Parametro a ser procesado el identificador del rol que va a eliminarse.
    :type request: HttpRequest.
    :type pk: int.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    context = RequestContext(request)
    user_story = get_object_or_404(UserStory, pk=pk)
    if request.method == 'POST':
        user_story.delete()
        return redirect('listar_user_story')

    return render_to_response('adm/eliminar_user_story.html', {'object':user_story}, context)



@login_required
def consultarUserStory(request, pk):

    context = RequestContext(request)
    user_story = get_list_or_404(UserStory, pk=pk)
    context_dict = {'user_story': user_story}

    return render_to_response('adm/detalle_user_story.html', context_dict, context)
