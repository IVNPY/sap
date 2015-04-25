from django.contrib.auth.models import User, Group, Permission
from apps.adm.models import UserStory, Proyecto


#def get_project_list():
#    project_list = Proyecto.objects.all().order_by('id_proyecto')
#    return project_list




def get_group_list():

    group_list = Group.objects.all().order_by('id')
    return group_list



def get_user_story_list():

    group_list = UserStory.objects.all().order_by('id')
    return group_list




"""
def get_category_list(max_results=0, starts_with=''):
        cat_list = []
        if starts_with:
            starts_with = starts_with + '%'
            cat_list = User.objects.filter(username__ilike=starts_with)
        # else:
        #         cat_list = User.objects.all()
        #
        # print cat_list

        if max_results > 0:
                if len(cat_list) > max_results:
                        cat_list = cat_list[:max_results]

        return cat_list
"""

def get_roles_list(max_results=0, starts_with=''):
        cat_list = []
        if starts_with:
            starts_with = starts_with + '%'
            cat_list = Group.objects.filter(name__ilike=starts_with)
        # else:
        #         cat_list = User.objects.all()
        #
        # print cat_list

        if max_results > 0:
                if len(cat_list) > max_results:
                        cat_list = cat_list[:max_results]

        return cat_list


#busca el texto ingresado en permisos
def get_permisos_list(max_results=0, starts_with=''):
        cat_list = []
        if starts_with:
            starts_with = starts_with + '%'
            cat_list = Permission.objects.filter(name__ilike=starts_with)
        # else:
        #         cat_list = User.objects.all()
        #
        # print cat_list

        if max_results > 0:
                if len(cat_list) > max_results:
                        cat_list = cat_list[:max_results]

        return cat_list

"""
#busca el texto ingresado en proyectos
def get_proyectos_list(max_results=0, starts_with=''):
        cat_list = []
        if starts_with:
            starts_with = starts_with + '%'
            cat_list = Proyecto.objects.filter(nombre_proyecto__ilike=starts_with)
        # else:
        #         cat_list = User.objects.all()
        #
        # print cat_list

        if max_results > 0:
                if len(cat_list) > max_results:
                        cat_list = cat_list[:max_results]

        return cat_list


#busca el texto ingresado en fases
def get_phases_list(pk):
    phases_list = Fase.objects.filter(proyecto_id=pk).order_by('numero_secuencia')
    return phases_list


#busca el texto ingresado en comites
def get_comite_list():
    comite_list = Comite.objects.all()
    return comite_list


#edu me dijo que va a usar
def encode_url(name):
    return name.replace(' ', '_')


def decode_url(url):
    return url.replace('_', ' ')
"""
