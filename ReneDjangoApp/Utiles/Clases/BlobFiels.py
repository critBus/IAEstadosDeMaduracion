from io import open
import shutil
from django.db import models
import os

#from ReneDjangoApp.Utiles.Clases.AppDj import AppDj
from ReneDjangoApp.Utiles.Clases.AppDjImpl import AppDjImpl

class ImageFieldBlob(models.ImageField):


    def __init__(self,carpetaTemp="static", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.carpetaTemp=carpetaTemp
        self.ultimoNombre=None

    def get_prep_value(self, value):
        url=str(value)
        try:
            url=value.path
        except:
            pass
        return toBlob(fileABlob=url)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        #self.ultimoNombre="img_"+str(value)[-40:-1]
        self.ultimoNombre = "img_" +crearNombreAleatorio()
        return fromBlob(value,fileACrear=self.carpetaTemp+"/"+self.ultimoNombre)


    def to_python(self, value):
        return value

    def db_type(self, connection):
        return 'blob'
    @staticmethod
    def crearImg(imageFieldBlob,request=None,app_conf:AppDjImpl=None,nombre=None,extencion=None,carpeta=None):
        """
        (request,app_conf,nombre)


        (request,app_conf,nombre,extencion)


        o no usar (request,app_conf) pero entonces los argumentos hay que pasarlos por keyword
        :param request:
        :param app_conf:
        :param carpeta:
        :param nombre:
        :param extencion:
        :return:
        """
        seUsoApp_config=app_conf is not None and request is not None

        if nombre is None:
            nombre = os.path.basename(str(imageFieldBlob))
            #nombre=str(imageFieldBlob)#imageFieldBlob.ultimoNombre
        if extencion is not None:
            nombre+=extencion
        if seUsoApp_config:
            dimg=app_conf.getDatosDeImagenTempDj(request,nombre)
            destino=dimg.url_relativa_completa
        else:
            if carpeta is None:
                carpeta=imageFieldBlob.carpetaTemp
            destino = carpeta + "/" + nombre
        fuente=str(imageFieldBlob)

        shutil.copyfile(fuente, destino)
        if seUsoApp_config:
            return dimg
        return destino


    # def crearImg(self,request=None,app_conf:AppDjImpl=None,nombre=None,extencion=None,carpeta=None):
    #     """
    #     (request,app_conf,nombre)
    #
    #
    #     (request,app_conf,nombre,extencion)
    #
    #
    #     o no usar (request,app_conf) pero entonces los argumentos hay que pasarlos por keyword
    #     :param request:
    #     :param app_conf:
    #     :param carpeta:
    #     :param nombre:
    #     :param extencion:
    #     :return:
    #     """
    #     seUsoApp_config=app_conf is not None and request is not None
    #
    #     if nombre is None:
    #         nombre=self.ultimoNombre
    #     if extencion is not None:
    #         nombre+=extencion
    #     if seUsoApp_config:
    #         dimg=app_conf.getDatosDeImagenTempDj(request,nombre)
    #         destino=dimg.url_relativa_completa
    #     else:
    #         if carpeta is None:
    #             carpeta=self.carpetaTemp
    #         destino = carpeta + "/" + nombre
    #     fuente=str(self)
    #
    #     shutil.copyfile(fuente, destino)
    #     if seUsoApp_config:
    #         return dimg
    #     return destino






def toBlob(cadenaABlob=None,fileABlob=None):
    if cadenaABlob!=None:
        return cadenaABlob.encode("utf-16").hex()
    with open(fileABlob, 'rb') as file:
        blobData = file.read()
    return blobData.hex()
def fromBlob(blobStr,fileACrear=None):
    if fileACrear==None:
        return bytes.fromhex(blobStr).decode("utf-16")
    with open(fileACrear, 'wb') as file:
        file.write(bytes.fromhex(blobStr))
        return fileACrear


def crearNombreAleatorio():
    import string
    import random

    length_of_string = 30
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))
