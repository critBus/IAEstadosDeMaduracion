from ReneDjangoApp.Utiles.Utiles import *
from ReneDjangoApp.Utiles.Clases.File import File
from Aplicacion.models import *
from Aplicacion.UtilesAplicacion.LogicaBD import bd
from Aplicacion.UtilesAplicacion.ClasesLogica import *
from Aplicacion.UtilesAplicacion.ConstantesApp import *
from Aplicacion.ReneIAClasificador.AlgoritmosDeProcesamientoDeImagenes import mresize
import os
import uuid
# def open2(dire):
# 	return open(dire, 'wb+')
from ProyectoPCChar.settings import MEDIA_ROOT,MEDIA_URL

def getUrlInicialBase_Mas(urlRelativa):
    return os.path.join(MEDIA_ROOT,urlRelativa)
def getUrlCarpetaSalidaDatasets():
    #urlCarpetaSalidaDatasets = bd.getConfiguracionGeneral_Actual().DireccionCarpetaDatasets
    return getUrlInicialBase_Mas("DATASETS")
def getUrlCarpetaSalidaModelos():
    #urlCarpetaSalidaModelos = bd.getConfiguracionGeneral_Actual().DireccionCarpetaModelosNeuronales
    return getUrlInicialBase_Mas("MODELOS_NURONALES")
def getUrlCarpetaSalidaTiposDeFrutos():
    #urlCarpetaSalidaModelos = bd.getConfiguracionGeneral_Actual().DireccionCarpetaModelosNeuronales
    return getUrlInicialBase_Mas("TIPOS_DE_FRUTOS")

def crearImagenesDeEjemploFruto(urlRelativa):
    urlCompleta=getDireccionCompleta_ImagenTipoDeFruto_DireccionRelativa(urlRelativa)
    nombreImagenResultante = File.castear(urlCompleta).getName()

    urlImagenEjemplo50px = getYCrea_DireccionCompletaNueva_ImagenTipoDeFruto50px(
        direccionRelativa=urlRelativa
        , nombreImagenDeEjemplo=nombreImagenResultante
    )

    mresize(urlImg=str(urlCompleta)
            , urlSalida=str(urlImagenEjemplo50px)
            , size=[50, 50])

    urlImagenEjemplo900_900px = getYCrea_DireccionCompletaNueva_ImagenTipoDeFruto900_900px(
        direccionRelativa=urlRelativa
        , nombreImagenDeEjemplo=nombreImagenResultante
    )
    mresize(urlImg=str(urlCompleta)
            , urlSalida=str(urlImagenEjemplo900_900px)
            , size=[900, 900])

def crearArchivosDe_TipoDeFruto(request,nombreDelFruto,nombreDeLaImagen,nombreKeyArchivo):
    urlRelativa = getYCrea_DireccionNuevaRelativa_ImagenTipoDeFruto(request=request
                                                                    , nombreDelFruto=nombreDelFruto
                                                                    , nombreDeLaImagen=nombreDeLaImagen
                                                                    )
    urlCompleta = getDireccionCompleta_ImagenTipoDeFruto_DireccionRelativa(urlRelativa)
    urlCompleta = getYCrear_PostFile(request, nombreKeyArchivo, urlCompleta)

    nombreImagenResultante=File.castear(urlCompleta).getName()

    urlImagenEjemplo50px=getYCrea_DireccionCompletaNueva_ImagenTipoDeFruto50px(
        direccionRelativa=urlRelativa
        ,nombreImagenDeEjemplo=nombreImagenResultante
    )

    mresize(urlImg=str(urlCompleta)
            , urlSalida=str(urlImagenEjemplo50px)
            , size=[50, 50])

    urlImagenEjemplo900_900px = getYCrea_DireccionCompletaNueva_ImagenTipoDeFruto900_900px(
        direccionRelativa=urlRelativa
        , nombreImagenDeEjemplo=nombreImagenResultante
    )
    mresize(urlImg=str(urlCompleta)
            , urlSalida=str(urlImagenEjemplo900_900px)
            , size=[900, 900])


    return urlRelativa


