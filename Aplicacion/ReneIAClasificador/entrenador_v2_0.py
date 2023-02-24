import tensorflow as tf
import numpy as np
import pathlib
from sklearn.metrics import confusion_matrix
from tensorflow import keras

#from ReneDjangoApp.Utiles.MetodosUtiles.Archivo import recorrerCarpetaYUtilizarSubCarpetas_BolContinuar
from twisted.conch.insults.insults import privateModes

from ReneDjangoApp.Utiles.MetodosUtiles import Archivo,UtilesImg
from ReneDjangoApp.Utiles.Clases import File,TipoDeImagen

from keras.models import model_from_json
from keras.models import model_from_yaml
from pandas import HDFStore

from keras.models import load_model
from typing import TYPE_CHECKING, Dict, List, NoReturn, Optional, Union, Tuple, cast, ClassVar

def guardarModelo_Keras(model,urlH5):
    model.save(urlH5)
def cargarModelo_Keras(urlH5):
    model = load_model(urlH5)
    return model

def cargarModelo_Pandas(urlH5):
    hdf = HDFStore(urlH5)
    return urlH5

def guardarModelo_JSON_Keras(model,urlH5,urlJson):
    # serializa el modelo para JSON
    model_json = model.to_json()
    with open(urlJson, "w") as json_file:
      json_file.write(model_json)
    #serializan los pesos (weights) para HDF5
    model.save_weights(urlH5)

def cargarModelo_JSON_Keras(urlH5,urlJson):
    # carga el json y crea el modelo
    json_file = open(urlJson, 'r')
    loaded_model_json = json_file.read()

    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # se cargan los pesos (weights) en el nuevo modelo
    loaded_model.load_weights(urlH5)

    # se evalua el modelo cargado con los datos de los test
    loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    return loaded_model

def guardarModelo_ÝAML_Keras(model,urlH5,urlYaml):
    model_yaml = model.to_yaml()
    with open(urlYaml, "w") as yaml_file:
        yaml_file.write(model_yaml)
    # serializa los pesos(weights) para HDF5
    model.save_weights(urlH5)

def cargarModelo_ÝAML_Keras(urlH5,urlYaml):
    # carga del YAML y crea el modelo
    yaml_file = open(urlYaml, 'r')
    loaded_model_yaml = yaml_file.read()
    yaml_file.close()
    loaded_model = model_from_yaml(loaded_model_yaml)
    # cargamos los pesos (weights) en el nuevo modelo
    loaded_model.load_weights(urlH5)
    # evalua el modelo con los datos test
    loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    return loaded_model


class ArchivosEnDisco:
    def __init__(self):
        self.cantidad=0
        self.espacioEnDiscoEnMB = 0
    def isEmpty(self):
        return self.cantidad==0

class ArchivosNoTipoImagen(ArchivosEnDisco):
    def __init__(self):
        ArchivosEnDisco.__init__(self)
        self.listaDeExtenciones=[]

class ArchivosTipoImagen(ArchivosEnDisco):
    def __init__(self):
        ArchivosEnDisco.__init__(self)
        self.tipo=None


class DatosDeClaseDeClasificacionDeImagenesDeDataset:
    def __init__(self):
        #self.cantidadDeImagenes=0
        self.nombre=""
        self.datosDeArchivosTipoImagen=[]#ArchivosTipoImagen()
        self.datosDeArchivosQueNoSonTipoImagen=ArchivosNoTipoImagen()
    def addTipoDeImagen(self,tipo,espacioEnDiscoEnMB):
        for e in self.datosDeArchivosTipoImagen:
            if e.tipo==tipo:
                e.cantidad+=1
                e.espacioEnDiscoEnMB+=espacioEnDiscoEnMB
                return None
        ATimg=ArchivosTipoImagen()
        ATimg.tipo=tipo
        ATimg.cantidad+=1
        ATimg.espacioEnDiscoEnMB += espacioEnDiscoEnMB
        self.datosDeArchivosTipoImagen.append(ATimg)

    def getCantidadDeImagenes(self):
        r = 0
        for e in self.datosDeArchivosTipoImagen:
            r+=e.cantidad
        return r
    #     return self.datosDeArchivosTipoImagen.cantidad
        # r=0
        # for e in self.listaDeClases:
        #     r+=e.cantidadDeImagenes
        # return r
    def getEspacioEnDiscoEnMB(self):
        r = self.datosDeArchivosQueNoSonTipoImagen.espacioEnDiscoEnMB
        for e in self.datosDeArchivosTipoImagen:
            r += e.espacioEnDiscoEnMB
        return r
        #return self.datosDeArchivosTipoImagen.espacioEnDiscoEnMB + self.datosDeArchivosQueNoSonTipoImagen.espacioEnDiscoEnMB
        # r = 0
        # for e in self.listaDeClases:
        #     r += e.espacioEnDiscoEnMB
        # return r

    def tieneImagenes(self):
        return len(self.datosDeArchivosTipoImagen)>0 and not self.datosDeArchivosTipoImagen[0].isEmpty()

    def sonSoloImagenes(self):
        return self.tieneImagenes() and self.datosDeArchivosQueNoSonTipoImagen.isEmpty()

