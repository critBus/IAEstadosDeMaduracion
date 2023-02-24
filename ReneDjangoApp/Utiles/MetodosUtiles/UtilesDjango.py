from ReneDjangoApp.Utiles.MetodosUtiles.UtilesDjangoUser import *
from ReneDjangoApp.Utiles.MetodosUtiles.UtilesDjangoUser import desloguearse,intentarLoguearse,getUserRequest,getUsernameRequest
from ReneDjangoApp.Utiles.Clases.AppDj import AppDj
from django.urls import path
from django.contrib import admin,auth
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import os
#from io import open
import base64

import uuid

from ReneDjangoApp.Utiles.MetodosUtiles.MetodosBasicos import *

def get_client_ip_DJ(request):
    #Asegúrese de que tiene configurado correctamente el proxy inverso (si lo hay) (por ejemplo mod_rpaf instalado para Apache).

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip



def toBase64Str_Img(url):
    imagen = None
    with open(url, "rb") as archivo_imagen:
        imagen = base64.b64encode(archivo_imagen.read()).decode('utf-8')
    return imagen

def deleteCampoImg(img):
    url=str(img)
    print("url=", url)
    # url=os.path.abspath(url)
    # print("2url=",url)
    if os.path.exists(url):
        os.remove(url)

def getExtencionPostFile(request,key):
    url=getPostFileStr(request,key)
    nombre = os.path.basename(url)
    #print("nombre=", nombre)
    formato = ""
    if contiene(nombre,"."):
        formato = nombre[nombre.rfind("."):len(nombre)]
        #print("formato=", formato)
    return formato

from django.conf import settings
from django.core.files.storage import FileSystemStorage
def crearFileDj_v2(request,nombrePostFile,url):
    folder =url #'my_folder/'
    if request.method == 'POST' and request.FILES[nombrePostFile]:
        myfile = request.FILES[nombrePostFile]
        fs = FileSystemStorage(location=folder)  # defaults to   MEDIA_ROOT
        filename = fs.save(myfile.name, myfile)
        file_url = fs.url(filename)
        return nombrePostFile,file_url

def getYCrear_PostFile(request,key,urlSalida):
    file = request.FILES[key].read()
    with open(urlSalida, 'wb+') as destination:
        destination.write(file)
    return urlSalida

def getPostFile(request,key):
    return request.FILES[key]

def getPostFileStr(request,key):
    return str(getPostFile(request,key))

def getSizeFileDj(request,nombrePostFile):
    f = request.FILES[nombrePostFile]
    return f.size #bytes