def getYCrea_NuevaCarpetaContenedoraDeFruto(request,nombreDelFruto):
    urlCarpetaSalidaFrutos = getUrlCarpetaSalidaTiposDeFrutos()
    nombreCarpetaTipoDeFruto=os.path.join(str(urlCarpetaSalidaFrutos),nombreDelFruto)
    f:File=File(nombreCarpetaTipoDeFruto)
    contadorDeCopias=1
    while f.existe():
        f=File(nombreCarpetaTipoDeFruto+ "_" + str(contadorDeCopias))
        contadorDeCopias+=1
    f.mkdirs()
    return f



def getYCrea_DireccionNuevaRelativa_ImagenTipoDeFruto(request,nombreDelFruto,nombreDeLaImagen):
    carpetaContenedoraFruto:File=getYCrea_NuevaCarpetaContenedoraDeFruto(request,nombreDelFruto)
    r=getUsernameRequest(request)+"_"+str(uuid.uuid4())+"_"+nombreDeLaImagen

    return os.path.join(str(carpetaContenedoraFruto.getName()),r)

# def getDireccionCompletaNueva_ImagenTipoDeFruto(request,nombreDeLaImagen):
#     urlCarpetaSalidaFrutos = getUrlCarpetaSalidaTiposDeFrutos()
#     return urlCarpetaSalidaFrutos + "/" + getDireccionNuevaRelativa_ImagenTipoDeFruto(request,nombreDeLaImagen)

def getDireccionCompleta_ImagenTipoDeFruto_DireccionRelativa(direccionRelativa):
    urlCarpetaSalidaFrutos = getUrlCarpetaSalidaTiposDeFrutos()
    return os.path.join(str(urlCarpetaSalidaFrutos),direccionRelativa)

def getCarpetaContenedoraDeFruto(direccionRelativa):
    urlCompleta=getDireccionCompleta_ImagenTipoDeFruto_DireccionRelativa(direccionRelativa)
    f=File.castear(urlCompleta)
    carpetaContenedora=f.getParentFile()
    return carpetaContenedora

NOMBRE_CARPETA_IMAGEN_DE_EJEMPLO_50PX="Imagen_De_Ejemplo50px"
def getYCrea_DireccionCompletaNueva_ImagenTipoDeFruto50px(direccionRelativa,nombreImagenDeEjemplo):
    carpetaContenedora=getCarpetaContenedoraDeFruto(direccionRelativa)
    carpetaImagenesDeEjemplo=os.path.join(str(carpetaContenedora),NOMBRE_CARPETA_IMAGEN_DE_EJEMPLO_50PX)
    f = File.castear(carpetaImagenesDeEjemplo)
    if not f.existe():
        f.mkdirs()
    return os.path.join(str(carpetaImagenesDeEjemplo),nombreImagenDeEjemplo)

def getDireccionCompleta_ImagenTipoDeFruto50px(direccionRelativa):
    carpetaContenedora = getCarpetaContenedoraDeFruto(direccionRelativa)
    carpetaImagenesDeEjemplo = os.path.join(str(carpetaContenedora), NOMBRE_CARPETA_IMAGEN_DE_EJEMPLO_50PX)
    return File.castear(carpetaImagenesDeEjemplo).listFiles()[0]

NOMBRE_CARPETA_IMAGEN_DE_EJEMPLO_900_900PX="Imagen_De_Ejemplo900_900px"
def getYCrea_DireccionCompletaNueva_ImagenTipoDeFruto900_900px(direccionRelativa,nombreImagenDeEjemplo):
    carpetaContenedora=getCarpetaContenedoraDeFruto(direccionRelativa)
    carpetaImagenesDeEjemplo=os.path.join(str(carpetaContenedora),NOMBRE_CARPETA_IMAGEN_DE_EJEMPLO_900_900PX)
    f = File.castear(carpetaImagenesDeEjemplo)
    if not f.existe():
        f.mkdirs()
    return os.path.join(str(carpetaImagenesDeEjemplo),nombreImagenDeEjemplo)

def getDireccionCompleta_ImagenTipoDeFruto900_900px(direccionRelativa):
    carpetaContenedora = getCarpetaContenedoraDeFruto(direccionRelativa)
    carpetaImagenesDeEjemplo = os.path.join(str(carpetaContenedora), NOMBRE_CARPETA_IMAGEN_DE_EJEMPLO_900_900PX)
    return File.castear(carpetaImagenesDeEjemplo).listFiles()[0]

