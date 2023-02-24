from ReneDjangoApp.Utiles.Clases.TipoDeImagen import TipoDeImagen
from ReneDjangoApp.Utiles.MetodosUtiles.Archivo import getExtencion

def getTipoDeImagen(f):
    extencion = getExtencion(f)
    return TipoDeImagen.get(extencion)
def esImagen(f):
    return getTipoDeImagen(f) is not None