def crearFileDj(request,nombrePostFile,url)->str:#nombreAplicacion,rutaIntermedia,nombreImagenACrear
    f=request.FILES[nombrePostFile]#,extencion=None,ponerExtencion=True
    print("f=",f)
    #ruta = nombreAplicacion+"/"+rutaIntermedia+"/"+nombreImagenACrear
    with open(url, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
        return  url



def getNombreImagenTemp_Aleatorios(request, nombre, extencion=None) -> str:
    if extencion is not None:
        nombre += extencion
    user:User=request.user
    nombreUsuario=""
    if user.is_anonymous or not user.is_authenticated:
        nombreUsuario=str(uuid.uuid1())
    else:
        nombreUsuario=request.user.username
    return  nombreUsuario + nombre
def getNombreArchivo_DesdeUploadDj(request, nombre) -> str:
    return request.user.username + nombre
class DatosDeArchivo_DesdeUploadDj:
    def __init__(self):
        self.url_relativa_carpeta_static=None
        self.url_relativa_completa=None
        self.nombre=None
    def crearDic(self):
        return {'url_relativa_carpeta_static':self.url_relativa_carpeta_static
                ,'url_relativa_completa':self.url_relativa_completa
                ,'nombre':self.nombre}

    @staticmethod
    def getDeDic(dic):
        d = DatosDeArchivo_DesdeUploadDj()
        d.nombre = dic['nombre']
        d.url_relativa_completa = dic['url_relativa_completa']
        d.url_relativa_carpeta_static = dic['url_relativa_carpeta_static']
        return d

class DatosDeImagenTempDj:
    def __init__(self):
        self.url_relativa_carpeta_static=None
        self.url_relativa_completa=None
        self.nombre=None
    def crearDic(self):
        return {'url_relativa_carpeta_static':self.url_relativa_carpeta_static
                ,'url_relativa_completa':self.url_relativa_completa
                ,'nombre':self.nombre}
    @staticmethod
    def getDeDic(dic):
        d=DatosDeImagenTempDj()
        d.nombre=dic['nombre']
        d.url_relativa_completa=dic['url_relativa_completa']
        d.url_relativa_carpeta_static = dic['url_relativa_carpeta_static']
        return d


def crearDatosDeImagenTempDj(request,app_cnf:AppDj,nombreImg,extencion=None)->DatosDeImagenTempDj:
    return getDatosDeImagenTempDj_DeNombre(app_cnf,getNombreImagenTemp_Aleatorios(request, nombreImg, extencion))

def getDatosDeImagenTempDj_DeNombre(app_cnf:AppDj,nombre):
    img = DatosDeImagenTempDj()
    img.nombre = nombre
    img.url_relativa_completa = app_cnf.getRutaCarpetaImg() + "/" + img.nombre
    img.url_relativa_carpeta_static = app_cnf.getRutaImgTem(img.nombre)
    return img

def getDatosDeArchivo_DesdeUploadDj_DeNombre(app_cnf:AppDj,nombre):
    img = DatosDeArchivo_DesdeUploadDj()
    img.nombre = nombre
    img.url_relativa_completa = app_cnf.getRutaCarpeta_archivos_temporales() + "/" + img.nombre
    img.url_relativa_carpeta_static = app_cnf.getRuta_archivo_temporal(img.nombre)
    return img
def crearDatosDeArchivo_DesdeUploadDj(request,app_cnf:AppDj,nombre)->DatosDeArchivo_DesdeUploadDj:
    return getDatosDeArchivo_DesdeUploadDj_DeNombre(app_cnf,getNombreArchivo_DesdeUploadDj(request, nombre))

def crearImgTempDj(request,app_cnf:AppDj,nombrePostFileImagen,nombreImg,extencion=None)->DatosDeImagenTempDj:
    d=crearDatosDeImagenTempDj(request,app_cnf,nombreImg,extencion)
    crearFileDj(request=request#,open2=app_cnf.metodoOpen
                       , nombrePostFile=nombrePostFileImagen
                       , url=d.url_relativa_completa
                       )

    return d

def crearArchivo_DesdeUpload_Dj(request,app_cnf:AppDj,nombrePostFileImagen,nombreImg)->DatosDeArchivo_DesdeUploadDj:
    d=crearDatosDeArchivo_DesdeUploadDj(request,app_cnf,nombreImg)

    crearFileDj(request=request#,open2=app_cnf.metodoOpen
                       , nombrePostFile=nombrePostFileImagen
                       , url=d.url_relativa_completa
                       )

    return d

def isPost(request,app_cnf:AppDj,nombreformularioActualPost)->bool:
    return request.method == 'POST' and request.POST[app_cnf.nombre_form_ubicacion_post] == str(nombreformularioActualPost)


def qdict_to_dict(qdict):
    """Convert a Django QueryDict to a Python dict.

    Single-value fields are put in directly, and for multi-value fields, a list
    of all values is stored at the field's key.

    """
    return {str(k).replace("[]",""): v[0] if len(v) == 1 else v for k, v in qdict.lists()}


def getPost(request,key):
    d=qdict_to_dict(request.POST)
    print("d=",d)
    return d[str(key)]
def getPostInt(request,key):
    return int(getPost(request,key))
def getPostFloat(request,key):
    return float(getPost(request,key))
def getPostBool(request,key):
    #print("key=",key)
    if key in request.POST:
        dato=getPost(request,key)
        dato=dato.strip()
        if dato=="on":
            return True
        elif dato=="off":
            return False
        #print("dato=",dato)
        return toBool(dato)
    return False

def setTiempoDeExpiracionDeSession(request,dias=-1,horas=-1):
    tiempo=60*60
    if dias==-1 and horas==-1:
        tiempo*=5
    else:
        if horas>0:
            tiempo*=horas
        if dias>0:
            tiempo*=24*dias

    request.session.set_expiry(tiempo)

def existePost(request,key):
    return key in request.POST
def existeSes(request,key):
    return key in request.session
def putSes(request,key,value):
    request.session[key] =value
def getSes(request,key):
    return request.session[key]
def getSesBool(request,key,porDefecto=None):
    try:
        v=getSes(request,key)
        return toBool(v)
    except:
        return porDefecto

def getSesInt(request,key):
    return int(getSes(request,key))


def toBool(a):
    return eval(str(a).capitalize())

def pathR(url,funcion):
    return path(url+"/", funcion,name=url)

def pathR_Admin(url):
    return pathR(url,lambda r:HttpResponseRedirect("/admin/"))

def pathR_Logout(url,app_config):
    def vista(r):
        desloguearse(r,app_config)
        return HttpResponseRedirect(app_config.loguin_redirect)
    return pathR(url, vista)
    #return path(url+"/", lambda r:HttpResponseRedirect("/admin/"),name="admin")




def pathR_loguin(plantilla,app_conf:AppDj):
    def vista(r):
        df=app_conf.datos_formulario_loguin
        if isPost(r,app_conf,df.nombre_form_loguin):
            # print("entro a intentar loguearse")
            seLogueo=intentarLoguearse(r,getPost(r,df.nombre_campo_username),getPost(r,df.nombre_campo_password))
            # print("seLogueo=",seLogueo)
            if seLogueo:
                app_conf.alLoguearse(r)
                df.hay_errores=False
                # print("Se logueo si")
                # print("va a ","/"+app_conf.urlHome+"/")
                return HttpResponseRedirect("/"+app_conf.urlHome+"/")
            df.setFalloDeLoguin()
        else:
            df.hay_errores = False

        return render(r,plantilla,{"form_loguin":df
                                   ,'nombre_form_ubicacion_post': app_conf.nombre_form_ubicacion_post})
    return pathR(app_conf.urls.URL_VISTA_LOGUIN,vista)


# def crearFileDj(request,open2,nombrePostFileImagen,urlimg)->str:
#     f = request.FILES[nombrePostFileImagen]
#     with open2(urlimg) as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)
#         return urlimg