def eliminarArchivosFruto(direccionRelativa):
    carpetaContenedora = getCarpetaContenedoraDeFruto(direccionRelativa)
    f:File=File.castear(carpetaContenedora)
    print("va a eliminar en eliminarArchivosFruto")
    print("f=",f)
    if f.existe() and f.isDir():
        f.delete()







def getDireccionCompleta_ImagenTipoDeFruto(frutoOId):
    if isinstance(frutoOId,Fruto):
        fruto=frutoOId
    else:
        fruto=bd.getFruto_id(frutoOId)
    urlCarpetaSalidaFrutos = getUrlCarpetaSalidaTiposDeFrutos()
    return urlCarpetaSalidaFrutos+"/"+fruto.DireccionImagen

def getDireccionNuevaRelativaModelo(request,nombreDelModelo):
    r=getUsernameRequest(request)+"_"+nombreDelModelo+".h5"
    if r.startswith("/") or r.startswith("\\"):
        r=r[1:]
    return r
def getDireccionNuevaModelo(request,nombreDelModelo):
    urlCarpetaSalidaModelos =getUrlCarpetaSalidaModelos()
    fModelos:File=File.castear(urlCarpetaSalidaModelos)
    if not fModelos.existe():
        fModelos.mkdirs()
    f:File=File(urlCarpetaSalidaModelos+"/"+getDireccionNuevaRelativaModelo(request,nombreDelModelo))
    contadorDeCopias = 1
    f2 = f
    while f2.existe():
        f2 = File(str(f) + "_" + str(contadorDeCopias))
        contadorDeCopias+=1

    return f2
def getDireccionCompletaModelo(modelo_O_Id):
    if isinstance(modelo_O_Id,ModeloNeuronal):
        modelo=modelo_O_Id
    else:
        modelo=bd.getModeloNeuronal_id(modelo_O_Id)
    urlCarpetaSalidaModelos = getUrlCarpetaSalidaModelos()#bd.getConfiguracionGeneral_Actual().DireccionCarpetaModelosNeuronales
    return urlCarpetaSalidaModelos+"/"+modelo.Direccion
def getDireccionCompletaDataset(id):
    # urlCarpetaDatasetProcesado = getUrlCarpetaContenedoraDeDatasetCompleto_Procesado()  # bd.getConfiguracionGeneral_Actual().DireccionCarpetaDatasets
    # direccionRelativa = bd.getDataset_id(id).Direccion_Imagenes_Procesadas  # .Direccion
    # if direccionRelativa.startswith("/") or direccionRelativa.startswith("\\"):
    #     direccionRelativa = direccionRelativa[1:]
    # return urlCarpetaDatasetProcesado + "/" + direccionRelativa
    # return bd.getDataset_id(id).Direccion_Imagenes_Procesadas # !!Aqui!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    urlCarpetaSalidaDatasets = getUrlCarpetaSalidaDatasets()#bd.getConfiguracionGeneral_Actual().DireccionCarpetaDatasets
    direccionRelativa=bd.getDataset_id(id).Direccion_Imagenes_Procesadas #.Direccion
    if direccionRelativa.startswith("/") or direccionRelativa.startswith("\\"):
        direccionRelativa=direccionRelativa[1:]
    return urlCarpetaSalidaDatasets+"/"+direccionRelativa

def get_url_relativa_carpeta_usuario_temp(request):
    return getUsernameRequest(request) + "_temporal"
def get_url_carpeta_usuario_temp(request):
    #return os.path.join(MEDIA_ROOT, get_url_relativa_carpeta_usuario_temp(request))
    return getUrlInicialBase_Mas(get_url_relativa_carpeta_usuario_temp(request))
def crear_carpeta_usuario_temp(request):
    f=File.castear(get_url_carpeta_usuario_temp(request))
    if not f.existe():
        f.mkdirs()
    return f
def get_url_carpeta_descomprimir_de_usuario(request):
    #crear_carpeta_usuario_temp(request)
    return os.path.join(get_url_carpeta_usuario_temp(request), getUsernameRequest(request) +"_descompridos")
