from django.core.exceptions import ValidationError
from ReneDjangoApp.Utiles.MetodosUtiles.MetodosBasicos import *

import re
#PATRON_DIRECCION=re.compile("^((?:[a-zA-Z]\:)|(?:\\))(?:\\{1}|(?:(?:\\{1})[^\\](?:[^/:*?<>""|]*))+)$")
PATRON_DIRECCION=re.compile("^((?:(?:[a-zA-Z]:)?(?:\\\\(?:[ ]|[_.-]|\w)+)+(?:\\\\)?)|(?:(?:[a-zA-Z]:)?(?:[/](?:[ ]|[_.-]|\w)+)+[/]?))$")
CARACTERES_NO_PERMITIDOS_EN_NOMBRE_ARCHIVO=('\\', '/', ':', '*', '?', '\"', '<', '>', '|')
def validar_direccion(value):

    if not len(re.findall(PATRON_DIRECCION,str(value)))>0:
        raise ValidationError(
            "No es una direccion valida",
            params={'value': value},
        )

def validar_nombre_archivo(value):

    if contieneOR(str(value),*CARACTERES_NO_PERMITIDOS_EN_NOMBRE_ARCHIVO):
        raise ValidationError(
            "Contiene caracteres no permitidos",
            params={'value': value},
        )
def getValidarDeMaximoSize(maximo,mensajeDeError):
    def file_size(value):  # add this to some file where you can import it from
        limit =maximo #ejemplo 2 * 1024 * 1024
        if value.size > limit:
            raise ValidationError(mensajeDeError)#Ejemplo ('File too large. Size should not exceed 2 MiB.')
    return file_size