class DatosDeCarpetaDataset:
    def __init__(self,urlCarpeta):
        self.listaDeCarpetasClases=[]
        self.urlCarpeta:str=urlCarpeta
        
    def getCantidadDeClases(self):
        return len(self.listaDeCarpetasClases)
    def getCantidadDeImagenes(self):
        r=0
        for e in self.listaDeCarpetasClases:
            r+=e.getCantidadDeImagenes()#.cantidadDeImagenes
        return r
    def getEspacioEnDiscoEnMB(self):
        r = 0
        for e in self.listaDeCarpetasClases:
            r += e.getEspacioEnDiscoEnMB()
        return r
    def sonSoloImagenes(self):
        for e in self.listaDeCarpetasClases:
            #if (not e.datosDeArchivosQueNoSonTipoImagen.isEmpty()) and (not e.datosDeArchivosTipoImagen.isEmpty()):
            if not e.sonSoloImagenes():
                return False
        return True
    def todasLasCarpetasTienenImagenes(self):
        for e in self.listaDeCarpetasClases:
            #if e.datosDeArchivosTipoImagen.isEmpty():
            if not e.tieneImagenes():
                return False
        return True
    def superaElMinimoDeImagenesPorClase(self,minimo):
        for e in self.listaDeCarpetasClases:
            if e.getCantidadDeImagenes()<minimo:
                return False
        return True


def getDatosDeDataset(urlCarpeta)->DatosDeCarpetaDataset:
    dc=DatosDeCarpetaDataset(str(urlCarpeta))
    def accion(f:File,profundidad:int):
        if profundidad==1:#solo carpetas
            if f.isFile():
                #print("fue file")
                return False
            dClase=DatosDeClaseDeClasificacionDeImagenesDeDataset()
            dClase.nombre=f.getName()
            dc.listaDeCarpetasClases.append(dClase)

        elif profundidad==2:#solo imagenes
            if f.isDir() or not UtilesImg.esImagen(f):
                #print("no fue imagen")
                return False

            dc.listaDeCarpetasClases[-1].addTipoDeImagen(tipo=UtilesImg.getTipoDeImagen(f)
                                                         ,espacioEnDiscoEnMB=f.getLenghtMB())
        else:
            #print("demasiada profundida")
            return False
        return True
    terminoConExitoElRecorrido=Archivo.recorrerCarpetaYUtilizarSubCarpetas_BolContinuar(urlCarpeta,utilizar=accion)
    if terminoConExitoElRecorrido:
        return dc
    return None

class ConfiguracionDeEntrenamiento:
    def __init__(self):
        self.cantidadDeEpocas=80
        self.direccionDelDataset=None
        self.direccionDeSalidaDelModelo=None
        self.cantidadDeClases=0
        self.usarPorcentajeParaValidacion=True
        self.porcentajeParaValidacion=0.2
        self.direccionDelDatasetParaValidacion=None#si not usarPorcentajeParaValidacion se usa este
        self.detenerSiLlegaAMaximoDePrecision=True
        self.maximoDePrecision=0.92
        self.guardarMejorEntrenamiento=True

        self.batch_size=32

        # self.fechaDeInicio=None
        # self.fechaDeFin=None


        self.nombreDelModelo = ""
        #self.tipoDeFruto=""
        self.descripcion=""



        # self.usarNombresDeClasesPersonalizados=True
        # self.listaDeNombresDeClases=[]