def hay_carpetas_o_archivos_en_carpeta_de_descompresion(request):
    f = File.castear(get_url_carpeta_descomprimir_de_usuario(request))
    return f.existe() and len(f.list())>0
def crear_carpeta_descomprimir_de_usuario(request):
    f=File.castear(get_url_carpeta_descomprimir_de_usuario(request))
    if not f.existe():
        f.mkdirs()
    return f

def get_url_archivo_comprimido_de_usuario(request,fileName):
    crear_carpeta_usuario_temp(request)
    return os.path.join(get_url_carpeta_usuario_temp(request), fileName)#getUsernameRequest(request) + "_"+
def get_url_carpeta_datasets_incompletos(request):
    urlCarpetaSalidaDatasets = getUrlCarpetaSalidaDatasets()#bd.getConfiguracionGeneral_Actual().DireccionCarpetaDatasets
    return os.path.join(urlCarpetaSalidaDatasets, "_INCOMPLETO")
def crear_carpeta_carpeta_datasets_incompletos(request):
    f = File.castear(get_url_carpeta_datasets_incompletos(request))
    if not f.existe():
        f.mkdirs()
    return f
# def get_nueva_url_dataset_incompleto_SiExisteCambiarNombre(request,nombreDelDataset):
#     f:File=os.path.join(str(crear_carpeta_carpeta_datasets_incompletos(request)),getUsernameRequest(request)+"_"+nombreDelDataset)
#     contadorDeCopias=1
#     while f.existe():
#         f=File(str(f)+"_"+str(contadorDeCopias))
#     return f
def get_nueva_url_dataset_incompleto(request,nombreDelDataset):
    return os.path.join(str(crear_carpeta_carpeta_datasets_incompletos(request)),getUsernameRequest(request)+"_"+nombreDelDataset)


def hay_carpetas_o_archivos_en_carpeta_dataset_incompleto(request,nombreDelDataset):
    f = File.castear(get_nueva_url_dataset_incompleto(request,nombreDelDataset))
    return f.existe() and f.isDir()  and len(f.list()) > 0
def eliminar_carpeta_dataset_incompleto_Si_hay_carpetas_o_archivos(request,nombreDelDataset):
    f = File.castear(get_nueva_url_dataset_incompleto(request,nombreDelDataset))
    print("va a borrar en eliminar_carpeta_dataset_incompleto_Si_hay_carpetas_o_archivos")
    print("eliminando a ", f)
    if hay_carpetas_o_archivos_en_carpeta_dataset_incompleto(request,nombreDelDataset):
        f.delete()
#

def getUrl_CarpetaContenedoraDeDatasetCompleto_ProcesadoYNoProcesado_DireccionEnDataset(direccionEnDataset):
    carpetaContenedorDeDataset = getFile_carpetaContenedorDeDataset_Dataset(direccionEnDataset)
    # urlCarpetaDedataset_ProcesadoYNoProcesado = os.path.join(str(getUrlCarpetaSalidaDatasets()),
    #                                                          getUsernameRequest(request) + "_" + nombreDelDataset)
    return carpetaContenedorDeDataset
def getUrl_CarpetaContenedoraDeDatasetCompleto_ProcesadoYNoProcesado(request,nombreDelDataset):
    urlCarpetaDedataset_ProcesadoYNoProcesado = os.path.join(str(getUrlCarpetaSalidaDatasets()),
                                                             getUsernameRequest(request) + "_" + nombreDelDataset)
    return urlCarpetaDedataset_ProcesadoYNoProcesado
def getYCrear_CarpetaContenedoraDeDatasetCompleto_ProcesadoYNoProcesado_SiExisteCrearNuevo(request,nombreDelDataset):
    f=File.castear(getUrl_CarpetaContenedoraDeDatasetCompleto_ProcesadoYNoProcesado(request,nombreDelDataset))
    contadorDeCopias = 1
    f2=f
    while f2.existe():
        f2=File(str(f)+"_"+str(contadorDeCopias))
        contadorDeCopias += 1
    f2.mkdirs()
    return f2
