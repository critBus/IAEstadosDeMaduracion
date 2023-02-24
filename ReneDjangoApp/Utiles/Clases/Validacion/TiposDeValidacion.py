from ReneDjangoApp.Utiles.MetodosUtiles.MetodosBasicos import *
from ReneDjangoApp.Utiles.MetodosUtiles.UtilesImg import *
import re
class TipoDeValidacion:
    NO_NULL=None
    STR_NO_EMPTY=None
    STR_CON_ALFANUMERICOS=None
    SOLO_INT_POSITIVO_STR=None
    SOLO_FLOAT_POSITIVO_STR=None
    STR_CORREO=None
    STR_SOLO_LETRAS=None
    STR_SOLO_LETRAS_Y_NUMEROS=None
    STR_SOLO_ALFANUMERICOS=None
    STR_SEGURIDAD_MINIMA_CONTRASEÑA=None
    STR_ES_DIRECCION_FORMATO_IMAGEN=None
    STR_ES_DIRECCION_FORMATO_IMAGEN_JPG_JPEG_PNG=None
    def __init__(self,esValido,getMensaje):
        self.esValido=esValido
        self.getMensaje=getMensaje
    def setMensaje(self,texto):
        self.getMensaje=lambda :texto

__MEDIO_PATRON_LETRAS="(?:\\w|[ÑñáéíóúÁÉÍÓÚÀÈÌÒÙàèìòù])"
#PATRON_CONTIENE_LETRAS=re.compile("(?:\\d*)((?![\\d_])\\w+(?<![\\d_]))(?:\\d*)")
PATRON_CONTIENE_LETRAS=re.compile("(?:\\d*)((?![\\d_])"+__MEDIO_PATRON_LETRAS+"+(?<![\\d_]))(?:\\d*)")

def hayMatch(patron,texto):
    return len(re.findall(patron, texto)) > 0
TipoDeValidacion.NO_NULL=TipoDeValidacion(lambda v:v is not None,lambda :"No puede estar vacío ")
TipoDeValidacion.STR_NO_EMPTY=TipoDeValidacion(lambda v:TipoDeValidacion.NO_NULL.esValido(v) and isinstance(v,str) and len(v.strip())>0
                                               ,lambda :"No puede estar vacío ")
TipoDeValidacion.STR_CON_ALFANUMERICOS=TipoDeValidacion(lambda v:TipoDeValidacion.STR_NO_EMPTY.esValido(v) and hayMatch(PATRON_CONTIENE_LETRAS,v)#re.findall(PATRON_CONTIENE_LETRAS,v)>0
                                               ,lambda :"Debe de contener letras")
def __esEnteroPosivo(v):
    if esInt(v):
        return v>=0
    else:
        return esIntStr(v)
def __esFloatPosivo(v):
    if esFloat(v):
        return v>=0
    else:
        return esFloatStr(v)
TipoDeValidacion.SOLO_INT_POSITIVO_STR=TipoDeValidacion(lambda v:TipoDeValidacion.NO_NULL.esValido(v)
                                            and __esEnteroPosivo(v)
                                            ,lambda :"Debe ser un numero entero positivo ")
TipoDeValidacion.SOLO_FLOAT_POSITIVO_STR=TipoDeValidacion(lambda v:TipoDeValidacion.NO_NULL.esValido(v)
                                            and __esFloatPosivo(v)
                                            ,lambda :"Debe ser un numero positivo cuyo indicador decimal sea un ‘.’")

class TipoDeValidacionMinLength(TipoDeValidacion):
    def __init__(self, lengthMin,creardorMensaje):
        TipoDeValidacion.__init__(self,lambda v:TipoDeValidacion.STR_NO_EMPTY.esValido(v)
                                           and len(str(v).strip())>=lengthMin
                                  ,lambda :creardorMensaje(lengthMin))
class TipoDeValidacionMaxLength(TipoDeValidacion):
    def __init__(self, lengthMax,creardorMensaje):
        TipoDeValidacion.__init__(self,lambda v:TipoDeValidacion.STR_NO_EMPTY.esValido(v)
                                           and len(str(v).strip())<=lengthMax
                                  ,lambda :creardorMensaje(lengthMax))