class DatosDeProgresoDeEntrenamiento:
    def __init__(self):
        self.listaDePerdidas=[]
        self.listaDePrecisiones=[]
        #self.totalDeEpocas =0
        self.cnf:ConfiguracionDeEntrenamiento=ConfiguracionDeEntrenamiento()


        self.listaDePerdidasLote = []
        self.listaDePrecisionesLote = []
        self.totalDeLotes=0

        self.estaEnFasePasosDeTerminacion=False
        self.pasoDeFinal=0

class ArgumentosDeAlTerminarUnaEpoca:
    def __init__(self):
        self.perdida=None
        self.presicion=None
        self.epoca=None
        self.eventoDeEntrenamiento=None

class ArgumentosDeAlTerminarUnLote:
    def __init__(self):
        self.perdida = None
        self.presicion = None
        self.lote = None
        self.cantidadDeLotes=None

        self.epoca=None
        self.dm_DatoEnHistorialDeEntrenamiento=None
class DatosParaCalcularCantidadDeLotes:
    def __init__(self):#,cnf:ConfiguracionDeEntrenamiento=None
        #self.cantidaDeClases=None
        self.cantidadDeImagenes=None
        self.batch_size=None
        self.porsentageParaValidacion=None

class EventosDeEntrenamiento(tf.keras.callbacks.Callback):
    def __init__(self,alComenzarElEntrenamiento
                 ,alTerminarUnaEpoca
                 ,alTerminarUnLote
                 ,condicionDeDetencion
                 , alTerminarYAntesDeOptenerLosDatos
                 ,alAvanzarEnEntrenamientoTerminado
                 ,alTerminarYGuardarLosDatosDelEntrenamiento
                 ,alDetenerElEntrenamiento
                 ):
        self.epocaActual = -1

        self.condicionDeDetencion = condicionDeDetencion
        self.detenerSiHayUnMaximoDePrecision = True
        self.maximoDePrecision = 0.4
        self.alTerminarUnaEpoca=alTerminarUnaEpoca#(ArgumentosDeAlTerminarUnaEpoca)->{}
        self.alTerminarUnLote = alTerminarUnLote  # (ArgumentosDeAlTerminarUnLote)->{}

        self.alTerminarYAntesDeOptenerLosDatos=alTerminarYAntesDeOptenerLosDatos
        self.alTerminarYGuardarLosDatosDelEntrenamiento=alTerminarYGuardarLosDatosDelEntrenamiento
        self.alComenzarElEntrenamiento=alComenzarElEntrenamiento

        self.alAvanzarEnEntrenamientoTerminado=alAvanzarEnEntrenamientoTerminado

        self.alDetenerElEntrenamiento=alDetenerElEntrenamiento


        self.datosParaCalcularCantidadDeLotes:DatosParaCalcularCantidadDeLotes=DatosParaCalcularCantidadDeLotes()
        self.lista_DM_DatoEnHistorialDeEntrenamiento: List[DM_DatoEnHistorialDeEntrenamiento] = []

        self.seDetuvoPorOrden=False


    def mandarAdetener(self):
        self.model.stop_training = True
        
    def detenerPorOrden(self):
        self.mandarAdetener()
        self.seDetuvoPorOrden = True

    def on_train_batch_end(self, batch, logs=None):
        #ejm batch= 2  #->  lote
        #log= {'loss': 51.03837203979492, 'accuracy': 0.2890625}
        # print("batch=",batch)
        # print("ty batch=", type(batch))
        # print("batch=", logs)
        # print("ty batch=", type(logs))
        if self.condicionDeDetencion():
            self.detenerPorOrden()

        arg=ArgumentosDeAlTerminarUnLote()

        arg.epoca = (self.epocaActual+1)

        arg.lote=batch
        arg.perdida=logs['loss']
        arg.presicion=logs['accuracy']
        arg.cantidadDeLotes=calcularTotalDeBachs(cantidadDeImagenes=self.datosParaCalcularCantidadDeLotes.cantidadDeImagenes
                                                 ,batch_size=self.datosParaCalcularCantidadDeLotes.batch_size
                                                 ,porsentageParaValidacion=self.datosParaCalcularCantidadDeLotes.porsentageParaValidacion)
        dh = DM_DatoEnHistorialDeEntrenamiento()
        dh.lote = arg.lote
        dh.perdida = arg.perdida
        dh.precision = arg.presicion
        dh.epoca = arg.epoca
        dh.total_de_lotes_de_epoca = arg.cantidadDeLotes
        arg.dm_DatoEnHistorialDeEntrenamiento=dh
        self.lista_DM_DatoEnHistorialDeEntrenamiento.append(dh)

        if self.alTerminarUnLote is not None:
            self.alTerminarUnLote(arg)

        # if self.epocaActual is None:
        #     print("fue null!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1")


    def on_epoch_end(self, epoch, logs):
        # print("epoca=", epoch)
        # print("logs=", logs)
        # print("tipo de logs=", type(logs))
        # if (logs.get('acc') > ACCURACY_THRESHOLD):
        #     print("\nReached %2.2f%% accuracy, so stopping training!!" % (ACCURACY_THRESHOLD * 100))
        # print("self.condicionDeDetencion=", self.condicionDeDetencion())
        self.epocaActual = epoch
        #print("termino una epoca &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        # if self.epocaActual is None:
        #     print("0 fue null##################################################2")


        if self.alTerminarUnaEpoca is not None:
            args=ArgumentosDeAlTerminarUnaEpoca()
            args.epoca=epoch
            args.perdida=logs['val_loss']
            args.presicion=logs['val_accuracy']
            args.eventoDeEntrenamiento=self
            self.alTerminarUnaEpoca(args)
        if self.condicionDeDetencion():
            self.detenerPorOrden()
        elif self.detenerSiHayUnMaximoDePrecision and logs['val_accuracy'] >= self.maximoDePrecision:
            print("se cumplio lo del maximo de detencion !!!!!!!!!!!!!!!")
            print("logs['val_accuracy']=",logs['val_accuracy'])
            print('self.maximoDePrecision',self.maximoDePrecision)
            print("logs['val_accuracy'] >= self.maximoDePrecision ",(logs['val_accuracy'] >= self.maximoDePrecision))
            self.mandarAdetener()
        # elif epoch==2:
        #     self.mandarAdetener()




        # print("no dio error")