# def __getYCrear_CarpetaContenedoraDeDatasetCompleto_ProcesadoYNoProcesado(request,nombreDelDataset):
#     # urlCarpetaDedataset_ProcesadoYNoProcesado = os.path.join(str(getUrlCarpetaSalidaDatasets()),
#     #                                                          getUsernameRequest(request) + "_" + nombreDelDataset)
#     urlCarpetaDedataset_ProcesadoYNoProcesado=getUrl_CarpetaContenedoraDeDatasetCompleto_ProcesadoYNoProcesado(request,nombreDelDataset)
#     f = File.castear(urlCarpetaDedataset_ProcesadoYNoProcesado)
#     if not f.existe():
#         f.mkdirs()
#     return  f
NOMBRE_CARPETA_PROCESADO="Procesado"


# def getUrlCarpetaContenedoraDeDatasetCompleto_Procesado(request,nombreDelDataset):
#     return os.path.join(
#         str(getUrl_CarpetaContenedoraDeDatasetCompleto_ProcesadoYNoProcesado(request, nombreDelDataset))
#         , NOMBRE_CARPETA_PROCESADO)

def getYCrear_CarpetaContenedoraDeDatasetCompleto_Procesado_DesdeContenedorDataset(direccionContenedorDataset):
    #urlCarpetaDedataset_Procesado=getUrlCarpetaContenedoraDeDatasetCompleto_Procesado(request,nombreDelDataset)
    urlCarpetaDedataset_Procesado=os.path.join(
        str(direccionContenedorDataset)
        , NOMBRE_CARPETA_PROCESADO)

    f = File.castear(urlCarpetaDedataset_Procesado)
    if not f.existe():
        f.mkdirs()
    return f
# def getUrlCarpetaContenedoraDeDatasetCompleto_NoProcesado(request,nombreDelDataset):
#     return os.path.join(
#         str(getUrl_CarpetaContenedoraDeDatasetCompleto_ProcesadoYNoProcesado(request, nombreDelDataset))
#         , "No_Procesado")

def getYCrear_CarpetaContenedoraDeDatasetCompleto_NoProcesado_DesdeContenedorDataset(direccionContenedorDataset):
    urlCarpetaDedataset_NoProcesado=os.path.join(
        str(direccionContenedorDataset)
        , "No_Procesado")

    f = File.castear(urlCarpetaDedataset_NoProcesado)
    if not f.existe():
        f.mkdirs()
    return f

# def eliminar_CarpetaContenedoraDeDatasetCompleto_Procesado_Si_hay_carpetas_o_archivos(request,nombreDelDataset):
#     f = File.castear(getUrlCarpetaContenedoraDeDatasetCompleto_Procesado(request,nombreDelDataset))
#     print("va a borrar en eliminar_CarpetaContenedoraDeDatasetCompleto_Procesado_Si_hay_carpetas_o_archivos")
#     print("eliminando a ",f)
#     if f.existe() and f.isDir() and len(f.list()):
#         f.delete()

# def eliminar_carpetaContenedoraDeDatasetCompleto_NoProcesado_Si_hay_carpetas_o_archivos(request,nombreDelDataset):
#
#     f = File.castear(getUrlCarpetaContenedoraDeDatasetCompleto_NoProcesado(request,nombreDelDataset))
#     print("va a borrar en eliminar_carpetaContenedoraDeDatasetCompleto_NoProcesado_Si_hay_carpetas_o_archivos")
#     print("eliminando a ", f)
#     if f.existe() and f.isDir() and len(f.list())>0:
#         f.delete()
NOMBRE_CARPETA_IMAGENES_DE_EJEMPLO_50PX="Imagenes_De_Ejemplo50px"
def getUrl_CarpetaContenedoraDeDatasetCompleto_ImagenesDeEjemplo50px_DesdeCarpetaContenedora(url_CarpetaContenedoraDeDatasetCompleto_ProcesadoYNoProcesado):
    return os.path.join(str(url_CarpetaContenedoraDeDatasetCompleto_ProcesadoYNoProcesado),
                                                             NOMBRE_CARPETA_IMAGENES_DE_EJEMPLO_50PX)
# def getUrl_CarpetaContenedoraDeDatasetCompleto_ImagenesDeEjemplo50px(request,nombreDelDataset):
#     return getUrl_CarpetaContenedoraDeDatasetCompleto_ImagenesDeEjemplo50px_DesdeCarpetaContenedora(
#         getUrl_CarpetaContenedoraDeDatasetCompleto_ProcesadoYNoProcesado(request, nombreDelDataset)
#     )

