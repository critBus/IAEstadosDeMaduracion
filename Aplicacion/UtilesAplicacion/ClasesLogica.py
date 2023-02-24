from ReneDjangoApp.Utiles.Utiles import *
from Aplicacion.UtilesAplicacion.ConstantesApp import *
from typing import TYPE_CHECKING, Dict, List, NoReturn, Optional, Union, Tuple, cast, ClassVar
from Aplicacion.ReneIAClasificador.entrenador_v2_0 import getMetricasDeClase,MetricasDeClase
from datetime import datetime

def __getStrDate(d,getStr_Fecha):


    if not isinstance(d, datetime):
        d = datetime.strptime(str(d),"%Y-%m-%d %H:%M:%S.%f")
    if isinstance(d, datetime):
        return getStr_Fecha(año="%04d" % (d.year)
                            , mes="%02d" % (d.month)
                            , dia="%02d" % (d.day)
                            , hora="%02d" % (d.hour)
                            , minutos="%02d" % (d.minute)
                            , segundos="%02d" % (d.second)
                            , microsegundos="%04d" % (d.microsecond)
                            )
    return ""
def getStrDate(d):
    def getStr_Fecha(año, mes, dia, hora, minutos, segundos, microsegundos):
        return strg(año, "-", mes, "-", dia, " ", hora, ":", minutos)
    return __getStrDate(d,getStr_Fecha)
def getStrDateEnImg(d):
    def getStr_Fecha(año, mes, dia, hora, minutos, segundos, microsegundos):
        return strg(año, "-", mes, "-", dia, "_", hora, "_", minutos, "_",segundos)
    return __getStrDate(d,getStr_Fecha)
def getStrDateEnImgNow():
    return getStrDateEnImg(datetime.now())


# def crearImgDatos(request,img,nombre=None):
#     if img is not None:
#         extencion=img.Formato
#         dimg = ImageFieldBlob.crearImg(imageFieldBlob=img.Contenido
#                                        ,request=request
#                                        ,app_conf= APP_CNF
#                                        ,nombre= nombre
#                                        ,extencion=extencion)
#         return dimg
#     return None

class DatosDeClasificacion:
    def __init__(self):
        self.datosDeImagenOriginal: DatosDeImagenTempDj = None
        self.clasificacion = None
        self.fecha=None
        self.modelo=None

        self.fruto=None
        self.variedadFruto = None
        self.nombreCientificoFruto = None

        self.idClasificacion = None






    @staticmethod
    def getDatosDeClasificacion(clasificacion,bd,nombreExtra=None):
        d=DatosDeClasificacion()
        d.datosDeImagenOriginal =APP_CNF.getDireccionRelativa_DeCampoImagen(clasificacion.Procesamiento.ImagenOriginal)
        # d.datosDeImagenOriginal=crearImgDatos(request=request
        #                                       ,img=clasificacion.Imagen
        #                                       )
        d.fecha=getStrDate(clasificacion.Fecha)
        modelo=clasificacion.ModeloNeuronal
        #d.fruto=modelo.Fruto#modelo.Fruto.Nombre

        dataset = bd.getDataset_ModeloNeuronal(modelo)

        d.fruto = dataset.Fruto.Nombre  # modelo.Fruto
        d.variedadFruto = dataset.Fruto.Variedad
        d.nombreCientificoFruto = dataset.Fruto.NombreCientifico

        d.modelo=modelo.Nombre
        d.clasificacion=clasificacion.Resultado
        d.idClasificacion=clasificacion.id
        return d





class DatosDeClasificacionYProcesamiento(DatosDeClasificacion):
    def __init__(self):
        super().__init__()
        self.datosDeImagenGrayWorld: DatosDeImagenTempDj = None
        self.datosDeImagenBoundingBox: DatosDeImagenTempDj = None
        self.datosDeImagenMResize: DatosDeImagenTempDj = None
        self.datosDeImagenCielAB: DatosDeImagenTempDj = None

        # self.datosDeImagenOriginal: DatosDeImagenTempDj = None
        # self.clasificacion=None

class Clase_RespuestaClasificacion:
    def __init__(self):
        self.nombre=None
        self.seleccionada=False
# class DatosDeImagenRespuesta:
#     def __init__(self):
#         self.datosDeImagenOriginal:DatosDeImagenTempDj=None
#         self.algoritmo=None

class RespuestaClasificacionYProcesamiento(DatosDeClasificacionYProcesamiento):
    def __init__(self):
        super().__init__()
        self.clases=None

        self.idProcesamientoDeImagen=None
    def crearClasesDeRespuesta(self):
        clasesCrudas=self.clases
        self.clases=[]
        for nombre in clasesCrudas:
            cr=Clase_RespuestaClasificacion()
            cr.nombre=nombre
            if nombre==self.clasificacion:
                cr.seleccionada=True
            self.clases.append(cr)