def calcularTotalDeBachs(cantidadDeImagenes,batch_size,porsentageParaValidacion=None):
    if porsentageParaValidacion is not None:
        imagenesParaValidar=cantidadDeImagenes*porsentageParaValidacion
        tieneDecimales=(imagenesParaValidar-int(imagenesParaValidar))>0
        if tieneDecimales:
            imagenesParaValidar+=1
        cantidadDeImagenes-=imagenesParaValidar
    return int(cantidadDeImagenes/batch_size)
# def entrenar(datosDeCarpetaDatasetEntrenamiento:DatosDeCarpetaDataset
#
#              ,cnf:ConfiguracionDeEntrenamiento
#              ,eventosDeEntrenamiento:EventosDeEntrenamiento
#              ,datosDeCarpetaDatasetValidacion:DatosDeCarpetaDataset=None
#              ):

def cumpleConLosRequisitosMinimosParaEntrenarCarpetaDataset(dc:DatosDeCarpetaDataset):
    # print("dc.sonSoloImagenes()=",dc.sonSoloImagenes())
    # print("dc.superaElMinimoDeImagenesPorClase(20)=",dc.superaElMinimoDeImagenesPorClase(20))
    # print("len(dc.listaDeCarpetasClases)>=2=",(len(dc.listaDeCarpetasClases)>=2))
    return dc is not None \
            and dc.sonSoloImagenes() \
            and dc.superaElMinimoDeImagenesPorClase(20) \
            and len(dc.listaDeCarpetasClases)>=2



