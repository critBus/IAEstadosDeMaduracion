#from ReneDjango.Utiles import *
from ReneDjangoApp.Utiles.Utiles import *
from ReneDjangoApp.Utiles.Clases.File import File

from django.shortcuts import render
from Aplicacion.models import *
from Aplicacion.UtilesAplicacion.LogicaBD import bd
from Aplicacion.UtilesAplicacion.ClasesLogica import *
from Aplicacion.UtilesAplicacion.ConstantesApp import *
from Aplicacion.ReneIAClasificador.entrenador_v2_0 import ConfiguracionDeEntrenamiento,DatosDeResultadoDeEntrenamiento
from django.db import models
import os
# def open2(dire):
# 	return open(dire, 'wb+')
from ProyectoPCChar.settings import MEDIA_ROOT,MEDIA_URL
from Aplicacion.UtilesAplicacion.UtilesUrlsApp import *
from ReneDjangoApp.Utiles.MetodosUtiles import Archivo
from ReneDjangoApp.Utiles.MetodosUtiles import UtilesImg

from ipware.ip import get_client_ip


def get_ip_usuario(request):
    client_ip, routable = get_client_ip(request)
    if client_ip is None:
        client_ip = get_client_ip_DJ(request)
    if client_ip is None:
        client_ip=APP_CNF.consts.NOMBRE_IP_ANONIMO
    return client_ip



# def puedeVerLaAdministracion(request):
#     return request.user.is_staff


def renderAppActual(request, template, dic=None, loc=None):
    user:User=request.user
    esValidoElUsuario=(not user.is_anonymous) and user.is_authenticated and user.is_active
    esAdmin=esValidoElUsuario and (bd.esAdmin(user) or user.is_staff or user.is_superuser)
    default = {
        'esAdmin': esAdmin
        ,'esInvestigador': esValidoElUsuario and (esAdmin or bd.esInvestigador(user))
        ,'estaAutenticado': user.is_authenticated
    }#puedeVerLaAdministracion(request)
    return APP_CNF.renderApp(request, template, appenDic(default,dic), loc)
def getDatosDeClasificacion_All_user(request,nombreExtra,tipoDeFiltro=None,valorAComparar=None):
    ldcla=[]
    user:User=request.user
    estaAutenticado=user.is_anonymous or not user.is_authenticated
    if estaAutenticado:
        username=APP_CNF.consts.NOMBRE_USUARIO_ANONIMO
    else:
        username=user.username
    ip=get_ip_usuario(request)
    valorAComparar=str(valorAComparar).lower()

    if not isNoneOR(tipoDeFiltro,valorAComparar):
        #print("tipoDeFiltro=",tipoDeFiltro," !!!!!!!!!!!!!!!!!!!!!!!!!")
        #print("valorAComparar=", valorAComparar, " !!!!!!!!!!!!!!!!!!!!!!!!!")
        if tipoDeFiltro == APP_CNF.radios.FRUTO:
            lcla=bd.getClasificacion_All_usuario_contains(username,ip,nombreFruto=valorAComparar)
        elif tipoDeFiltro == APP_CNF.radios.FECHA:
            #print("entro en fecha !!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            lcla=bd.getClasificacion_All_usuario_contains(username,ip,fecha=valorAComparar)
            #print("len =",len(lcla))
        elif tipoDeFiltro == APP_CNF.radios.CLASIFICACION:
            lcla=bd.getClasificacion_All_usuario_contains(username,ip,resultado=valorAComparar)
        elif tipoDeFiltro == APP_CNF.radios.MODELO:
            lcla=bd.getClasificacion_All_usuario_contains(username,ip,nombreModelo=valorAComparar)
        elif tipoDeFiltro == APP_CNF.radios.TODO:
            lcla=bd.getClasificacion_All_usuario_contains(username,ip
                                                          ,nombreModelo=valorAComparar
                                                          ,nombreFruto=valorAComparar
                                                          ,fecha=valorAComparar
                                                          ,resultado=valorAComparar)

    else:
        if estaAutenticado:
            lcla = bd.getClasificacion_All_username(username)
        else:
            lcla=bd.getClasificacion_All_username_ip(username,ip)
    for cla in lcla:
        d=DatosDeClasificacion.getDatosDeClasificacion(cla,bd)#(request,cla)#nombreExtra
        #print("nombre img=",d.datosDeImagenOriginal.nombre)
        ldcla.append(d)
    return ldcla