class ConjuntoProcesamientoYClasificacion:
    def __init__(self):
        self.clasificaion=None
        self.procesamiento=None
        self.imagen = None



class ConjuntoAlgoritoYImagen:
    def __init__(self):
        self.imagenProcesada=None
        self.imagen=None


class ConjuntoProcesamiento_Clasificacion_Algoritmos(ConjuntoProcesamientoYClasificacion):
    def __init__(self):
        super().__init__()
        self.listaDeConjuntoAlgoritoYImagen=[]

class DatosDataset:
    def __init__(self,dataset,bd):
        self.id=dataset.id
        self.nombre=dataset.Nombre
        self.nombreUsuario=dataset.User.username
        #self.fruto=dataset.Fruto

        self.fruto = dataset.Fruto.Nombre  # modelo.Fruto
        self.variedadFruto = dataset.Fruto.Variedad
        self.nombreCientificoFruto = dataset.Fruto.NombreCientifico
        self.IdFruto=dataset.Fruto.id

        self.fechaDeCreacion=dataset.FechaDeCreacion
        self.descripcion=dataset.Descripcion

        self.cantidadDeImagenes=dataset.CantidadDeImagenes

        clasesDeClasificaciones=bd.getClaseDeClasificacion_SortVisual_All_Dataset(dataset)

        self.clasificaciones=[c.Nombre for c in clasesDeClasificaciones]
        self.cantidadDeClasificaciones=0
        for c in clasesDeClasificaciones:
            self.cantidadDeClasificaciones+=1

        self.matris_Clasificacion_CantidadDeImagenes=[[c.Nombre,c.CantidadDeImagenes] for c in clasesDeClasificaciones]
        self.matris_Clasificacion_Carpeta_Descripcion = [
            [c.Nombre,  c.NombreCarpetaCorrespondiente, c.Descripcion] for c in
            clasesDeClasificaciones]


    @staticmethod
    def getDatosDataset(bd):
        l=bd.getDatasetAll()
        return [DatosDataset(e,bd) for e in l]
class RepresentacionDeEpoca:
    def __init__(self):
        self.epoca=None
        self.precision_Epoca = None
        self.perdida_Epoca = None
        self.listaDeLotes=[]
class RepresentacionDeDatoDeLoteEnHistorialDeEntrenamiento:
    def __init__(self):
        self.epoca=None
        self.lote=None
        self.cantidadDeLotes=None
        self.cantidadDeEpocas=None
        self.precision_Lote=None
        self.perdida_Lote=None
        self.precision_Epoca = None
        self.perdida_Epoca = None

