from django.contrib import admin,auth
from django.contrib.auth.models import User

def getUsernameRequest(request):
    return request.user.username
def getUserRequest(request):
    return request.user

def intentarLoguearse(request,nombreUsario,contraseña):
    user=auth.authenticate(username=nombreUsario,password=contraseña)
    if user is not None:
        auth.login(request,user)
        return True
    return False

def desloguearse(request,app_config=None):
    if app_config is not None:
        app_config.alDesloguearse(request)
    auth.logout(request)



def getModelUserDJ():
    # return settings.AUTH_USER_MODEL
    return User

def editarUserDJ(t):
    t.save()
    return t

def saveUserDJ( username, password, nombre, apellido, correo, es_de_los_adminstradores=False):
    user = getModelUserDJ().objects.create_user(str(username).strip(), str(correo).strip(), str(password).strip())
    #user.username = str(username).strip()
    #user.password = str(password).strip()
    #user.email = str(correo).strip()
    user.first_name = str(nombre).strip()
    user.last_name = str(apellido).strip()
    if es_de_los_adminstradores:
        user.is_staff=True
    user.save()
    return user

def getUserDJ_id( id):
    return getModelUserDJ().objects.get(id=id)

def getUserDJ_username( username):
    username=str(username).strip()
    ls = getModelUserDJ().objects.filter(username=username)
    if len(ls) > 0:
        return ls[0]
    return None


def getUserDJ_All():
    return getModelUserDJ().objects.all()

def deleteUserDJ( t):
    t.delete()

def existeUsuarioDJ(username):
    username = str(username).strip()
    return getUserDJ_username(username) is not None

def cambiarContraseñaUsuarioDJ(usuario:User,contraseña):
    usuario.set_password(contraseña)
    usuario.save()
    return usuario



