from django.template import RequestContext
from django.shortcuts import render_to_response
from sap.forms import LoginForm
from django.contrib.auth import authenticate, login, logout


def login_page(request):
    ''' lanza la vista encargada del login '''
    message = None
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render_to_response('homepage.html', context_instance=RequestContext(request))
                else:
                    message = "La contrasenha es valida, pero la cuenta esta deshabilitada!"
            else:
                message = "Usuario o contrasenha incorrectas"
    else:
        form = LoginForm()
    return render_to_response('login.html',{'message': message, 'form': form}, context_instance=RequestContext(request))  

def homepage(request):
    ''' lanza la pagina principal '''
    return render_to_response('homepage.html', context_instance=RequestContext(request))

def logout_page(request):
    ''' se encarga de cerrar la sesion '''
    logout(request)
    return login_page(request)
