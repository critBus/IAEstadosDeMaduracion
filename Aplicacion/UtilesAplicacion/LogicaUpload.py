from Aplicacion.UtilesAplicacion.UtilesApp import *
from Aplicacion.UtilesAplicacion.ClasesLogica import *
from Aplicacion.UtilesAplicacion.LogicaBD import *
from datetime import datetime
from ReneDjangoApp.Utiles.Clases.TipoDeImagen import TipoDeImagen
from ReneDjangoApp.Utiles.MetodosUtiles import Archivo

from ReneDjangoApp.Utiles.Clases.Upload.ClasesUpload import *
from Aplicacion.ReneIAClasificador.entrenador_v2_0 import cumpleConLosRequisitosMinimosParaEntrenarCarpetaDataset,getDatosDeDataset,getClasesDeDatasetEn
from Aplicacion.ReneIAClasificador.UtilesDataSet import *

class RespestaDeMetodoIntentarCrearDataset:
    def __init__(self):
        self.terminoConExito=False
        self.mandoADetener=False
        self.terminoConError=False

class DatosDelDataset:
    def __init__(self):
        self.nombre=None
        self.tipoDeFruto=None
        self.descripcion=None
        self.matrizPar_Clasificacion_Carpeta=[]
        self.matris_Clasificacion_Carpeta_Descripcion=[]





class DatosDeClaseEnProcesamientoDeImagenParaCreacionDataset:
    def __init__(self):
        self.nombre=None
        self.carpeta=None
        self.indice=0
class DatosDeImagenEnProcesamientoParaCreacionDataset:
    def __init__(self):
        self.nombre=None
        self.tipoDeImagen:TipoDeImagen=None
        self.datosDeClase:DatosDeClaseEnProcesamientoDeImagenParaCreacionDataset=DatosDeClaseEnProcesamientoDeImagenParaCreacionDataset()
        self.faseAlgoritmo=None
class DatosDeFaseUploadDataset:
    def __init__(self,nombre,esta_en_esta,indice):
        self.esta_en_esta=esta_en_esta
        self.indice=indice
        self.nombre=nombre
class GestorDeFasesUploadDataset:
    def __init__(self):
        self.fases=[]
        self.__indice=0
    def addFase(self,nombre):
        leng=len(self.fases)
        self.fases.append(DatosDeFaseUploadDataset(nombre,self.__indice==leng,leng))
        return self
    def getFaseActual(self):
        return self.fases[self.__indice]
    def setFaseActual(self,nombre):
        for f in self.fases:
            f.esta_en_esta=f.nombre==nombre
            if f.esta_en_esta:
                self.__indice = f.indice


