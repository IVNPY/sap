from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

#para el registro y login
from apps.registration.backends.default.views import ActivationView
from apps.registration.backends.default.views import RegistrationView

#para el abm de usuarios y roles
from apps.adm.views import *
from apps.adm.models import *
from django.contrib import admin

admin.autodiscover ()

urlpatterns = patterns('',

    #documentacion
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Descomenta la suiguiente linea para habilitar el admin:
    url(r'^admin/', include(admin.site.urls)),
    #Pagina acerca de SAP
    url(r'^about/',
        TemplateView.as_view(template_name='about.html'),
        name='about'),

    #Administracion de usuarios
    url(r'^users$', login_required(ListarUsuarioView.as_view()), name='listar_usuario'),
    url(r'^users/create$', CrearUsuarioView.as_view(), name='crear_usuario'),
    url(r'^users/delete/(?P<pk>\d+)$',login_required(EliminarUsuarioView.as_view()), name='eliminar_usuario'),
    url(r'^users/edit/(?P<pk>\d+)$',login_required(ModificarUsuarioView.as_view()), name='modificar_usuario'),
    url(r'^users/(?P<pk>\d+)$',consultarUsuario, name='usuario_detalle'),

    #Administracion de roles
    url(r'^groups/$', login_required(ListarRolView.as_view()), name='listar_rol'),
    url(r'^groups/create/$', crearRol, name='crear_rol'),
    url(r'^groups/delete/(?P<pk>\d+)$', eliminarRol, name='eliminar_rol'),
    url(r'^groups/edit/(?P<pk>\d+)$', modificarRol, name='modificar_rol'),
    url(r'^groups/(?P<pk>\d+)$',consultarRol, name='rol_detalle'),
    url(r'^groups/users$',login_required(ListarUsuariosAsignarRolSistemaView.as_view()), name='listar_usuario_asignar_rol_sistema'),
    url(r'^groups/users/(?P<pk>\d+)$',login_required(AsignarRolesSistema.as_view()), name='asignar_rol_sistema'),
    url(r'^accounts/', include('apps.registration.backends.default.urls')),


    #Administracion de user stories
    url(r'^user_story/$', login_required(ListarUserStoryView.as_view()), name='listar_user_story'),
    url(r'^user_story/create/$', crearUserStory, name='crear_user_story'),
    url(r'^user_story/delete/(?P<pk>\d+)$', eliminarUserStory, name='eliminar_user_story'),
    url(r'^user_story/edit/(?P<pk>\d+)$', login_required(ModificarUserStoryView.as_view()), name='modificar_user_story'),
    url(r'^user_story/(?P<pk>\d+)$',consultarUserStory, name='user_story_detalle'),







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