def entrenarAutomatico(
        #urlSalidaDelModelo
#             ,urlCarpetaDeImagenesEntrenamiento
#             ,urlCarpetaDeImagenesValidacion=None
             cnf:ConfiguracionDeEntrenamiento=ConfiguracionDeEntrenamiento()
             ,eventosDeEntrenamiento:EventosDeEntrenamiento=None
             ):
    urlCarpetaDeImagenesEntrenamiento=cnf.direccionDelDataset
    urlCarpetaDeImagenesValidacion=cnf.direccionDelDatasetParaValidacion
    dcEntrenamiento=getDatosDeDataset(urlCarpetaDeImagenesEntrenamiento)
    # print("urlCarpetaDeImagenesEntrenamiento=",urlCarpetaDeImagenesEntrenamiento)
    # print("urlCarpetaDeImagenesValidacion=",urlCarpetaDeImagenesValidacion)
    # print("dcEntrenamiento is not None=", (dcEntrenamiento is not None))
    # if dcEntrenamiento is not None:
    #     print("dcEntrenamiento.sonSoloImagenes()=", dcEntrenamiento.sonSoloImagenes())
    #     print("dcEntrenamiento.superaElMinimoDeImagenesPorClase()=", dcEntrenamiento.superaElMinimoDeImagenesPorClase())
    if dcEntrenamiento is not None \
            and dcEntrenamiento.sonSoloImagenes() \
            and dcEntrenamiento.superaElMinimoDeImagenesPorClase(20):
        cantidadDeClases = dcEntrenamiento.getCantidadDeClases()
        # print("cantidadDeClases=", cantidadDeClases)
        # print("not cnf.usarPorcentajeParaValidacion=", not cnf.usarPorcentajeParaValidacion)
        # print("urlCarpetaDeImagenesValidacion is not None=", not urlCarpetaDeImagenesValidacion is not None)

        realizarElEntrenamiento = True

        if (not cnf.usarPorcentajeParaValidacion) and urlCarpetaDeImagenesValidacion is not None:
            dcValidacion = getDatosDeDataset(urlCarpetaDeImagenesValidacion)
            realizarElEntrenamiento=dcValidacion is not None\
                                    and dcValidacion.sonSoloImagenes() \
                    and dcValidacion.superaElMinimoDeImagenesPorClase(20)\
                    and dcValidacion.getCantidadDeClases()==cantidadDeClases
        if realizarElEntrenamiento:
            cnf.cantidadDeClases=cantidadDeClases

            if eventosDeEntrenamiento is not None:
                eventosDeEntrenamiento.detenerSiHayUnMaximoDePrecision = cnf.detenerSiLlegaAMaximoDePrecision
                eventosDeEntrenamiento.maximoDePrecision =cnf.maximoDePrecision#0.4 #
                eventosDeEntrenamiento.alComenzarElEntrenamiento()
                eventosDeEntrenamiento.datosParaCalcularCantidadDeLotes.batch_size = cnf.batch_size
                eventosDeEntrenamiento.datosParaCalcularCantidadDeLotes.cantidadDeImagenes=dcEntrenamiento.getCantidadDeImagenes()
                if cnf.usarPorcentajeParaValidacion:
                    eventosDeEntrenamiento.datosParaCalcularCantidadDeLotes.porsentageParaValidacion = cnf.porcentajeParaValidacion

            entrenar(
                # urlSalidaDelModelo=urlSalidaDelModelo
                #      ,cantidaDeClases=cantidadDeClases
                #      ,urlCarpetaDeImagenesEntrenamiento=urlCarpetaDeImagenesEntrenamiento
                #      ,urlCarpetaDeImagenesValidacion=urlCarpetaDeImagenesValidacion
                     cnf=cnf
                     ,eventosDeEntrenamiento=eventosDeEntrenamiento)
            return True
    return False

class DM_DatoEnHistorialDeEntrenamiento:
    def __init__(self):
        self.epoca=0
        self.lote=0
        self.precision = 0
        self.perdida = 0
        self.total_de_lotes_de_epoca= 0
