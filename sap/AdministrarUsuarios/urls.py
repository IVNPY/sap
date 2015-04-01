from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'recetario.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$','principal.views.home'),
    
    url(r'^$', 'AdministrarUsuarios.views.indexUsuario', name='index'),
    url(r'^eliminar/(?P<id>\d+)/$', 'AdministrarUsuarios.views.eliminarUsuario', name='eliminar'),
    url(r'^nuevo','AdministrarUsuarios.views.nuevoUsuario', name='nuevo'),
    url(r'^modificar','AdministrarUsuarios.views.modificarUsuario', name='modificar'),
    url(r'^rol/(?P<id>\d+)/$','AdministrarUsuarios.views.rolUsuario', name='rol'),
)