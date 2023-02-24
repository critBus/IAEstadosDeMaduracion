import traceback
import os
import re

PATRON_SOLO_INT_POSITIVO_STR=re.compile(r"^[0-9]&")
PATRON_SOLO_FLOAT_POSITIVO_STR=re.compile(r"^[0-9]+(?:(?:[.](?:[0-9]+))?)$")


def separadorDePalabrasEnTextoUnido(palabra:str):
    listaDePalabras=[]
    #palabraActual = ""
    p=[""]
    def appenC(c):
        p[0]+=c


    def agregarPalabra():
        if len(p[0])>0:
            listaDePalabras.append(p[0])
            p[0]=""

    elAnteriorFueNumero=False
    for c in palabra:
        if c.isnumeric():
            if not elAnteriorFueNumero:
                agregarPalabra()
            appenC(c)
            elAnteriorFueNumero=True
            continue
        else:
            elAnteriorFueNumero=False
        if c.isupper():
            agregarPalabra()
            appenC(c)
        elif c=="_" or c.isspace():
            agregarPalabra()
        elif c.isalpha():
            appenC(c)
    agregarPalabra()
    return  listaDePalabras
# def inT(a):
#     if a is None:
#         return None
#     elif esInt(a):
#         return a
#     elif esFloat(a) or esFloatStr(a):
#         return int(a)
#     return None
#
# def inT(a):
#     if a is None:
#         return None
#     elif esInt(a):
#         return a
#     elif esFloat(a) or esFloatStr(a):
#         return int(a)
#     return None
def strg(*a):
    sal = ""
    for i in a:
        if i==None:
            sal+="None"
        else:
            sal += str(i)
    return sal
def esIntStr(a):
    a=str(a)
    return len(re.findall(PATRON_SOLO_INT_POSITIVO_STR,a))>0
def esFloatStr(a):
    a=str(a)
    return len(re.findall(PATRON_SOLO_FLOAT_POSITIVO_STR,a))>0
# def appenDic(dic,dicNew=None):
#     if dicNew is not None:
#         for k in dicNew.keys():
#             dic[k] = dicNew[k]
#     return dic
def starWithOR(a,*b):
    """
    args son las terminaciones
    :param a:
    :param b:
    :return:
    """
    for i in b:
        if a.startswith(i):
            return True
    return False
def endsWithOR(a,*args):
    """
    args son las terminaciones
    :param a:
    :param args:
    :return:
    """
    b=tuplaRectificada(args)
    for i in b:
        if a.endswith(i):
            return True
    return False

def tuplaRectificada(a):
    if esTupla(a) and len(a)==1 and esTupla(a[0]):
        return a[0]
    return a
def isEmpty(a):
    if esString(a) or esLista(a) or esTupla(a):
        return len(a)==0
def getFormato(url):
    print("url=",url)
    print("type=",type(url))
    nombre = os.path.basename(url)
    print("nombre=", nombre)
    formato = ""
    if contiene(nombre,"."):
        formato = nombre[nombre.rfind("."):len(nombre)]
        print("formato=", formato)
    return formato

def strLista(lista):
    salida = "[ "
    for i in range(len(lista)):
        if i != 0:
            salida += " , "
        salida += str(lista[i])
    salida += " ]"
    return salida
def verLista(lista):
    salida=strLista(lista)
    print(salida)
    return salida
def getExceptionStr():
    return traceback.format_exc()
def verException():
    print(getExceptionStr())
def appenDic(dic,dicNew=None):
    if dicNew is not None:
        if esLista(dicNew):
            for dicI in dicNew:
                for k in dicI.keys():
                    dic[k] = dicI[k]
        else:
            for k in dicNew.keys():
                dic[k] = dicNew[k]
    return dic
# Basicos

def isNoneAll(*a):
    for e in a:
        if e is not None:
            return False
    return True
def isNoneOR(*a):
    for e in a:
        if e is None:
            return True
    return False


def esInt(a):
    if esBool(a):
        return False
    return isinstance(a, int)
def esFloat(a):
    return isinstance(a, float)
def esBool(a):
    return isinstance(a,bool)

def esIntOR(*a):
    for i in a:
        if(esInt(i)):
            return True
    return False
def esBoolOR(*a):
    for i in a:
        if(esBool(i)):
            return True
    return False
def esFloatOR(*a):
    for i in a:
        if(esFloat(i)):
            return True
    return False
def esStringOR(*a):
    for i in a:
        if(esString(i)):
            return True
    return False



def esIntAll(*a):
    for i in a:
        if not esInt(i):
            return False
    return True
def esBoolAll(*a):
    for i in a:
        if not esBool(i):
            return False
    return True
def esFloatAll(*a):
    for i in a:
        if not esFloat(i):
            return False
    return True
def esStringAll(*a):
    for i in a:
        if not esString(i):
            return False
    return True

def esString(a):
    return isinstance(a,str)

def esFuncion(a):
    return str(type(a))=="<class 'function'>"

def esLista(a):
    return isinstance(a,list)
def esListaAll(*a):
    for i in a:
        if not esLista(i):
            return False
    return True
def esTupla(a):
    return isinstance(a,tuple)
def esSet(a):
    return isinstance(a,set)
def esMap(a):
    return isinstance(a,dict)

def strg(*a):
    sal = ""
    for i in a:
        if i==None:
            sal+="None"
        else:
            sal += str(i)
    return sal
def contiene(palabra,subContenido,ignoreCase=False):

    if subContenido is None:
        return False
    if esString(palabra):
        if ignoreCase:
            palabra=palabra.lower()
            subContenido = subContenido.lower()
        return palabra.find(subContenido)!=-1
    if esSet(palabra):
        palabra=list(palabra)
    if esLista(palabra) or esTupla(palabra):
        try:
            return palabra.index(subContenido) != -1
        except:
            return False
    if esMap(palabra):
        listakeys=list(palabra.keys())
        return contiene(listakeys,subContenido)
def contieneOR(palabra,*subContenido):
    if len(subContenido)==1 and esLista(subContenido[0]):
        subContenido=subContenido[0]
    for i in subContenido:
        if contiene(palabra,i):
            return True
    return False

def toBool(a):
    return eval(str(a).capitalize())