class DatosDeResultadoDeEntrenamiento:
    def __init__(self):
        self.clases=[]
        self.matrizDeConfusion=[]
        self.presicion=0
        self.perdida=0
        self.matriz_DM_DatoEnHistorialDeEntrenamiento:List[List[DM_DatoEnHistorialDeEntrenamiento]]=[]
        self.metricas:List[MetricasDeClase]=[]
    def setLista_DM_DatoEnHistorialDeEntrenamiento(self,lista_DM_DatoEnHistorialDeEntrenamiento:List[DM_DatoEnHistorialDeEntrenamiento]):
        ultimaEpoca=None
        for dm_DatoEnHistorialDeEntrenamiento in lista_DM_DatoEnHistorialDeEntrenamiento:
            if ultimaEpoca is None or dm_DatoEnHistorialDeEntrenamiento.epoca != ultimaEpoca:
                ultimaEpoca=dm_DatoEnHistorialDeEntrenamiento.epoca
                self.matriz_DM_DatoEnHistorialDeEntrenamiento.append([])
            # if dm_DatoEnHistorialDeEntrenamiento.epoca != ultimaEpoca:
            #     self.matriz_DM_DatoEnHistorialDeEntrenamiento.append([])
            #self.matriz_DM_DatoEnHistorialDeEntrenamiento[len(self.matriz_DM_DatoEnHistorialDeEntrenamiento)-1].append(dm_DatoEnHistorialDeEntrenamiento)
            self.matriz_DM_DatoEnHistorialDeEntrenamiento[-1].append(dm_DatoEnHistorialDeEntrenamiento)


def crearMatrizDeConfusionBidimencionalDeUnaClase(matrizDeConfusionMulticlase,indiceDeClase):
    """
    [[Negativos Reales TN,Falsos Positivos FP],[ Falsos Negativos FN , Positivos Reales TP ]]
    :param matrizDeConfusionMulticlase:
    :param indiceDeClase:
    :return:
    """
    FP=0
    TP=0
    FN=0
    TN=0
    for f in range(len(matrizDeConfusionMulticlase)):
        fila=matrizDeConfusionMulticlase[f]
        for c in range(len(fila)):
            valor=fila[c]
            if c==indiceDeClase and f ==indiceDeClase:
                TP+=valor
            elif c==indiceDeClase and f!=indiceDeClase:
                FP+=valor
            elif f==indiceDeClase and c!=indiceDeClase:
                FN+=valor
            else:
                TN+=valor
    return [[TN,FP],[FN,TP]]

class MetricasDeClase:
    def __init__(self):
        # self.nombreDeClase=None
        # self.indiceDeClase=0

        self.precision=0
        self.especificidad=0
        self.sensibilidad=0

        self.exactitud=0
    def __str__(self):
        def ft(n):
            return "%.2f"%(n*100)
        return " precision="+ft(self.precision)+" especificidad="+ft(self.especificidad)+" sensibilidad="+ft(self.sensibilidad)+" exactitud="+ft(self.exactitud)

def getMetricasDeClase(matrizDeConfusionMulticlase)->List[MetricasDeClase]:
    metricas=[]#,listaDeNombreClases
    for i in range(len(matrizDeConfusionMulticlase)):
        matrizBinaria=crearMatrizDeConfusionBidimencionalDeUnaClase(matrizDeConfusionMulticlase,i)
        # print("--------------------------------")
        # print(i)
        # print(matrizBinaria)
        #[[TN a, FP b], [FN c, TP d]]
        TN=matrizBinaria[0][0]
        FP=matrizBinaria[0][1]
        FN = matrizBinaria[1][0]
        TP = matrizBinaria[1][1]
        metricaActual=MetricasDeClase()
        #metricaActual.indiceDeClase=i
        #metricaActual.nombreDeClase=listaDeNombreClases[metricaActual.indiceDeClase]
        #print(TP, "/(", FP, "+", TP, ")")
        if FP==0 and TP==0:
            metricaActual.precision = 0
        else:
            metricaActual.precision=TP/(FP+TP) #d/(b+d)
        #print(metricaActual.precision)

        #print(TN, "/(", FN, "+", FP, ")")
        if TN==0 and FP==0:
            metricaActual.especificidad=0
        else:
            metricaActual.especificidad = TN / (TN + FP)  # a/(a+b)
        #print(metricaActual.especificidad)

        #print(TP, "/(", TP, "+", FN, ")")
        if TP==0 and FN==0:
            metricaActual.sensibilidad =0
        else:
            metricaActual.sensibilidad = TP / (TP + FN)  # d/(d+c)
        #print(metricaActual.sensibilidad)

        #print(TP, "/(", FP, "+", TP, ")")
        if TN==0 and FP==0 and FN==0 and TP==0:
            metricaActual.exactitud =0
        else:
            metricaActual.exactitud = (TN+FP) / (TN + FP+FN+TP)  # (a+d)/(a+b+c+d)
        #print(metricaActual.exactitud)

        t=metricaActual.exactitud
        metricaActual.exactitud=metricaActual.precision
        metricaActual.precision=t

        metricas.append(metricaActual)
    return metricas

