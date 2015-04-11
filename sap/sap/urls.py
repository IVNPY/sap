from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

#para el registro y login
from apps.registration.backends.default.views import ActivationView
from apps.registration.backends.default.views import RegistrationView

#para el abm de usuarios
#from apps.admin.views import CrearUsuarioView
#from apps.admin.views import ListarUsuarioView
#from apps.admin.views import EliminarUsuarioView
#from apps.admin.views import ModificarUsuarioView
#from apps.admin.views import consultarUsuario
#from apps.admin.views import AsignarRolesSistema

#para el abm de roles
#from apps.admin.views import crearRol
#from apps.admin.views import modificarRol
#from apps.admin.views import eliminarRol
#from apps.admin.views import listarRol
#from apps.admin.views import consultarRol

from apps.admin.views import *

urlpatterns = patterns('',

    #Pagina acerca de SAP
    url(r'^about/',
        TemplateView.as_view(template_name='about.html'),
        name='about'),

    #Administracion de usuarios
    url(r'^users$', ListarUsuarioView.as_view(), name='listar_usuario'),
    url(r'^users/create$', CrearUsuarioView.as_view(), name='crear_usuario'),
    url(r'^users/delete/(?P<pk>\d+)$',EliminarUsuarioView.as_view(), name='eliminar_usuario'),
    url(r'^users/edit/(?P<pk>\d+)$',ModificarUsuarioView.as_view(), name='modificar_usuario'),
    url(r'^users/(?P<pk>\d+)$',consultarUsuario, name='usuario_detalle'),
    url(r'^users/groups/(?P<pk>\d+)$',AsignarRolesSistema.as_view(), name='usuario_editaroles'),

    #Administracion de roles
    url(r'^group/$', listarRol, name='listar_rol'),
    url(r'^group/create/$', crearRol, name='crear_rol'),
    url(r'^group/delete/(?P<pk>\d+)$', eliminarRol, name='eliminar_rol'),
    url(r'^group/edit/(?P<pk>\d+)$', modificarRol, name='modificar_rol'),
    url(r'^group/(?P<pk>\d+)$',consultarRol, name='rol_detalle'),

#    url(r'^rol/crear/$', CrearRolView.as_view(), name='crear_rol'),
#    url(r'^rol/editar/(?P<pk>\d+)$', EditaRolPermisosView.as_view(), name='rol_permisos_edita'),
#    url(r'^rol/lista/$', ListaRolPermisosView.as_view(), name='rol_permisos_lista'),
#    url(r'^rol/eliminar/(?P<pk>\d+)/$', EliminaRolPermisosView.as_view(), name='rol_permisos_elimina'),
#    url(r'^rol/asignar/$', AsignaRolProyectoView.as_view(), name='rol_proyecto_crear'),
#    url(r'^rol/listaasignados/$', ListaRolProyectoView.as_view(), name='rol_proyecto_listar'),
#    url(r'^rol/listaasignados/(?P<idrolproyecto>\d+)$', ListaRolProyectoView.as_view(), name='rol_proyecto_fase'),
    


    url(r'^accounts/', include('apps.registration.backends.default.urls')),

    #Perfil del usuario
    url(r'^accounts/profile/',
        TemplateView.as_view(template_name='profile.html'),
        name='profile'),

    #Pagina de logueo
    url(r'^$',
        'django.contrib.auth.views.login',
        name='login'),

    #Registro de usuarios
    url(r'^activate/complete/$',
        TemplateView.as_view(template_name='registration/activation_complete.html'),
        name='registration_activation_complete'),
    # Activation keys get matched by \w+ instead of the more specific
    # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
    # that way it can return a sensible "invalid key" message instead of a
    # confusing 404.
    url(r'^activate/(?P<activation_key>\w+)/$',
        ActivationView.as_view(),
        name='registration_activate'),
    url(r'^register/$',
        RegistrationView.as_view(),
        name='registration_register'),
    url(r'^register/complete/$',
        TemplateView.as_view(template_name='registration/registration_complete.html'),
        name='registration_complete'),
    url(r'^register/closed/$',
        TemplateView.as_view(template_name='registration/registration_closed.html'),
        name='registration_disallowed'),
        (r'', include('apps.registration.auth_urls')),
)