def getYCrear_CarpetaContenedoraDeDatasetCompleto_ImagenesDeEjemplo50px_DesdeContentedorDataset(direccionContenedorDataset):
    urlCarpetaContenedoraDeDatasetCompleto_ImagenesDeEjemplo =\
        getUrl_CarpetaContenedoraDeDatasetCompleto_ImagenesDeEjemplo50px_DesdeCarpetaContenedora(
            direccionContenedorDataset
    )
    # urlCarpetaContenedoraDeDatasetCompleto_ImagenesDeEjemplo=getUrl_CarpetaContenedoraDeDatasetCompleto_ImagenesDeEjemplo50px(request,nombreDelDataset)

    f = File.castear(urlCarpetaContenedoraDeDatasetCompleto_ImagenesDeEjemplo)
    if not f.existe():
        f.mkdirs()
    return f
# def eliminar_CarpetaContenedoraDeDatasetCompleto_ImagenesDeEjemplo50px_Si_hay_carpetas_o_archivos(request,nombreDelDataset):
#
#     f = File.castear(getUrl_CarpetaContenedoraDeDatasetCompleto_ImagenesDeEjemplo50px(request,nombreDelDataset))
#     print("va a borrar en eliminar_CarpetaContenedoraDeDatasetCompleto_ImagenesDeEjemplo50px_Si_hay_carpetas_o_archivos")
#     print("eliminando a ", f)
#     if f.existe() and f.isDir() and len(f.list())>0:
#         f.delete()

def getYCrear_CarpetaContenedoraDeDatasetCompleto_DatasetID_ImagenDeEjemplo50px(direccionEnDataset,nombreCarpetaDeClasificacion):
    f = get_CarpetaContenedoraDeDatasetCompleto_DatasetID_ImagenDeEjemplo50px(direccionEnDataset,nombreCarpetaDeClasificacion)
    if not f.existe():
        f.mkdirs()
    return f

def get_CarpetaContenedoraDeDatasetCompleto_DatasetID_ImagenDeEjemplo50px(direccionEnDataset,nombreCarpetaDeClasificacion):
    #print("direccionEnDataset=", str(direccionEnDataset),"   \n+++++++++++++++++++++++++++++++++++++++++++++")
    #carpetaProcesesadoONo = getFile_carpetaProcesesadoONo_Dataset(direccionEnDataset)
    carpetaContenedorDeDataset = getFile_carpetaContenedorDeDataset_Dataset(direccionEnDataset)
    #print("carpetaProcesesadoONo=",str(carpetaContenedorDeDataset),"   \n+++++++++++++++++++++++++++++++++++++++++++++")
    urlCarpetaContenedoraDeDatasetCompleto_ImagenesDeEjemplo = getUrl_CarpetaContenedoraDeDatasetCompleto_ImagenesDeEjemplo50px_DesdeCarpetaContenedora(
        carpetaContenedorDeDataset
    )
    urlCarpetaContenedoraDeDatasetCompleto_ImagenDeEjemplo=os.path.join(str(urlCarpetaContenedoraDeDatasetCompleto_ImagenesDeEjemplo),
                                                             nombreCarpetaDeClasificacion)
    f = File.castear(urlCarpetaContenedoraDeDatasetCompleto_ImagenDeEjemplo)
    return f

def getYCrear_CarpetaContenedoraDeDatasetCompleto_ImagenDeEjemplo50px_DesdeContentedorDataset(direccionContenedorDataset,nombreCarpetaDeClasificacion):
    urlCarpetaContenedoraDeDatasetCompleto_ImagenesDeEjemplo = getYCrear_CarpetaContenedoraDeDatasetCompleto_ImagenesDeEjemplo50px_DesdeContentedorDataset(
        direccionContenedorDataset)
    urlCarpetaContenedoraDeDatasetCompleto_ImagenDeEjemplo=os.path.join(str(urlCarpetaContenedoraDeDatasetCompleto_ImagenesDeEjemplo),
                                                             nombreCarpetaDeClasificacion)
    f = File.castear(urlCarpetaContenedoraDeDatasetCompleto_ImagenDeEjemplo)
    if not f.existe():
        f.mkdirs()
    return f