class DatosEnMemoriaUploadDataset:
    FASE_COMIENZO="FASE_COMIENZO"
    FASE_SUVIENDO_DATASET = "FASE_SUVIENDO_DATASET"
    FASE_DETENIENDO_UPLOAD_DATASET = "FASE_DETENIENDO_UPLOAD_DATASET"
    FASE_ERROR_SUVIENDO_DATASET = "FASE_ERROR_SUVIENDO_DATASET"
    FASE_ARCHIVO_DATASET_SUVIDO = "FASE_ARCHIVO_DATASET_SUVIDO"
    FASE_DESCOMPRIMIENDO_DATASET = "FASE_DESCOMPRIMIENDO_DATASET"
    FASE_DETENIENDO_DESCOMPRESION_DATASET="FASE_DETENIENDO_DESCOMPRESION_DATASET"
    FASE_DATASET_DESCOMPRIMIDO_CON_ERROR = "FASE_DATASET_DESCOMPRIMIDO_CON_ERROR"
    FASE_DATASET_DESCOMPRIMIDO = "FASE_DATASET_DESCOMPRIMIDO"
    FASE_DATASET_SUVIDO_CON_CLASES_ERRONEAS = "FASE_DATASET_SUVIDO_CON_CLASES_ERRONEAS"
    FASE_DATASET_DESCOMPRIDO_PASO_VALIDACION = "FASE_DATASET_DESCOMPRIDO_PASO_VALIDACION"
    FASE_DATASET_PROCESANDO_IMAGENES  = "FASE_DATASET_PROCESANDO_IMAGENES "
    FASE_DETENIENDO_PROCESAMIENTO_DE_IMAGENES = "FASE_DETENIENDO_PROCESAMIENTO_DE_IMAGENES "
    FASE_TERMINANDO_LA_CREACION_DEL_DATASET = "FASE_TERMINANDO_LA_CREACION_DEL_DATASET"
    FASE_TERMINO_LA_CREACION_DEL_DATASET = "FASE_TERMINO_LA_CREACION_DEL_DATASET"



    def __init__(self):
        self.__gf=GestorDeFasesUploadDataset()
        self.__gf.addFase(DatosEnMemoriaUploadDataset.FASE_COMIENZO)
        self.__gf.addFase(DatosEnMemoriaUploadDataset.FASE_SUVIENDO_DATASET)
        self.__gf.addFase(DatosEnMemoriaUploadDataset.FASE_DETENIENDO_UPLOAD_DATASET)
        self.__gf.addFase(DatosEnMemoriaUploadDataset.FASE_ARCHIVO_DATASET_SUVIDO)
        self.__gf.addFase(DatosEnMemoriaUploadDataset.FASE_DESCOMPRIMIENDO_DATASET)
        self.__gf.addFase(DatosEnMemoriaUploadDataset.FASE_DETENIENDO_DESCOMPRESION_DATASET)
        self.__gf.addFase(DatosEnMemoriaUploadDataset.FASE_DATASET_DESCOMPRIMIDO_CON_ERROR)
        self.__gf.addFase(DatosEnMemoriaUploadDataset.FASE_DATASET_DESCOMPRIMIDO)
        self.__gf.addFase(DatosEnMemoriaUploadDataset.FASE_DATASET_SUVIDO_CON_CLASES_ERRONEAS)
        self.__gf.addFase(DatosEnMemoriaUploadDataset.FASE_DATASET_DESCOMPRIDO_PASO_VALIDACION)
        self.__gf.addFase(DatosEnMemoriaUploadDataset.FASE_DATASET_PROCESANDO_IMAGENES)
        self.__gf.addFase(DatosEnMemoriaUploadDataset.FASE_DETENIENDO_PROCESAMIENTO_DE_IMAGENES)
        self.__gf.addFase(DatosEnMemoriaUploadDataset.FASE_TERMINANDO_LA_CREACION_DEL_DATASET)
        self.__gf.addFase(DatosEnMemoriaUploadDataset.FASE_TERMINO_LA_CREACION_DEL_DATASET)



        self.datosDeimagenEnProcesamiento:DatosDeImagenEnProcesamientoParaCreacionDataset=None
        self.datosDeFileDj: DatosDeFileDj=DatosDeFileDj()
        self.mensajeDeError=""

        self.gestorDeDatosUpload=GestorDeDatosUpload()

        self.llamoAdetenerUpload=False

        self.llamoAdetenerDescompresion = False
        self.carpetaDeDescompresion=None
        self.carpetaDatasetDescomprimido = None
        self.progresoDeDescompresion=0

        self.listaDeCarpetasEnDatasetDescomprimido=[]
        self.listaPar_Carpeta_CantidadDeImagenes=[]

        self.estadoDeProcesamientoDeImagenes=None
        self.directorioCarpetaEnCreacionDeDatasetProcesado=None
        self.directorioCarpetaEnCreacionDeDatasetNoProcesado:File = None
        self.llamoADetenerProcesamientoDeImagenes=False
        self.datosDelDataset:DatosDelDataset=None


    def __setEstadoHantesDeDatasetDescomprimido(self):
        self.listaDeCarpetasEnDatasetDescomprimido = []

    def pasarAFase_COMIENZO(self):
        self.__gf.setFaseActual(DatosEnMemoriaUploadDataset.FASE_COMIENZO)
        self.__setEstadoHantesDeDatasetDescomprimido()

    def pasarAFase_SUVIENDO_DATASET(self):
        self.__gf.setFaseActual(DatosEnMemoriaUploadDataset.FASE_SUVIENDO_DATASET)
        self.__setEstadoHantesDeDatasetDescomprimido()
    def pasarAFase_DETENIENDO_UPLOAD_DATASET(self):
        self.__gf.setFaseActual(DatosEnMemoriaUploadDataset.FASE_DETENIENDO_UPLOAD_DATASET)
        self.__setEstadoHantesDeDatasetDescomprimido()
    def pasarAFase_ERROR_SUVIENDO_DATASET(self):
        self.__gf.setFaseActual(DatosEnMemoriaUploadDataset.FASE_ERROR_SUVIENDO_DATASET)
        self.__setEstadoHantesDeDatasetDescomprimido()
    def pasarAFase_ARCHIVO_DATASET_SUVIDO(self):
        self.__gf.setFaseActual(DatosEnMemoriaUploadDataset.FASE_ARCHIVO_DATASET_SUVIDO)
        self.__setEstadoHantesDeDatasetDescomprimido()
    def pasarAFase_DESCOMPRIMIENDO_DATASET(self):
        self.__gf.setFaseActual(DatosEnMemoriaUploadDataset.FASE_DESCOMPRIMIENDO_DATASET)
        self.__setEstadoHantesDeDatasetDescomprimido()
    def pasarAFase_DETENIENDO_DESCOMPRESION_DATASET(self):
        self.__gf.setFaseActual(DatosEnMemoriaUploadDataset.FASE_DETENIENDO_DESCOMPRESION_DATASET)
        self.__setEstadoHantesDeDatasetDescomprimido()
    def pasarAFase_DATASET_DESCOMPRIMIDO_CON_ERROR(self):
        self.__gf.setFaseActual(DatosEnMemoriaUploadDataset.FASE_DATASET_DESCOMPRIMIDO_CON_ERROR)
        self.__setEstadoHantesDeDatasetDescomprimido()
    def pasarAFase_DATASET_DESCOMPRIMIDO(self):
        #print("Alguien llamo a la pase DATASET_DESCOMPRIMIDO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        self.__gf.setFaseActual(DatosEnMemoriaUploadDataset.FASE_DATASET_DESCOMPRIMIDO)
    def pasarAFase_DATASET_SUVIDO_CON_CLASES_ERRONEAS(self):
        self.__gf.setFaseActual(DatosEnMemoriaUploadDataset.FASE_DATASET_SUVIDO_CON_CLASES_ERRONEAS)
    def pasarAFase_DATASET_DESCOMPRIDO_PASO_VALIDACION(self):
        self.__gf.setFaseActual(DatosEnMemoriaUploadDataset.FASE_DATASET_DESCOMPRIDO_PASO_VALIDACION)
    def pasarAFase_DATASET_PROCESANDO_IMAGENES(self):
        self.__gf.setFaseActual(DatosEnMemoriaUploadDataset.FASE_DATASET_PROCESANDO_IMAGENES)

    def pasarAFase_DETENIENDO_PROCESAMIENTO_DE_IMAGENES(self):
        self.__gf.setFaseActual(DatosEnMemoriaUploadDataset.FASE_DETENIENDO_PROCESAMIENTO_DE_IMAGENES)
    def pasarAFase_TERMINANDO_LA_CREACION_DEL_DATASET(self):
        self.__gf.setFaseActual(DatosEnMemoriaUploadDataset.FASE_TERMINANDO_LA_CREACION_DEL_DATASET)
    def pasarAFase_TERMINO_LA_CREACION_DEL_DATASET(self):
        self.__gf.setFaseActual(DatosEnMemoriaUploadDataset.FASE_TERMINO_LA_CREACION_DEL_DATASET)



    def estaEnFase_COMIENZO(self):
        return self.__gf.getFaseActual().nombre==DatosEnMemoriaUploadDataset.FASE_COMIENZO

    def estaEnFase_SUVIENDO_DATASET(self):
        return self.__gf.getFaseActual().nombre==DatosEnMemoriaUploadDataset.FASE_SUVIENDO_DATASET
    def estaEnFase_DETENIENDO_UPLOAD_DATASET(self):
        return self.__gf.getFaseActual().nombre==DatosEnMemoriaUploadDataset.FASE_DETENIENDO_UPLOAD_DATASET
    def estaEnFase_ERROR_SUVIENDO_DATASET(self):
        return self.__gf.getFaseActual().nombre==DatosEnMemoriaUploadDataset.FASE_ERROR_SUVIENDO_DATASET
    def estaEnFase_ARCHIVO_DATASET_SUVIDO(self):
        return self.__gf.getFaseActual().nombre==DatosEnMemoriaUploadDataset.FASE_ARCHIVO_DATASET_SUVIDO
    def estaEnFase_DESCOMPRIMIENDO_DATASET(self):
        return self.__gf.getFaseActual().nombre==DatosEnMemoriaUploadDataset.FASE_DESCOMPRIMIENDO_DATASET
    def estaEnFase_DETENIENDO_DESCOMPRESION_DATASET(self):
        return self.__gf.getFaseActual().nombre==DatosEnMemoriaUploadDataset.FASE_DETENIENDO_DESCOMPRESION_DATASET
    def estaEnFase_DATASET_DESCOMPRIMIDO_CON_ERROR(self):
        return self.__gf.getFaseActual().nombre==DatosEnMemoriaUploadDataset.FASE_DATASET_DESCOMPRIMIDO_CON_ERROR
    def estaEnFase_DATASET_DESCOMPRIMIDO(self):
        return self.__gf.getFaseActual().nombre==DatosEnMemoriaUploadDataset.FASE_DATASET_DESCOMPRIMIDO
    def estaEnFase_DATASET_SUVIDO_CON_CLASES_ERRONEAS(self):
        return self.__gf.getFaseActual().nombre==DatosEnMemoriaUploadDataset.FASE_DATASET_SUVIDO_CON_CLASES_ERRONEAS
    def estaEnFase_DATASET_DESCOMPRIDO_PASO_VALIDACION(self):
        return self.__gf.getFaseActual().nombre==DatosEnMemoriaUploadDataset.FASE_DATASET_DESCOMPRIDO_PASO_VALIDACION
    def estaEnFase_DATASET_PROCESANDO_IMAGENES(self):
        return self.__gf.getFaseActual().nombre==DatosEnMemoriaUploadDataset.FASE_DATASET_PROCESANDO_IMAGENES
    def estaEnFase_DETENIENDO_PROCESAMIENTO_DE_IMAGENES(self):
        return self.__gf.getFaseActual().nombre==DatosEnMemoriaUploadDataset.FASE_DETENIENDO_PROCESAMIENTO_DE_IMAGENES
    def estaEnFase_TERMINANDO_LA_CREACION_DEL_DATASET(self):
        return self.__gf.getFaseActual().nombre==DatosEnMemoriaUploadDataset.FASE_TERMINANDO_LA_CREACION_DEL_DATASET
    def estaEnFase_TERMINO_LA_CREACION_DEL_DATASET(self):
        return self.__gf.getFaseActual().nombre==DatosEnMemoriaUploadDataset.FASE_TERMINO_LA_CREACION_DEL_DATASET