def getClasesDeDatasetEn(urlCompleta):
    batch_size = 32
    img_height = 32
    img_width = 32
    train_ds_original = tf.keras.utils.image_dataset_from_directory(
        str(urlCompleta),

        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size
    )
    return train_ds_original.class_names


def entrenar(
            # urlSalidaDelModelo
            # ,cantidaDeClases
            # ,urlCarpetaDeImagenesEntrenamiento
            # ,urlCarpetaDeImagenesValidacion=None
             cnf:ConfiguracionDeEntrenamiento=ConfiguracionDeEntrenamiento()
             ,eventosDeEntrenamiento:EventosDeEntrenamiento=None
             )->DatosDeResultadoDeEntrenamiento:#(urlCarpetaDeImagenes, urlSalidaDelModelo,cantidadDeEpocas,eventosDeEntrenamiento):
    cnf.direccionDeSalidaDelModelo=str(cnf.direccionDeSalidaDelModelo)
    print("t1 ----------------------------")
    def avanzarEnEntrenamientoTerminado():
        if eventosDeEntrenamiento is not None:
            eventosDeEntrenamiento.alAvanzarEnEntrenamientoTerminado()

    num_classes = cnf.cantidadDeClases
    #print("num_classes=",num_classes)
    batch_size = 32
    img_height = 32
    img_width = 32


        #.datosParaCalcularCantidadDeLotes:DatosParaCalcularCantidadDeLotes=DatosParaCalcularCantidadDeLotes()

    # labels="inferred"
    # if cnf.usarNombresDeClasesPersonalizados:
    #     labels=cnf.listaDeNombresDeClases
    #print("cnf.usarPorcentajeParaValidacion=",cnf.usarPorcentajeParaValidacion)
    if cnf.usarPorcentajeParaValidacion:
        data_dir = pathlib.Path(cnf.direccionDelDataset)

        # print("data_dir=",data_dir)
        # print("cnf.porcentajeParaValidacion=",cnf.porcentajeParaValidacion)

        train_ds_original = tf.keras.utils.image_dataset_from_directory(
            data_dir,
            validation_split=cnf.porcentajeParaValidacion,
            subset="training",
            seed=123,
            image_size=(img_height, img_width),
            batch_size=batch_size
        )
        print("t2 ----------------------------")
        val_ds = tf.keras.utils.image_dataset_from_directory(
            data_dir,
            validation_split=cnf.porcentajeParaValidacion,
            subset="validation",
            seed=123,
            image_size=(img_height, img_width),
            batch_size=batch_size)
    else:
        data_dir_entrenamiento = pathlib.Path(cnf.direccionDelDataset)
        data_dir_validacion = pathlib.Path(cnf.direccionDelDatasetParaValidacion)
        train_ds_original = tf.keras.utils.image_dataset_from_directory(
            data_dir_entrenamiento,

            seed=123,
            image_size=(img_height, img_width),
            batch_size=batch_size
        )
        print("t2 ----------------------------")
        val_ds = tf.keras.utils.image_dataset_from_directory(
            data_dir_validacion,

            seed=123,
            image_size=(img_height, img_width),
            batch_size=batch_size)
    print("t3 ----------------------------")

    AUTOTUNE = tf.data.AUTOTUNE
    print("!!!!!!!!!!!!!!!!!! AUTOTUNE=",AUTOTUNE)

    train_ds = train_ds_original.cache().prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    print("t4 ----------------------------")

    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(16, 3, padding='same'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.ReLU(),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(32, 3, padding='same'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.ReLU(),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(64, 3, padding='same'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.ReLU(),
        tf.keras.layers.MaxPooling2D(),

        tf.keras.layers.Flatten(),#input_shape=(img_height,img_width) lo pasa de un [][] a uno [] con c=f*c

        tf.keras.layers.Dense(4500),
        tf.keras.layers.Dense(1000),
        tf.keras.layers.Dense(num_classes)
    ])

    print("t5 ----------------------------")

    model.compile(
        optimizer='adam',
        loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy'])
    print("Paso el compile !!!!!!!!!!!!!!!!!!!!!!!!!!____________")
    print("t6 ----------------------------")
    # def eventoAlTerminarUnaEpoca(epoch, logs):
    #     print("epoca=", epoch)
    #     print("logs=", logs)
    #     print("tipo de logs=", type(logs))
    #     # epoca = 0
    #     # logs = {'loss': 28.492460250854492, 'accuracy': 0.5435267686843872, 'val_loss': 88.94847106933594,
    #     #         'val_accuracy': 0.2455357164144516}
    #     # tipo de logs = <class 'dict'>
    #
    # cm_callback = tf.keras.callbacks.LambdaCallback(on_epoch_end=eventoAlTerminarUnaEpoca)


    if eventosDeEntrenamiento is not None:
        cm_callback =eventosDeEntrenamiento
        callbacks=[cm_callback]#checkpoint,
    else:
        callbacks=[]

    if cnf.guardarMejorEntrenamiento:
        checkpoint = keras.callbacks.ModelCheckpoint(cnf.direccionDeSalidaDelModelo, save_best_only=True)
        callbacks.insert(0,checkpoint)

    model.fit(
        train_ds,
        #batch_size=30,
        validation_data=val_ds,
        callbacks=callbacks,
        epochs=cnf.cantidadDeEpocas

    )

    if eventosDeEntrenamiento is not None and eventosDeEntrenamiento.seDetuvoPorOrden:
        eventosDeEntrenamiento.alDetenerElEntrenamiento()
        return None

    if eventosDeEntrenamiento is not None:
        eventosDeEntrenamiento.alTerminarYAntesDeOptenerLosDatos()
    avanzarEnEntrenamientoTerminado()#1
    print("Termino de el fit !!!!!!!!!!!!!!!!!!!!!!!!!!____________")
    if not cnf.guardarMejorEntrenamiento:
        model.save(cnf.direccionDeSalidaDelModelo)
    else:
        model = load_model(cnf.direccionDeSalidaDelModelo)
    print("creo el modelo fisico !!!!!!!!!!!!!!!!!!!!!!!!!!")
    avanzarEnEntrenamientoTerminado()#2
    #print("cnf.direccionDeSalidaDelModelo=", cnf.direccionDeSalidaDelModelo)


    y_pred = model.predict(val_ds)
    print("p1 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    avanzarEnEntrenamientoTerminado()#3
    predicted_categories = tf.argmax(y_pred, axis=1)
    print("p2 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    avanzarEnEntrenamientoTerminado()#4
    true_categories = tf.concat([y for x, y in val_ds], axis=0)
    print("p3 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    avanzarEnEntrenamientoTerminado()#5
    matrizDeConfusion=confusion_matrix(predicted_categories, true_categories)
    print("p4 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    avanzarEnEntrenamientoTerminado()#6

    test_loss, test_acc=model.evaluate(val_ds)
    print("p5 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    avanzarEnEntrenamientoTerminado()#7

    dr=DatosDeResultadoDeEntrenamiento()
    dr.clases=train_ds_original.class_names
    dr.matrizDeConfusion=matrizDeConfusion
    dr.presicion=test_acc
    dr.perdida=test_loss
    dr.metricas = getMetricasDeClase(dr.matrizDeConfusion,)

    #print("eventosDeEntrenamiento is not None =",(eventosDeEntrenamiento is not None))
    if eventosDeEntrenamiento is not None:
        #dr.lista_DM_DatoEnHistorialDeEntrenamiento=eventosDeEntrenamiento.lista_DM_DatoEnHistorialDeEntrenamiento
        dr.setLista_DM_DatoEnHistorialDeEntrenamiento(eventosDeEntrenamiento.lista_DM_DatoEnHistorialDeEntrenamiento)

        eventosDeEntrenamiento.alTerminarYGuardarLosDatosDelEntrenamiento(dr)
        avanzarEnEntrenamientoTerminado()#8
        print("llamo alterminar !!!!!!!!!!!!!!!!!!!!!!!!!!____________")

    return dr