def getDireccionRealtivaDeDataset(fileDataset: File):
    #fileDataset: se refiere a la ubicacion completa de la carpeta prosesada, o la ubicacion completa de la carpeta no prosesada
    carpetaProcesesadoONo = fileDataset.getParentFile()
    carpetaContenedorDeDataset = carpetaProcesesadoONo.getParentFile()
    url = ""
    for f in [carpetaContenedorDeDataset, carpetaProcesesadoONo, fileDataset]:
        url += "/" + f.getName()
    return url
# def getFile_carpetaProcesesadoONo_Dataset(direccion):
#     if direccion.startswith("/") or direccion.startswith("\\"):
#         direccion=direccion[1:]
#     direccionDataset=getUrlCarpetaSalidaDatasets()
#     direccionCompleta=os.path.join(str(direccionDataset),str(direccion))
#     fileDataset=File.castear(direccionCompleta)
#     carpetaProcesesadoONo = fileDataset.getParentFile()
#     return carpetaProcesesadoONo

def getFile_DireccionCompleta_Dataset(direccion):
    if direccion.startswith("/") or direccion.startswith("\\"):
        direccion=direccion[1:]
    direccionDataset=getUrlCarpetaSalidaDatasets()
    direccionCompleta=os.path.join(str(direccionDataset),str(direccion))
    #direccionCompleta = getFile_DireccionCompleta_Dataset(direccion)
    fileDataset = File.castear(direccionCompleta)
    return fileDataset

def getFile_carpetaContenedorDeDataset_Dataset(direccion):
    fileDataset =getFile_DireccionCompleta_Dataset(direccion)
    carpetaProcesesadoONo = fileDataset.getParentFile()
    carpetaContenedorDeDataset = carpetaProcesesadoONo.getParentFile()
    return carpetaContenedorDeDataset

def eliminar_CarpetaContenedoraDeDatasetCompleto_ProcesadoYNoProcesado_EnDireccion(direccion):
    #carpetaProcesesadoONo=getFile_carpetaProcesesadoONo_Dataset(direccion)
    #carpetaContenedorDeDataset = carpetaProcesesadoONo.getParentFile()
    carpetaContenedorDeDataset = getFile_carpetaContenedorDeDataset_Dataset(direccion)
    f =carpetaContenedorDeDataset
    print(
        "va a borrar en eliminar_CarpetaContenedoraDeDatasetCompleto_ProcesadoYNoProcesado_EnDireccion")
    print("eliminando a ", f)
    if f.existe() and f.isDir():
        f.delete()
def eliminar_Archivo_ModeloNeuronalFisico(direccion):
    if direccion.startswith("/") or direccion.startswith("\\"):
        direccion=direccion[1:]
    dirccionModelosNuronales=getUrlCarpetaSalidaModelos()
    direccionCompleta = os.path.join(str(dirccionModelosNuronales), str(direccion))
    f:File = File.castear(direccionCompleta)
    print(
        "va a borrar en eliminar_Archivo_ModeloNeuronalFisico")
    print("eliminando a ", f)
    if f.existe() and f.isFile():
        f.delete()
# def eliminar_CarpetaContenedoraDeDatasetCompleto_ProcesadoYNoProcesado_Si_hay_carpetas_o_archivos(request,nombreDelDataset):
#     f = File.castear(getUrl_CarpetaContenedoraDeDatasetCompleto_ProcesadoYNoProcesado(request,nombreDelDataset))
#     print("va a borrar en eliminar_CarpetaContenedoraDeDatasetCompleto_ProcesadoYNoProcesado_Si_hay_carpetas_o_archivos")
#     print("eliminando a ",f)
#     if f.existe() and f.isDir() and len(f.list())>0:
#         f.delete()



NOMBRE_CARPETA_IMAGENES_DE_EJEMPLO_900_600PX="Imagenes_De_Ejemplo900_600px"
def getUrl_CarpetaContenedoraDeDatasetCompleto_ImagenesDeEjemplo900_600px_DesdeCarpetaContenedora(url_CarpetaContenedoraDeDatasetCompleto_ProcesadoYNoProcesado):
    return os.path.join(str(url_CarpetaContenedoraDeDatasetCompleto_ProcesadoYNoProcesado),
                                                             NOMBRE_CARPETA_IMAGENES_DE_EJEMPLO_900_600PX)