class LogicaUploadDataset:
    def __init__(self,app_config: AppDjImpl):
        self.app = app_config
        self.dm = app_config.datos_en_memoria

        self.__listaDeNombresDeDatasetEnProceso=[]




    def getListaDeNombresDeDatasetEnProceso(self):
        return self.__listaDeNombresDeDatasetEnProceso
    def addNombreDeDatasetEnProceso(self,nombre):
        if not nombre in self.__listaDeNombresDeDatasetEnProceso:
            self.__listaDeNombresDeDatasetEnProceso.append(nombre)
    def removeNombreDeDatasetEnProceso(self,nombre):
        self.__listaDeNombresDeDatasetEnProceso.remove(nombre)

    def getDatosEnMemoriaUploadDataset(self,request)->DatosEnMemoriaUploadDataset:
        return self.dm.get(request, KEY_DATOS_EN_MEMORIA_DE_UPLOAD_DATASET,DatosEnMemoriaUploadDataset())

    def intentarPasarAFaseComienzo(self,request):
        dmuld = self.getDatosEnMemoriaUploadDataset(request)
        dmuld.pasarAFase_COMIENZO()
    def detenerDescompresion(self,request):
        dmuld = self.getDatosEnMemoriaUploadDataset(request)
        estabaEnFaseDescomprimendoDataset=self.estaEnFase_DESCOMPRIMIENDO_DATASET(request)
        dmuld.pasarAFase_DETENIENDO_DESCOMPRESION_DATASET()
        if (not estabaEnFaseDescomprimendoDataset):
            print("no fue la fase descomprimendo asi que lo vamos a borrar forzado")
            self.__eliminarArchivosDeUploadDataset(request)
            dmuld.llamoAdetenerUpload = False
            dmuld.pasarAFase_COMIENZO()
        else:
            dmuld.llamoAdetenerDescompresion = True



    def detenerUpload(self,request):
        dmuld = self.getDatosEnMemoriaUploadDataset(request)
        dmuld.pasarAFase_DETENIENDO_UPLOAD_DATASET()
        dmuld.llamoAdetenerUpload=True
        print("llamo a la fase detener upload y paso al DETENIENDO_UPLOAD_DATASET")
    def sellamoADetenerUpload(self,request):
        return self.getDatosEnMemoriaUploadDataset(request).llamoAdetenerUpload

    def estaEnFase_COMIENZO(self,request):
        return self.getDatosEnMemoriaUploadDataset(request).estaEnFase_COMIENZO()

    def estaEnFase_SUVIENDO_DATASET(self,request):
        return self.getDatosEnMemoriaUploadDataset(request).estaEnFase_SUVIENDO_DATASET()
    def estaEnFase_DETENIENDO_UPLOAD_DATASET(self,request):
        return self.getDatosEnMemoriaUploadDataset(request).estaEnFase_DETENIENDO_UPLOAD_DATASET()
    def estaEnFase_ERROR_SUVIENDO_DATASET(self,request):
        return self.getDatosEnMemoriaUploadDataset(request).estaEnFase_ERROR_SUVIENDO_DATASET()
    def estaEnFase_ARCHIVO_DATASET_SUVIDO(self,request):
        return self.getDatosEnMemoriaUploadDataset(request).estaEnFase_ARCHIVO_DATASET_SUVIDO()

    def estaEnFase_DESCOMPRIMIENDO_DATASET(self,request):
        return self.getDatosEnMemoriaUploadDataset(request).estaEnFase_DESCOMPRIMIENDO_DATASET()
    def estaEnFase_DETENIENDO_DESCOMPRESION_DATASET(self,request):
        return self.getDatosEnMemoriaUploadDataset(request).estaEnFase_DETENIENDO_DESCOMPRESION_DATASET()
    def estaEnFase_DATASET_DESCOMPRIMIDO_CON_ERROR(self,request):
        return self.getDatosEnMemoriaUploadDataset(request).estaEnFase_DATASET_DESCOMPRIMIDO_CON_ERROR()

    def estaEnFase_DATASET_DESCOMPRIMIDO(self,request):
        return self.getDatosEnMemoriaUploadDataset(request).estaEnFase_DATASET_DESCOMPRIMIDO()

    def estaEnFase_DATASET_SUVIDO_CON_CLASES_ERRONEAS(self,request):
        return self.getDatosEnMemoriaUploadDataset(request).estaEnFase_DATASET_SUVIDO_CON_CLASES_ERRONEAS()

    def estaEnFase_DATASET_DESCOMPRIDO_PASO_VALIDACION(self,request):
        return self.getDatosEnMemoriaUploadDataset(request).estaEnFase_DATASET_DESCOMPRIDO_PASO_VALIDACION()

    def estaEnFase_DATASET_PROCESANDO_IMAGENES(self,request):
        return self.getDatosEnMemoriaUploadDataset(request).estaEnFase_DATASET_PROCESANDO_IMAGENES()
    def estaEnFase_DETENIENDO_PROCESAMIENTO_DE_IMAGENES(self,request):
        return self.getDatosEnMemoriaUploadDataset(request).estaEnFase_DETENIENDO_PROCESAMIENTO_DE_IMAGENES()
    def estaEnFase_TERMINANDO_LA_CREACION_DEL_DATASET(self,request):
        return self.getDatosEnMemoriaUploadDataset(request).estaEnFase_TERMINANDO_LA_CREACION_DEL_DATASET()

    def estaEnFase_TERMINO_LA_CREACION_DEL_DATASET(self,request):
        return self.getDatosEnMemoriaUploadDataset(request).estaEnFase_TERMINO_LA_CREACION_DEL_DATASET()

    def getProgresoActual(self,request):
        return self.getDatosEnMemoriaUploadDataset(request).datosDeFileDj.porcientoActual
    def getNombreArchivo(self,request):
        return self.getDatosEnMemoriaUploadDataset(request).datosDeFileDj.name
    def __eliminarDatasetEnProcesoIncompleto(self,request):
        dmuld = self.getDatosEnMemoriaUploadDataset(request)
        print("va a borrar datasetImcompleto")
        fc = File(dmuld.directorioCarpetaEnCreacionDeDatasetProcesado)
        if fc.isDir() and fc.existe():

            for f in fc.listFiles():
                print("2va a borrar a", f)
                f.delete()
            print("2va aborrar a",fc)
            fc.delete()


    def __eliminarCarpetaDescompresion(self,request):
        dmuld = self.getDatosEnMemoriaUploadDataset(request)
        urlCarpetaSalida = dmuld.carpetaDeDescompresion
        print("va a borrar desechos")
        fc = File(urlCarpetaSalida)
        if fc.isDir():

            for f in fc.listFiles():
                print("va a borrar a", f)
                f.delete()
    def __eliminarArchivosDeUploadDataset(self,request):
        dmuld = self.getDatosEnMemoriaUploadDataset(request)
        dmuld.datosDeFileDj.eliminar()
        self.__eliminarCarpetaDescompresion(request)

    def eliminarDatasetSubido(self,request):
        self.__eliminarArchivosDeUploadDataset(request)
        dmuld = self.getDatosEnMemoriaUploadDataset(request)
        # dmuld.datosDeFileDj.eliminar()
        # urlCarpetaSalida = dmuld.carpetaDeDescompresion

        dmuld.pasarAFase_COMIENZO()

    def descomprirDatasetSubido(self, request):
        if self.estaEnFase_ARCHIVO_DATASET_SUVIDO(request):
            dmuld = self.getDatosEnMemoriaUploadDataset(request)
            dmuld.pasarAFase_DESCOMPRIMIENDO_DATASET()

            if hay_carpetas_o_archivos_en_carpeta_de_descompresion(request):
                dmuld.carpetaDeDescompresion =crear_carpeta_descomprimir_de_usuario(request)
                self.__eliminarCarpetaDescompresion(request)

            dmuld.carpetaDeDescompresion = crear_carpeta_descomprimir_de_usuario(request)
            dmuld.progresoDeDescompresion = 0
            dmuld.listaDeCarpetasEnDatasetDescomprimido = []

            urlZip = dmuld.datosDeFileDj.existingPath  # get_url_archivo_comprimido_de_usuario(request,fileName)
            urlCarpetaSalida = dmuld.carpetaDeDescompresion  # r"D://_Cosas//Programacion//Proyectos//Python//Django 3.1//ProyectoPCChar//media//descomprimido"


            def verNombre(nombre):
                #print("zip f nombre=", nombre)
                if self.getDatosEnMemoriaUploadDataset(request).llamoAdetenerDescompresion:
                    #print("resulto false 1")
                    return False
                profundidad=Archivo.getProfundidad(nombre)
                if profundidad>1 and not cumpleConCondicionMinimaArchivoDentroDeComprimidoDatset(nombre):
                    #print("resulto false 2")
                    self.getDatosEnMemoriaUploadDataset(request).pasarAFase_DATASET_DESCOMPRIMIDO_CON_ERROR()
                    return False
                return True

            def verProgreso(total, indice):
                dmuld = self.getDatosEnMemoriaUploadDataset(request)
                if dmuld.llamoAdetenerDescompresion\
                        or dmuld.llamoAdetenerUpload:
                    #print("resulto false 3")
                    return False
                progreso= int(((indice / total) * 100))
                dmuld.progresoDeDescompresion = progreso
                #print("total=", total, " indice=", indice, " ",progreso, "%")
                return True
            try:
                Archivo.extraerZip_BoolContinuar(urlZip=urlZip
                                                 , urlCarpetaSalida=urlCarpetaSalida
                                                 , metodoBool_AntesDeExtraer=verNombre
                                                 , metodoBool_GetProgreso=verProgreso)
            except:
                # print("dio error al descomprimir !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                dmuld.pasarAFase_DATASET_DESCOMPRIMIDO_CON_ERROR()
            #estaEnFaseDescomprimidoConError=dmuld.estaEnFase_DATASET_DESCOMPRIMIDO_CON_ERROR()
            estaEnFaseMandoADetenerDescompresion=dmuld.estaEnFase_DETENIENDO_DESCOMPRESION_DATASET()
            if (not dmuld.estaEnFase_DATASET_DESCOMPRIMIDO_CON_ERROR()) and (not estaEnFaseMandoADetenerDescompresion):
                fc = File(urlCarpetaSalida)
                # print("fc=",fc)
                # print("fc.isDir()=",fc.isDir())
                if fc.isDir():
                    lf = fc.listFiles()
                    # print("len(lf) == 1 =",(len(lf) == 1))
                    if len(lf) == 1:
                        fcd = lf[0]
                        # print("fcd.isDir()=",fcd.isDir())
                        if fcd.isDir():
                            ddt:DatosDeCarpetaDataset = getDatosDeDataset(fcd)
                            # print("cumpleConLosRequisitosMinimosParaEntrenarCarpetaDataset(ddt)=",cumpleConLosRequisitosMinimosParaEntrenarCarpetaDataset(ddt))
                            if cumpleConLosRequisitosMinimosParaEntrenarCarpetaDataset(ddt):
                                dmuld.listaDeCarpetasEnDatasetDescomprimido = [c.nombre for c in
                                                                               ddt.listaDeCarpetasClases]
                                dmuld.carpetaDatasetDescomprimido = str(fcd)
                                dmuld.listaPar_Carpeta_CantidadDeImagenes=[[c.nombre,c.getCantidadDeImagenes()] for c in
                                                                               ddt.listaDeCarpetasClases]

                                # print("Lo paso a la fase dataset descomprimido")
                                dmuld.pasarAFase_DATASET_DESCOMPRIMIDO()

                                return None
                # print("lo paso a la fase descomprimido con error")
                dmuld.pasarAFase_DATASET_DESCOMPRIMIDO_CON_ERROR()
            if estaEnFaseMandoADetenerDescompresion or dmuld.estaEnFase_DATASET_DESCOMPRIMIDO_CON_ERROR():
                self.__eliminarArchivosDeUploadDataset(request)
                dmuld.llamoAdetenerUpload=False
                # dmuld.datosDeFileDj.eliminar()
                if estaEnFaseMandoADetenerDescompresion:
                    # print("Entro a la fase detener descompresion")
                    # print("Y lo mando al principio")
                    dmuld.pasarAFase_COMIENZO()

    def getUploadManagerInicializado(self,request):
        def alAvanzar(r, uploadManager: UploadManager, datosDeFileDj: DatosDeFileDj):
            # print("Se esta avanzando en la suvida del dataset")
            dmuld=self.getDatosEnMemoriaUploadDataset(r)
            dmuld.datosDeFileDj=datosDeFileDj
            dmuld.pasarAFase_SUVIENDO_DATASET()
        def AlTerminarConExito(r, uploadManager: UploadManager, datosDeFileDj: DatosDeFileDj):
            # print("Termino con exito la suvida del dataset")
            dmuld = self.getDatosEnMemoriaUploadDataset(r)
            dmuld.datosDeFileDj = datosDeFileDj
            dmuld.pasarAFase_ARCHIVO_DATASET_SUVIDO()
            # print("va a mandar a descomprimir")
            self.descomprirDatasetSubido(r)
        def alDarError(r, uploadManager: UploadManager,mensajeDeError):
            # print("di0 error en la suvida del dataset")
            dmuld = self.getDatosEnMemoriaUploadDataset(r)
            dmuld.pasarAFase_ERROR_SUVIENDO_DATASET()
            dmuld.mensajeDeError=mensajeDeError
        # def AlNoEncontrarLaDireccion(r, uploadManager: UploadManager, datosDeFileDj: DatosDeFileDj,mensajeDeError):
        #     dmuld = self.getDatosEnMemoriaUploadDataset(r)
        #     dmuld.datosDeFileDj = datosDeFileDj
        #     print("Error con el proseso no encontro la direcion !!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        #     dmuld.pasarAFase_ERROR_SUVIENDO_DATASET()
        #     dmuld.mensajeDeError=mensajeDeError
        def AlComenzarADetener(r, uploadManager: UploadManager, datosDeFileDj: DatosDeFileDj):
            # print("llamo a comenzar a detener la suvida del dataset")
            dmuld = self.getDatosEnMemoriaUploadDataset(r)
            dmuld.pasarAFase_DETENIENDO_UPLOAD_DATASET()
            #

        def AlTerminarDeDetener(r, uploadManager: UploadManager, datosDeFileDj: DatosDeFileDj):
            # print("llamo a terminar de detener la suvida del dataset")
            self.getDatosEnMemoriaUploadDataset(request).llamoAdetenerUpload=False
            dmuld.pasarAFase_COMIENZO()

        dmuld = self.getDatosEnMemoriaUploadDataset(request)

        umng = UploadManager()

        umng.gestorDeDatos=dmuld.gestorDeDatosUpload
        umng.metodoGetUrlSalidaArchivo=lambda r,s,fileName:get_url_archivo_comprimido_de_usuario(r,fileName)
        #umng.nameInputFile = nombreInputFile
        umng.metodoAlAvanzar=alAvanzar
        umng.metodoAlTerminarConExito = AlTerminarConExito
        #umng.AlNoEncontrarLaDireccion = AlNoEncontrarLaDireccion
        umng.alDarError = alDarError

        umng.metodoAlComenzarADetener = AlComenzarADetener
        umng.metodoAlTerminarDeDetener = AlTerminarDeDetener

        #umng.detener_upload=dmuld.llamoAdetenerUpload
        umng.condicionDetenerUpload=lambda r,uploadoManager:dmuld.llamoAdetenerUpload
        return umng

    def esValidoMatrisDeclasificaciones(self,request,matrisDeClasificaciones):
        return RespuestaDeValidacionDeMarisDeclasificaciones\
            .esValidoMatrisDeclasificaciones(
            matrisDeClasificaciones,self.getDatosEnMemoriaUploadDataset(request).listaDeCarpetasEnDatasetDescomprimido
        )
        # #print("matrisDeClasificaciones=",matrisDeClasificaciones)
        # r=RespuestaDeValidacionDeMarisDeclasificaciones()
        #
        # dmuld = self.getDatosEnMemoriaUploadDataset(request)
        # if not len(matrisDeClasificaciones)==len(dmuld.listaDeCarpetasEnDatasetDescomprimido):
        #     r.esValido = False
        #     r.mensaje = "La cantidad de clasificaciones tiene que ser la misma que la cantidad de carpetas que representas estas clasificaciones "
        #     return r
        # listaDeClasificaciones=[]
        # listaDeNombresCarpeta = []
        # for i in range(len(matrisDeClasificaciones)):
        #     row=matrisDeClasificaciones[i]
        #     print("i=",i," row=",row)
        #     clasificacion=row[0].strip()
        #     nombreCarpeta=row[1].strip()
        #
        #     if clasificacion in listaDeClasificaciones:
        #         r.esValido=False
        #         r.mensaje="No puede existir Clasificaciones iguales "
        #         return r
        #     listaDeClasificaciones.append(clasificacion)
        #     if nombreCarpeta in listaDeNombresCarpeta:
        #         r.esValido=False
        #         r.mensaje="No puede existir carpetas con el mismo nombre"
        #         return r
        #     listaDeNombresCarpeta.append(nombreCarpeta)
        #
        #     if not nombreCarpeta in dmuld.listaDeCarpetasEnDatasetDescomprimido:
        #         # print("nombreCarpeta=",nombreCarpeta)
        #         # print("dmuld.listaDeCarpetasEnDatasetDescomprimido=",dmuld.listaDeCarpetasEnDatasetDescomprimido)
        #         r.esValido = False
        #         r.mensaje = "Tienen que coincidir con los nombres reales de las carpetas del Dataset "
        #         return r
        #
        # r.esValido=True
        # return r



    def llamoADetener_ProcesamientoDeImagenes(self,request):
        dmuld = self.getDatosEnMemoriaUploadDataset(request)
        estabaEnProcesadoImagenes = self.estaEnFase_DATASET_PROCESANDO_IMAGENES(request)
        dmuld.llamoADetenerProcesamientoDeImagenes=True
        #dmuld.pasarAFase_DETENIENDO_DESCOMPRESION_DATASET()
        dmuld.pasarAFase_DETENIENDO_PROCESAMIENTO_DE_IMAGENES()
        if (not estabaEnProcesadoImagenes):
            print("no fue la fase prosesando imagenes asi que lo vamos a borrar forzado")
            self.__eliminarDatasetEnProcesoIncompleto(request)
            dmuld.llamoADetenerProcesamientoDeImagenes = False
            dmuld.pasarAFase_DATASET_DESCOMPRIMIDO()

    def llamoAResetearEstados(self,request):
        dmuld = self.getDatosEnMemoriaUploadDataset(request)
        dmuld.pasarAFase_COMIENZO()

        dmuld.datosDeimagenEnProcesamiento= None
        dmuld.datosDeFileDj = DatosDeFileDj()
        dmuld.mensajeDeError = ""

        dmuld.gestorDeDatosUpload = GestorDeDatosUpload()

        dmuld.llamoAdetenerUpload = False

        dmuld.llamoAdetenerDescompresion = False
        dmuld.carpetaDeDescompresion = None
        dmuld.carpetaDatasetDescomprimido = None
        dmuld.progresoDeDescompresion = 0

        dmuld.listaDeCarpetasEnDatasetDescomprimido = []
        dmuld.listaPar_Carpeta_CantidadDeImagenes = []

        dmuld.estadoDeProcesamientoDeImagenes = None
        dmuld.directorioCarpetaEnCreacionDeDatasetProcesado = None
        dmuld.directorioCarpetaEnCreacionDeDatasetNoProcesado = None
        dmuld.llamoADetenerProcesamientoDeImagenes = False
        dmuld.datosDelDataset = None


    def crearDatasetProcesado(self,request,dt:DatosDelDataset):
        dmuld = self.getDatosEnMemoriaUploadDataset(request)

        eliminar_carpeta_dataset_incompleto_Si_hay_carpetas_o_archivos(request,dt.nombre)


        dmuld.directorioCarpetaEnCreacionDeDatasetProcesado = get_nueva_url_dataset_incompleto(request,dt.nombre)
        #dmuld.directorioCarpetaEnCreacionDeDatasetProcesado = get_nueva_url_dataset_incompleto_SiExisteCambiarNombre(request, dt.nombre)

        entrada = dmuld.carpetaDatasetDescomprimido
        salida = dmuld.directorioCarpetaEnCreacionDeDatasetProcesado



        def antesDeComenzarAProcesarLaImagen(args: ArgumentosDeEventosAlProcesarYcrearDataSet):
            dmuld = self.getDatosEnMemoriaUploadDataset(request)
            if dmuld.llamoADetenerProcesamientoDeImagenes:
                return False

            dmuld.estadoDeProcesamientoDeImagenes=args
            dmuld.pasarAFase_DATASET_PROCESANDO_IMAGENES()
            return True

        def antesDeAplicar_grayWorld(args: ArgumentosDeEventosAlProcesarYcrearDataSet):
            dmuld = self.getDatosEnMemoriaUploadDataset(request)
            if dmuld.llamoADetenerProcesamientoDeImagenes:
                return False

            dmuld.estadoDeProcesamientoDeImagenes = args
            return True

        def antesDeAplicar_boundingBox(args: ArgumentosDeEventosAlProcesarYcrearDataSet):
            dmuld = self.getDatosEnMemoriaUploadDataset(request)
            if dmuld.llamoADetenerProcesamientoDeImagenes:
                return False

            dmuld.estadoDeProcesamientoDeImagenes = args
            return True

        def antesDeAplicar_mresize(args: ArgumentosDeEventosAlProcesarYcrearDataSet):
            dmuld = self.getDatosEnMemoriaUploadDataset(request)
            if dmuld.llamoADetenerProcesamientoDeImagenes:
                return False

            dmuld.estadoDeProcesamientoDeImagenes = args
            return True

        def antesDeAplicar_cielAB(args: ArgumentosDeEventosAlProcesarYcrearDataSet):
            dmuld = self.getDatosEnMemoriaUploadDataset(request)
            if dmuld.llamoADetenerProcesamientoDeImagenes:
                return False

            dmuld.estadoDeProcesamientoDeImagenes = args
            return True

        def alTerminarConExito(args: ArgumentosDeEventosAlProcesarYcrearDataSet):
            dmuld = self.getDatosEnMemoriaUploadDataset(request)
            if dmuld.llamoADetenerProcesamientoDeImagenes:
                return False

            dmuld.estadoDeProcesamientoDeImagenes = args
            return True

        listaPar_NombreCarpeta_CantidadDeImagenes =dmuld.listaPar_Carpeta_CantidadDeImagenes #dt.matrizPar_Clasificacion_Carpeta
        eventos = EventosAlProcesarYcrearDataSet(
            listaPar_NombreCarpeta_CantidadDeImagenes=listaPar_NombreCarpeta_CantidadDeImagenes
            , antesDeComenzarAProcesarLaImagen=antesDeComenzarAProcesarLaImagen
            , antesDeAplicar_grayWorld=antesDeAplicar_grayWorld
            , antesDeAplicar_boundingBox=antesDeAplicar_boundingBox
            , antesDeAplicar_mresize=antesDeAplicar_mresize
            , antesDeAplicar_cielAB=antesDeAplicar_cielAB
            , alTerminarConExito=alTerminarConExito
        )
        procesarYcrearDataSet_BoolSiContinuar(
            carpetaImagenesOriginales=entrada
            , carpetaSalidaDataSet=salida
            , eventos=eventos
        )
        r=RespestaDeMetodoIntentarCrearDataset()
        if dmuld.llamoADetenerProcesamientoDeImagenes:
            dmuld.pasarAFase_DETENIENDO_PROCESAMIENTO_DE_IMAGENES()
            #dmuld.pasarAFase_DETENIENDO_DESCOMPRESION_DATASET()
            self.__eliminarDatasetEnProcesoIncompleto(request)
            dmuld.llamoADetenerProcesamientoDeImagenes=False
            dmuld.pasarAFase_DATASET_DESCOMPRIMIDO()
            r.mandoADetener=True
        else:
            #eliminar_CarpetaContenedoraDeDatasetCompleto_ProcesadoYNoProcesado_Si_hay_carpetas_o_archivos(request,dt.nombre)

            direccionContenedorDataset=getYCrear_CarpetaContenedoraDeDatasetCompleto_ProcesadoYNoProcesado_SiExisteCrearNuevo(request,dt.nombre) #request,dt.nombre

            dmuld.pasarAFase_TERMINANDO_LA_CREACION_DEL_DATASET()
            dmuld.directorioCarpetaEnCreacionDeDatasetProcesado = File(
                dmuld.directorioCarpetaEnCreacionDeDatasetProcesado)\
                .move(getYCrear_CarpetaContenedoraDeDatasetCompleto_Procesado_DesdeContenedorDataset(direccionContenedorDataset))
            if dmuld.directorioCarpetaEnCreacionDeDatasetProcesado is not None:
                #eliminar_carpetaContenedoraDeDatasetCompleto_NoProcesado_Si_hay_carpetas_o_archivos(request,dt.nombre)

                dmuld.directorioCarpetaEnCreacionDeDatasetNoProcesado = File(
                    dmuld.carpetaDatasetDescomprimido) \
                    .move(getYCrear_CarpetaContenedoraDeDatasetCompleto_NoProcesado_DesdeContenedorDataset(direccionContenedorDataset))
                if dmuld.directorioCarpetaEnCreacionDeDatasetNoProcesado is not None:
                    print("accion con la bd")



                    cantidadDeImagenes=0
                    for carpeta,cantidad in listaPar_NombreCarpeta_CantidadDeImagenes:
                        cantidadDeImagenes+=cantidad
                        carpetaImagenDeEjemplo50px=getYCrear_CarpetaContenedoraDeDatasetCompleto_ImagenDeEjemplo50px_DesdeContentedorDataset(direccionContenedorDataset,carpeta)

                        carpetaDeOrininal=File(str(dmuld.directorioCarpetaEnCreacionDeDatasetNoProcesado)+"/"+carpeta)
                        # print("carpetaDeOrininal=", carpetaDeOrininal)

                        primeraImagenDeCarpetaOriginal=carpetaDeOrininal.listFiles()[0]

                        salidaImagenDeEjemplo50px=File(str(carpetaImagenDeEjemplo50px)+"/"+primeraImagenDeCarpetaOriginal.getName())
                        # print("primeraImagenDeCarpetaOriginal=",primeraImagenDeCarpetaOriginal)
                        # print("salidaImagenDeEjemplo=",salidaImagenDeEjemplo)
                        mresize(urlImg=str(primeraImagenDeCarpetaOriginal)
                                ,urlSalida=str(salidaImagenDeEjemplo50px)
                                ,size=[50,50])


                        carpetaImagenDeEjemplo900_600px = getYCrear_CarpetaContenedoraDeDatasetCompleto_ImagenDeEjemplo900_600px_DesdeContentedorDataset(direccionContenedorDataset,carpeta)
                        salidaImagenDeEjemplo900_600px = File(
                            str(carpetaImagenDeEjemplo900_600px) + "/" + primeraImagenDeCarpetaOriginal.getName())
                        mresize(urlImg=str(primeraImagenDeCarpetaOriginal)
                                , urlSalida=str(salidaImagenDeEjemplo900_600px)
                                , size=[900, 600])

                    matris_Clasificacion_NombreCarpeta_CantidadDeImagenes=[]
                    #for clasificacion,carpeta in dt.matrizPar_Clasificacion_Carpeta:
                    for clasificacion, carpeta,descripcion in dt.matris_Clasificacion_Carpeta_Descripcion:
                        for carpeta2, cantidad in listaPar_NombreCarpeta_CantidadDeImagenes:
                            if carpeta==carpeta2:
                                matris_Clasificacion_NombreCarpeta_CantidadDeImagenes.append([clasificacion
                                                                                              ,carpeta
                                                                                              ,cantidad
                                                                                              ,descripcion
                                                                                              ])
                                break
                    clasesEnOrdenParaEntrenamiento=getClasesDeDatasetEn(dmuld.directorioCarpetaEnCreacionDeDatasetProcesado)

                    for i,nombre_clase in enumerate(clasesEnOrdenParaEntrenamiento):
                        for j,Clasificacion_NombreCarpeta_CantidadDeImagenes in enumerate(matris_Clasificacion_NombreCarpeta_CantidadDeImagenes):
                            nombre_carpeta=Clasificacion_NombreCarpeta_CantidadDeImagenes[1]
                            if nombre_clase==nombre_carpeta:
                                Clasificacion_NombreCarpeta_CantidadDeImagenes.append(i)
                                break
                    print("matris_Clasificacion_NombreCarpeta_CantidadDeImagenes=",matris_Clasificacion_NombreCarpeta_CantidadDeImagenes)





                    dataset=bd.saveDataset(
                        Direccion_Imagenes_Procesadas=getDireccionRealtivaDeDataset(dmuld.directorioCarpetaEnCreacionDeDatasetProcesado)#str(dmuld.directorioCarpetaEnCreacionDeDatasetProcesado.getName())
                        ,Direccion_Imagenes_Originales=getDireccionRealtivaDeDataset(dmuld.directorioCarpetaEnCreacionDeDatasetNoProcesado)#str(dmuld.directorioCarpetaEnCreacionDeDatasetNoProcesado.getName())
                        ,Nombre=dt.nombre
                        ,Descripcion=dt.descripcion
                        ,CantidadDeImagenes=cantidadDeImagenes

                        ,Fruto=bd.getFruto_id(dt.tipoDeFruto)
                        ,usuario=getUserRequest(request)
                        ,matris_Clasificacion_NombreCarpeta_CantidadDeImagenes=matris_Clasificacion_NombreCarpeta_CantidadDeImagenes
                    )

                    dmuld.datosDeFileDj.eliminar()
                    #self.__eliminarArchivosDeUploadDataset(request)
                    dmuld.pasarAFase_TERMINO_LA_CREACION_DEL_DATASET()
                    r.terminoConExito=True
                    r.mandoADetener = False
                    return  r

            dmuld.pasarAFase_DATASET_DESCOMPRIMIDO()
            r.terminoConError=True
            r.mandoADetener = False

        return r