class TipoDeValidacionRangoEnteroPositivo(TipoDeValidacion):
    def __init__(self, min,max,creardorMensaje):
        TipoDeValidacion.__init__(self,lambda v:TipoDeValidacion.SOLO_INT_POSITIVO_STR.esValido(v)
                                           and int(v)>=min and int(v)<=max
                                  ,lambda :creardorMensaje(min,max))

class TipoDeValidacionRangoPositivo(TipoDeValidacion):
    def __init__(self, min,max,creardorMensaje):
        TipoDeValidacion.__init__(self,lambda v:TipoDeValidacion.SOLO_FLOAT_POSITIVO_STR.esValido(v)
                                           and float(v)>=min and float(v)<=max
                                  ,lambda :creardorMensaje(min,max))


PATRON_CORREO=re.compile("^([a-z0-9_]+(?:(?:[.]?[a-z0-9_])*)[@][a-z0-9_]+\\.)(com)$")
TipoDeValidacion.STR_CORREO=TipoDeValidacion(lambda v:TipoDeValidacion.STR_NO_EMPTY.esValido(v)
                                            and hayMatch(PATRON_CORREO, v)
                                            ,lambda :"Correo Incorrecto")

PATRON_SOLO_LETRAS=re.compile("^(?:(?:[ ]*)(?:(?![\\d_])"+__MEDIO_PATRON_LETRAS+"(?<![\\d_]))+(?:[ ]*))+$")
TipoDeValidacion.STR_SOLO_LETRAS =TipoDeValidacion(lambda v:TipoDeValidacion.STR_NO_EMPTY.esValido(v) and hayMatch(PATRON_SOLO_LETRAS, v)
                                            ,lambda :"Solo debe de contener letras y espacios ")
PATRON_SOLO_LETRAS_Y_NUMEROS=re.compile("^(?:(?:[ ]*)(?:(?![_])"+__MEDIO_PATRON_LETRAS+"(?<![_]))+(?:[ ]*))+$")
TipoDeValidacion.STR_SOLO_LETRAS_Y_NUMEROS =TipoDeValidacion(lambda v:TipoDeValidacion.STR_NO_EMPTY.esValido(v) and hayMatch(PATRON_SOLO_LETRAS_Y_NUMEROS,v.strip() )
                                            ,lambda :"Solo debe de contener letras, numeros y espacios ")
PATRON_SOLO_ALFANUMERICOS =re.compile("^(?:(?:[ ]*)"+__MEDIO_PATRON_LETRAS+"+(?:[ ]*))+$")
TipoDeValidacion.STR_SOLO_ALFANUMERICOS =TipoDeValidacion(lambda v:TipoDeValidacion.STR_NO_EMPTY.esValido(v) and hayMatch(PATRON_SOLO_ALFANUMERICOS, v)
                                            ,lambda :"Solo debe de contener letras, numeros, espacios y '_'")
PATRON_TIENE_NUMEROS =re.compile("[0-9]+")
TipoDeValidacion.STR_SEGURIDAD_MINIMA_CONTRASEÑA =TipoDeValidacion(
    lambda v: (hayMatch(PATRON_CONTIENE_LETRAS, v) and hayMatch(PATRON_TIENE_NUMEROS,v)) \
    if (TipoDeValidacion.STR_NO_EMPTY.esValido(v)and len(str(v))>7) else False
                                            ,lambda :"Debe de contener letras, numeros, y al menos 8 caracteres")


TipoDeValidacion.STR_ES_DIRECCION_FORMATO_IMAGEN =TipoDeValidacion(lambda v:esImagen(v)
                                            ,lambda :"Debe de seleccionar algun archivo de tipo imagen")
TipoDeValidacion.STR_ES_DIRECCION_FORMATO_IMAGEN_JPG_JPEG_PNG =TipoDeValidacion(lambda v:esImagen(v)
                                                                           and (getTipoDeImagen(v)==TipoDeImagen.JPG
                                                                                or getTipoDeImagen(v)==TipoDeImagen.JPEG
                                                                                or getTipoDeImagen(v)==TipoDeImagen.PNG)
                                            ,lambda :"Debe de seleccionar algun archivo de tipo imagen con formato .jpg .jpeg .png")