# def getUrl_CarpetaContenedoraDeDatasetCompleto_ImagenesDeEjemplo900_600px(request,nombreDelDataset):
#     return getUrl_CarpetaContenedoraDeDatasetCompleto_ImagenesDeEjemplo900_600px_DesdeCarpetaContenedora(
#         getUrl_CarpetaContenedoraDeDatasetCompleto_ProcesadoYNoProcesado(request, nombreDelDataset)
#     )
    # return os.path.join(str(getUrl_CarpetaContenedoraDeDatasetCompleto_ProcesadoYNoProcesado(request,nombreDelDataset)),
    #                                                          "Imagenes_De_Ejemplo900_600px")
def getYCrear_CarpetaContenedoraDeDatasetCompleto_ImagenesDeEjemplo900_600px_DesdeContentedorDataset(direccionContenedorDataset):
    urlCarpetaContenedoraDeDatasetCompleto_ImagenesDeEjemplo=\
        getUrl_CarpetaContenedoraDeDatasetCompleto_ImagenesDeEjemplo900_600px_DesdeCarpetaContenedora(direccionContenedorDataset)

    f = File.castear(urlCarpetaContenedoraDeDatasetCompleto_ImagenesDeEjemplo)
    if not f.existe():
        f.mkdirs()
    return f
# def eliminar_CarpetaContenedoraDeDatasetCompleto_ImagenesDeEjemplo900_600px_Si_hay_carpetas_o_archivos(request,nombreDelDataset):
#
#     f = File.castear(getUrl_CarpetaContenedoraDeDatasetCompleto_ImagenesDeEjemplo900_600px(request,nombreDelDataset))
#     print("va a borrar en eliminar_CarpetaContenedoraDeDatasetCompleto_ImagenesDeEjemplo900_600px_Si_hay_carpetas_o_archivos")
#     print("eliminando a ", f)
#     if f.existe() and f.isDir() and len(f.list())>0:
#         f.delete()


def get_CarpetaContenedoraDeDatasetCompleto_DatasetID_ImagenDeEjemplo900_600px(direccionEnDataset,nombreCarpetaDeClasificacion):
    carpetaContenedorDeDataset = getFile_carpetaContenedorDeDataset_Dataset(direccionEnDataset)
    # print("carpetaProcesesadoONo=",str(carpetaContenedorDeDataset),"   \n+++++++++++++++++++++++++++++++++++++++++++++")
    urlCarpetaContenedoraDeDatasetCompleto_ImagenesDeEjemplo = getUrl_CarpetaContenedoraDeDatasetCompleto_ImagenesDeEjemplo900_600px_DesdeCarpetaContenedora(
        carpetaContenedorDeDataset
    )

    urlCarpetaContenedoraDeDatasetCompleto_ImagenDeEjemplo=os.path.join(str(urlCarpetaContenedoraDeDatasetCompleto_ImagenesDeEjemplo),
                                                             nombreCarpetaDeClasificacion)
    f = File.castear(urlCarpetaContenedoraDeDatasetCompleto_ImagenDeEjemplo)

    return f

def getYCrear_CarpetaContenedoraDeDatasetCompleto_ImagenDeEjemplo900_600px_DesdeContentedorDataset(direccionContenedorDataset,nombreCarpetaDeClasificacion):
    urlCarpetaContenedoraDeDatasetCompleto_ImagenesDeEjemplo = getYCrear_CarpetaContenedoraDeDatasetCompleto_ImagenesDeEjemplo900_600px_DesdeContentedorDataset(
        direccionContenedorDataset)
    urlCarpetaContenedoraDeDatasetCompleto_ImagenDeEjemplo=os.path.join(str(urlCarpetaContenedoraDeDatasetCompleto_ImagenesDeEjemplo),
                                                             nombreCarpetaDeClasificacion)
    f = File.castear(urlCarpetaContenedoraDeDatasetCompleto_ImagenDeEjemplo)
    if not f.existe():
        f.mkdirs()
    return f