class DatosModeloNeuronal:
    def __init__(self,modelo,bd):
        self.id=modelo.id
        self.nombre=modelo.Nombre
        self.nombreUsuario=modelo.User.username

        self.fechaDeCreacion=modelo.FechaDeCreacion
        self.descripcion=modelo.Descripcion

        self.cantidadDeEpocas=modelo.CantidadDeEpocas
        self.precision=modelo.Precision
        self.perdida=modelo.Perdida
        dataset=bd.getDataset_ModeloNeuronal(modelo)

        self.fruto = dataset.Fruto.Nombre#modelo.Fruto
        self.variedadFruto=dataset.Fruto.Variedad
        self.nombreCientificoFruto = dataset.Fruto.NombreCientifico
        self.idFruto=dataset.Fruto.id
        #print("dataset.id=",dataset.id)
        self.idDataset=dataset.id
        #print("dataset.Nombre=", dataset.Nombre)
        self.nombreDataset=dataset.Nombre
        validacion=bd.getValidacion_ModeloNeuronal(modelo)
        self.porcientoDeValidacion=validacion.Porcentaje_Utilizado_Del_Dataset
        self.usoPorcientoDeValidacion=self.porcientoDeValidacion!=100

        self.idDatasetValidacion=validacion.Dataset.id
        self.nombreDatasetValidacion = validacion.Dataset.Nombre
        self.mismoDatasetParaValidacion=self.idDatasetValidacion==self.idDataset



        clasesDeClasificaciones=bd.getClaseDeClasificacion_SortVisual_All_ModeloNeuronal(modelo)

        self.clasificaciones=[c.Nombre for c in clasesDeClasificaciones]
        self.cantidadDeClasificaciones=len(clasesDeClasificaciones)
        # for c in clasesDeClasificaciones:
        #     self.cantidadDeClasificaciones+=1

        self.matriz_Clasificacion_CantidadDeImagenes=[[c.Nombre,c.CantidadDeImagenes] for c in clasesDeClasificaciones]

        self.matriz_de_confusion=[[0 for j in range(self.cantidadDeClasificaciones)] for i in range(self.cantidadDeClasificaciones) ]
        datosEnMatrizDeConfusion=bd.getDatoEnMatrizDeConfusion_All_Validacion(validacion)
        for d in datosEnMatrizDeConfusion:
            self.matriz_de_confusion[d.Indice_fila][d.Indice_columna]=d.Cantidad
        self.metricas:List[MetricasDeClase]=getMetricasDeClase(self.matriz_de_confusion)
        self.matriz_Clasificacion_Metrica=[]
        for i,c in enumerate(self.clasificaciones):
            self.matriz_Clasificacion_Metrica.append([c,self.metricas[i]])

        self.matriz_RepresentacionDeEpoca = bd.getRepresentacionesDeEpoca(
            entrenamiento=bd.getEntrenamiento_ModeloNeuronal(modelo))

        self.listaDePrecision = [p.precision_Epoca for p in self.matriz_RepresentacionDeEpoca]
        self.listaDePerdida = [p.perdida_Epoca for p in self.matriz_RepresentacionDeEpoca]

        # self.matriz_RepresentacionDeDatoDeLoteEnHistorialDeEntrenamiento=bd.getMatriz_RepresentacionDeDatoDeLoteEnHistorialDeEntrenamiento(entrenamiento=bd.getEntrenamiento_ModeloNeuronal(modelo))
        #
        # self.listaDePrecision=[p[1][0].precision_Epoca for p in self.matriz_RepresentacionDeDatoDeLoteEnHistorialDeEntrenamiento if len(p[1])>0]
        # self.listaDePerdida = [p[1][0].perdida_Epoca for p in
        #                          self.matriz_RepresentacionDeDatoDeLoteEnHistorialDeEntrenamiento if len(p[1]) > 0]




    @staticmethod
    def getDatosModelosNeuronales(bd):
        l=bd.getModelosNeuronalesAll()
        return [DatosModeloNeuronal(e,bd) for e in l]


class RepresentacionDeUsuario:
    def __init__(self):
        self.username=None
        self.nombre=None
        self.apellidos = None
        self.correo = None

        self.id=None
        self.permiso=None
        self.fechaDeCreacion=None
        self.enable=None

class RespuestaDeValidacionDeMarisDeclasificaciones:
    def __init__(self):
        self.esValido=False
        self.mensaje=""

    @staticmethod
    def esValidoMatrisDeclasificaciones(matrisDeClasificaciones,listaDeCarpetas):
        r = RespuestaDeValidacionDeMarisDeclasificaciones()


        if not len(matrisDeClasificaciones) == len(listaDeCarpetas):
            r.esValido = False
            r.mensaje = "La cantidad de clasificaciones tiene que ser la misma que la cantidad de carpetas que representas estas clasificaciones "
            return r
        listaDeClasificaciones = []
        listaDeNombresCarpeta = []
        for i in range(len(matrisDeClasificaciones)):
            row = matrisDeClasificaciones[i]
            print("i=", i, " row=", row)
            clasificacion = row[0].strip()
            nombreCarpeta = row[1].strip()

            if clasificacion in listaDeClasificaciones:
                r.esValido = False
                r.mensaje = "No puede existir Clasificaciones iguales "
                return r
            listaDeClasificaciones.append(clasificacion)
            if nombreCarpeta in listaDeNombresCarpeta:
                r.esValido = False
                r.mensaje = "No puede existir carpetas con el mismo nombre"
                return r
            listaDeNombresCarpeta.append(nombreCarpeta)

            if not nombreCarpeta in listaDeCarpetas:
                r.esValido = False
                r.mensaje = "Tienen que coincidir con los nombres reales de las carpetas del Dataset "
                return r

        r.esValido = True
        return r


class DatosDeFruto:
    def __init__(self,fruto):
        self.nombre=fruto.Nombre
        self.nombreCientifico=fruto.NombreCientifico
        self.variedad=fruto.Variedad
        self.descripcion=fruto.Descripcion
        self.id=fruto.id
        self.fecha=fruto.Fecha

    @staticmethod
    def getDatosDeFrutos(bd):
        l=bd.getFrutosAll()
        return [DatosDeFruto(e) for e in l]


class ConfiguracionDePaginacionDeImg:
    STEP=30
    INDICES=5
# class ConjuntoDatasets:
#     def __init__(self):
#         self.