def getDatosDeClasificacionDetalles(request,idClasificacion,idProcesamientoDeImagen=None)->DatosDeClasificacionYProcesamiento:
    d=DatosDeClasificacionYProcesamiento()

    cla = bd.getClasificacion_id(idClasificacion)
    if idProcesamientoDeImagen is None:
        pro=bd.getProcesamientoDeImagen_Clasificacion(cla)
    else:
        pro = bd.getProcesamientoDeImagen_id(idProcesamientoDeImagen)
    limgs=bd.getImagenProcesada_All_deProcesamiento(pro)
    #print("l leng=",len(limgs))
    for imgp in limgs:
        #dimg=crearImgDetalles(request,imgp)
        dimg = APP_CNF.getDireccionRelativa_DeCampoImagen(imgp.ImagenResultante)
        nombreAlgoritmo=imgp.AlgoritmoUtilizado
        #print('nombreAlgoritmo=',nombreAlgoritmo)
        if nombreAlgoritmo==NOMBRE_ALGORITMO_GRAY_WORD:
            d.datosDeImagenGrayWorld=dimg
        elif nombreAlgoritmo==NOMBRE_ALGORITMO_CIEL_AB:
            d.datosDeImagenCielAB=dimg
        elif nombreAlgoritmo==NOMBRE_ALGORITMO_M_RESIZE:
            d.datosDeImagenMResize=dimg
        elif nombreAlgoritmo==NOMBRE_ALGORITMO_BOUNDING_BOX:
            d.datosDeImagenBoundingBox=dimg

    # d.datosDeImagenOriginal = crearImgDetalles(request,pro)
    d.datosDeImagenOriginal = APP_CNF.getDireccionRelativa_DeCampoImagen(pro.ImagenOriginal)
    d.clasificacion=cla.Resultado
    return d

def eliminarArchivoDelModelo(cnf:ConfiguracionDeEntrenamiento):
    f=File(cnf.direccionDeSalidaDelModelo)
    print("va a eliminar archivo modelo ",f)
    if f.existe() and f.isFile():
        f.delete()





def organizarClasesEnDatosResultadoDeEntrenamiento(dr:DatosDeResultadoDeEntrenamiento,idDataset):
    listaDeClasesClasificacion=bd.getClaseDeClasificacion_All_Dataset(bd.getDataset_id(idDataset))
    matrisDeConfusionOrganizada=[[0 for j in range(len(dr.clases))] for i in range(len(dr.clases))]
    nombresDeClasesOrganizados=get_nombresDeClasesOrganizados_De_listaDeClasesClasificacion(listaDeClasesClasificacion)


    for i in range(len(dr.matrizDeConfusion)):
        for j in range(len(dr.matrizDeConfusion[i])):
            f=-1
            c=-1
            for cla in listaDeClasesClasificacion:
                if f!=-1 and c!=-1:
                    break
                if f==-1 and cla.NombreCarpetaCorrespondiente == dr.clases[i]:
                    f=cla.Indice
                if c==-1 and cla.NombreCarpetaCorrespondiente == dr.clases[j]:
                    c=cla.Indice
            matrisDeConfusionOrganizada[f][c]=dr.matrizDeConfusion[i][j]
    dr.clases=nombresDeClasesOrganizados
    dr.matrizDeConfusion=matrisDeConfusionOrganizada

    metricasOrdenadas=[me for me in dr.metricas]
    for i,cla in enumerate(listaDeClasesClasificacion):
        metricasOrdenadas[cla.Indice]=dr.metricas[i]
    dr.metricas=metricasOrdenadas

def get_nombresDeClasesOrganizados_De_listaDeClasesClasificacion(listaDeClasesClasificacion):
    nombresDeClasesOrganizados = [0 for i in range(len(listaDeClasesClasificacion))]
    for cla in listaDeClasesClasificacion:
        nombresDeClasesOrganizados[cla.Indice]=cla.Nombre
    return nombresDeClasesOrganizados
def get_nombresDeClasesOrganizados_De_ModeloNeuronal(modeloNuronal:ModeloNeuronal):
    listaDeClasesClasificacion=bd.getClaseDeClasificacion_All_ModeloNeuronal(modeloNuronal)
    return get_nombresDeClasesOrganizados_De_listaDeClasesClasificacion(listaDeClasesClasificacion)

def cumpleConCondicionMinimaArchivoDentroDeComprimidoDatset(f):
    # print("condicion f=",f)
    # print("Archivo.getProfundidad(f)=",Archivo.getProfundidad(f))
    # print("UtilesImg.esImagen(f)=",UtilesImg.esImagen(f))
    return Archivo.getProfundidad(f)==2 and UtilesImg.esImagen(f)



#
# def crearImgDetalles(request,instanciaDeModelo):
#     img=None
#     nombreExtra=""
#     if isinstance(instanciaDeModelo,models.ImageField):
#         img=instanciaDeModelo
#         nombreExtra = "Original"
#     elif isinstance(instanciaDeModelo,ProcesamientoDeImagen):
#         img=instanciaDeModelo.ImagenOriginal
#         nombreExtra = "Original"
#     elif isinstance(instanciaDeModelo,Clasificacion):
#         img=instanciaDeModelo.ImagenProcesada
#         nombreExtra = "Original"
#     elif isinstance(instanciaDeModelo,ImagenProcesada):
#         img=instanciaDeModelo.ImagenResultante
#         nombreExtra = instanciaDeModelo.AlgoritmoUtilizado
#     return crearImgDatos(request,img,"ImgDetalles" + nombreExtra)