logicaUploadDataset:LogicaUploadDataset=LogicaUploadDataset(APP_CNF)
#
#
# class DatosEnMemoriaUploadDataset:
#     def __init__(self):
#         indice = -1
#         self.esta_en_fase_comienzo=DatosDeFaseUploadDataset(True,++indice)#0
#         self.esta_en_fase_suviendo_dataset=False#1
#         self.esta_en_fase_descomprimiendo_dataset = False#2
#         self.esta_en_fase_dataset_descomprimido_con_error = False#3
#         self.esta_en_fase_dataset_descomprimido = False#4
#         self.esta_en_fase_dataset_suvido_con_clases_erroneas = False#5
#         self.esta_en_fase_dataset_descomprido_paso_validacion=False#6
#         self.esta_en_fase_dataset_procesando_imagenes = False#7
#         self.esta_en_fase_termino_la_creacion_deldataset=False#8
#
#
#         self.datosDeimagenEnProcesamiento:DatosDeImagenEnProcesamientoParaCreacionDataset=None
#         self.datosDeFileDj: DatosDeFileDj=DatosDeFileDj()
#     def __initFasesDeListaBool(self,listaBool):
#         indice=-1
#         self.esta_en_fase_comienzo = listaBool[++indice]
#         self.esta_en_fase_suviendo_dataset = listaBool[++indice]
#         self.esta_en_fase_descomprimiendo_dataset = listaBool[++indice]
#         self.esta_en_fase_dataset_descomprimido_con_error = listaBool[++indice]
#         self.esta_en_fase_dataset_descomprimido = listaBool[++indice]
#         self.esta_en_fase_dataset_suvido_con_clases_erroneas = listaBool[++indice]
#         self.esta_en_fase_dataset_descomprido_paso_validacion = listaBool[++indice]
#         self.esta_en_fase_dataset_procesando_imagenes = listaBool[++indice]
#         self.esta_en_fase_termino_la_creacion_deldataset = listaBool[++indice]
#     def __setFase(self,indice):
#         self.__initFasesDeListaBool([b for i in range()])
#     def pasarAFase_comienzo(self):
#         self.esta_en_fase_comienzo = True
#         self.esta_en_fase_suviendo_dataset = False
#         self.esta_en_fase_descomprimiendo_dataset = False
#         self.esta_en_fase_dataset_descomprimido_con_error = False
#         self.esta_en_fase_dataset_descomprimido = False
#         self.esta_en_fase_dataset_suvido_con_clases_erroneas = False
#         self.esta_en_fase_dataset_descomprido_paso_validacion = False
#         self.esta_en_fase_dataset_procesando_imagenes = False
#         self.esta_en_fase_termino_la_creacion_deldataset = False
#
#     def pasarAFase_suviendo_dataset(self):
#         self.esta_en_fase_comienzo = True
#         self.esta_en_fase_suviendo_dataset = False
#         self.esta_en_fase_descomprimiendo_dataset = False
#         self.esta_en_fase_dataset_descomprimido_con_error = False
#         self.esta_en_fase_dataset_descomprimido = False
#         self.esta_en_fase_dataset_suvido_con_clases_erroneas = False
#         self.esta_en_fase_dataset_descomprido_paso_validacion = False
#         self.esta_en_fase_dataset_procesando_imagenes = False
#         self.esta_en_fase_termino_la_creacion_deldataset = False

