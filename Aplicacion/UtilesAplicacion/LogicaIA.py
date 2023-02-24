from Aplicacion.ReneIAClasificador.comprobador_v1_0 import obtenerPrediccion
from Aplicacion.ReneIAClasificador.entrenador_v2_0 import entrenarAutomatico,ArgumentosDeAlTerminarUnaEpoca,EventosDeEntrenamiento,DatosDeProgresoDeEntrenamiento,ConfiguracionDeEntrenamiento,DatosDeResultadoDeEntrenamiento,ArgumentosDeAlTerminarUnLote
from Aplicacion.ReneIAClasificador.AlgoritmosDeProcesamientoDeImagenes import *
from Aplicacion.UtilesAplicacion.UtilesApp import *
from Aplicacion.UtilesAplicacion.ClasesLogica import *
from Aplicacion.UtilesAplicacion.LogicaBD import *
from datetime import datetime
from typing import TYPE_CHECKING, Dict, List, NoReturn, Optional, Union, Tuple, cast, ClassVar


class ConfiguracionDeEntrenamiento_BD(ConfiguracionDeEntrenamiento):
    def __init__(self):
        ConfiguracionDeEntrenamiento.__init__(self)
        self.idDelDataset = None
        self.idDelDatasetParaValidacion = None  # si not usarPorcentajeParaValidacion se usa este


class IA:

    def realizarPasoGrayWord(self,request,nombreImg,formato,strDate):

        r = RespuestaClasificacionYProcesamiento()
        r.datosDeImagenOriginal = APP_CNF.getDatosDeImagenTempDj_DeNombre(nombreImg)

        urlEntrada = r.datosDeImagenOriginal.url_relativa_completa

        r.datosDeImagenGrayWorld = APP_CNF.getDatosDeImagenTempDj(request,
                                                                  strDate + NOMBRE_IMG_ALGORITMO_GRAY_WORD + formato)

        urlSalida = r.datosDeImagenGrayWorld.url_relativa_completa

        print("0--------------------------------------------")
        grayWorld(urlEntrada, urlSalida)
        print("1--------------------------------------------")



        return r

    def realizarPasoBoundingBox(self,request,r:RespuestaClasificacionYProcesamiento,formato,strDate):


        r.datosDeImagenBoundingBox = APP_CNF.getDatosDeImagenTempDj(request,
                                                                    strDate + NOMBRE_IMG_ALGORITMO_BOUNDING_BOX + formato)
        urlEntrada = r.datosDeImagenGrayWorld.url_relativa_completa

        urlSalida = r.datosDeImagenBoundingBox.url_relativa_completa

        boundingBox(urlEntrada, urlSalida)
        print("2--------------------------------------------")
        return r


    def realizarPasoMResize(self, request, r: RespuestaClasificacionYProcesamiento, formato,strDate):

        r.datosDeImagenMResize = APP_CNF.getDatosDeImagenTempDj(request,
                                                                strDate + NOMBRE_IMG_ALGORITMO_M_RESIZE + formato)
        urlEntrada = r.datosDeImagenBoundingBox.url_relativa_completa

        urlSalida = r.datosDeImagenMResize.url_relativa_completa

        mresize(urlEntrada, urlSalida)
        print("3--------------------------------------------")

        return r

    def realizarPasoCielAB(self, request, r: RespuestaClasificacionYProcesamiento, formato, strDate):
        r.datosDeImagenCielAB = APP_CNF.getDatosDeImagenTempDj(request,
                                                               strDate + NOMBRE_IMG_ALGORITMO_CIEL_AB + formato)

        urlEntrada = r.datosDeImagenMResize.url_relativa_completa

        urlSalida = r.datosDeImagenCielAB.url_relativa_completa

        cielAB(urlEntrada, urlSalida)
        print("4--------------------------------------------")
        return r

    def realizarPasoPrediccion(self, request,nombreModeloNeuronal:str, r: RespuestaClasificacionYProcesamiento, formato, strDate):
        urlSalida = r.datosDeImagenCielAB.url_relativa_completa
        modelo: ModeloNeuronal = bd.getModelo(nombreModeloNeuronal)

        #r.clases = get_nombresDeClasesOrganizados_De_ModeloNeuronal(modelo)
        r.clases = bd.getClaseDeClasificacion_All_ModeloNeuronal(modelo)
        listaDeNombresDeClases= [cla.Nombre for cla in r.clases]
        r.clases=get_nombresDeClasesOrganizados_De_listaDeClasesClasificacion(r.clases)
        # if contiene(nombreModeloNeuronal.lower(), "bomba"):
        #     r.clases = ["Verde Hecho", "Verde", "Rayona", "Madura"]
        # else:
        #     r.clases = ["Verde", "Verde-pintona", "Madura", "Sobre-maduración"]
        #print("#######################################################")
        #print(getDireccionCompletaModelo(modelo))
        r.clasificacion = obtenerPrediccion(
            urlDelModelo=str(getDireccionCompletaModelo(modelo))#modelo.Direccion#urlDelModelo=getDireccionCompletaModelo(modelo)#modelo.Direccion
            , urlImagenProcesada=urlSalida
            , listaDeNombresDeClases=listaDeNombresDeClases)

        r.crearClasesDeRespuesta()

        imgOriginal = APP_CNF.getDireccionRelativa_DeCampoImagen(r.datosDeImagenOriginal.url_relativa_completa)
        imgGrayWorld = APP_CNF.getDireccionRelativa_DeCampoImagen(r.datosDeImagenGrayWorld.url_relativa_completa)
        imgBoundingBox = APP_CNF.getDireccionRelativa_DeCampoImagen(r.datosDeImagenBoundingBox.url_relativa_completa)
        imgMresize = APP_CNF.getDireccionRelativa_DeCampoImagen(r.datosDeImagenMResize.url_relativa_completa)
        imgCielAB = APP_CNF.getDireccionRelativa_DeCampoImagen(r.datosDeImagenCielAB.url_relativa_completa)
        pro = bd.saveProcesamientoImagen(imgOriginal)#, request.user
        bd.saveImagenProcesada(imgGrayWorld, pro, "default", NOMBRE_ALGORITMO_GRAY_WORD)
        bd.saveImagenProcesada(imgBoundingBox, pro, "default", NOMBRE_ALGORITMO_BOUNDING_BOX)
        bd.saveImagenProcesada(imgMresize, pro, "default", NOMBRE_ALGORITMO_M_RESIZE)
        imgpCielAb = bd.saveImagenProcesada(imgCielAB, pro, "default", NOMBRE_ALGORITMO_CIEL_AB)

        user:User=request.user
        if user.is_anonymous or not user.is_authenticated:
            username=APP_CNF.consts.NOMBRE_USUARIO_ANONIMO
        else:
            username=user.username

        client_ip=get_ip_usuario(request)

        cla = bd.saveClasificacion(procesamiento=pro
                                   , imagen=imgpCielAb
                                   , resultado=r.clasificacion
                                   , username=username
                                   ,ip=client_ip
                                   , modelo=modelo)
        r.idClasificacion = cla.id
        r.idProcesamientoDeImagen = pro.id
        return r

    def comenzarEntrenamiento(self,request,eventosDeEntrenamiento,cnf:ConfiguracionDeEntrenamiento_BD):

        cnf.direccionDeSalidaDelModelo=str(getDireccionNuevaModelo(request,cnf.nombreDelModelo))
        cnf.direccionDelDataset=str(getDireccionCompletaDataset(cnf.idDelDataset))
        if not cnf.usarPorcentajeParaValidacion:
            cnf.direccionDelDatasetParaValidacion=str(getDireccionCompletaDataset(cnf.idDelDatasetParaValidacion))
        return entrenarAutomatico(cnf,eventosDeEntrenamiento)




ia=IA()
class DatosEnMemoriaDeEntrenamiento:
    def __init__(self):
        self.fase_entrenamiento_en_curso=False
        self.fase_entrenamiento_terminado = False
        self.fase_entrenamiento_comenzando = False
        self.fase_pasos_de_terminacion=False

        self.detener_entrenamiento=False
        self.lista_perdida=[]
        self.lista_presicion=[]

        self.llamo_a_detener_entrenamiento=False
        self.fechaDeInicio = None
        self.fechaDeFin = None

        self.datosResultadoDelEntrenamiento:DatosDeResultadoDeEntrenamiento=DatosDeResultadoDeEntrenamiento()

        self.lista_perdida_lote = []
        self.lista_presicion_lote = []
        self.lote_actual=0
        self.cantidad_de_lotes = 0

        self.pasoDeFinal = 0

        self.nombreDelModelo=None
        #self.lista_DM_DatoEnHistorialDeEntrenamiento:List[DM_DatoEnHistorialDeEntrenamiento]=[]

class LogicaParaEntrenamiento:
    def __init__(self, app_config: AppDjImpl):
        self.app = app_config
        self.dm = app_config.datos_en_memoria

        self.__listaDeNombresDeModeloEnProceso = []
    def getDatosEnMemoriaDeEntrenamiento(self,request)->DatosEnMemoriaDeEntrenamiento:
        return self.dm.get(request, KEY_DATOS_EN_MEMORIA_DE_ENTRENAMIENTO, DatosEnMemoriaDeEntrenamiento())

    def __getDME(self, request):
        return self.getDatosEnMemoriaDeEntrenamiento(request)

    def getListaDeNombresDeModeloEnProceso(self):
        return self.__listaDeNombresDeModeloEnProceso
    def addNombreDeModeloEnProceso(self,nombre):
        if not nombre in self.__listaDeNombresDeModeloEnProceso:
            self.__listaDeNombresDeModeloEnProceso.append(nombre)
    def removeNombreDeModeloEnProceso(self,nombre):
        self.__listaDeNombresDeModeloEnProceso.remove(nombre)



    def yaHayUnEntrenamientoEnCurso(self, request):
        #return self.dm.get(request, KEY_fase_entrenamiento_en_curso, False)
        return  self.getDatosEnMemoriaDeEntrenamiento(request).fase_entrenamiento_en_curso
    def estaEnFaseEntrenamientoTerminado(self,request):
        #return self.dm.get(request, KEY_fase_entrenamiento_terminado, False)
        return self.getDatosEnMemoriaDeEntrenamiento(request).fase_entrenamiento_terminado
    def estaEnFaseEntrenamientoComenzando(self,request):
        return self.getDatosEnMemoriaDeEntrenamiento(request).fase_entrenamiento_comenzando
    def estaEnFasePasosDeTerminacion(self,request):
        return self.getDatosEnMemoriaDeEntrenamiento(request).fase_pasos_de_terminacion
    def pasarAFaseEntrenamientoComenzando(self,request):
        dme = self.getDatosEnMemoriaDeEntrenamiento(request)
        dme.fase_entrenamiento_comenzando = True
        # print("pas =",dme)
        # print("1 pas =", self.getDatosEnMemoriaDeEntrenamiento(request).fase_entrenamiento_comenzando)
    def llamoADetenerEntrenamiento(self,request):
        return self.getDatosEnMemoriaDeEntrenamiento(request).llamo_a_detener_entrenamiento

    def __resetearDatosDeAvanzeDelFinal(self,request):
        dme = self.getDatosEnMemoriaDeEntrenamiento(request)
        dme.pasoDeFinal=0
        dme.fase_entrenamiento_terminado = False
        dme.fase_pasos_de_terminacion=False


    def __restearDatosDeLote(self,request):
        dme = self.getDatosEnMemoriaDeEntrenamiento(request)
        dme.lista_perdida_lote = []
        dme.lista_presicion_lote = []
        dme.lote_actual = 0
        dme.cantidad_de_lotes = 0

    def __alTomarAccionUnaVesTerminadoUnEntrenamiento(self,request):
        dme = self.getDatosEnMemoriaDeEntrenamiento(request)

        dme.llamo_a_detener_entrenamiento = False
        dme.lista_perdida = []
        dme.lista_presicion = []
        dme.detener_entrenamiento = False
        dme.fase_entrenamiento_comenzando = False




        self.__restearDatosDeLote(request)
        self.__resetearDatosDeAvanzeDelFinal(request)
        self.removeNombreDeModeloEnProceso(dme.nombreDelModelo)


    def llamoACancelarEntrenamientoTerminado(self,request):
        self.__alTomarAccionUnaVesTerminadoUnEntrenamiento(request)

    def llamoAGuardarModelo(self,request):
        cnf=self.getConf(request)
        dme= self.getDatosEnMemoriaDeEntrenamiento(request)
        dts=bd.getDataset_id(cnf.idDelDataset)
        dr = self.getDatosResultadoDelEntrenamiento(request)
        listaDePerdidas=dme.lista_perdida
        listaPresicion=dme.lista_presicion
        print("listaPresicion=",listaPresicion)
        print("listaDePerdidas=", listaDePerdidas)
        # for dh in dme.lista_DM_DatoEnHistorialDeEntrenamiento:
        #     print("epoca=",dh.epoca," lote=",dh.lote," precision=",dh.precision," perdida=",dh.perdida," total_de_lotes_de_epoca=",dh.total_de_lotes_de_epoca)
        perdida=listaDePerdidas[-1]
        for i,pre in enumerate(listaPresicion):
            if pre==dr.presicion:
                perdida=listaDePerdidas[i]

        m=bd.saveModeloNeuronal(direccion=getDireccionNuevaRelativaModelo(request,cnf.nombreDelModelo)
                              ,nombre=cnf.nombreDelModelo
                              #,fruto=cnf.tipoDeFruto
                              ,user=getUserRequest(request)
                              #,dataset=bd.getDataset_id(cnf.idDelDataset)
                              ,fechaDeCreacion=dme.fechaDeFin
                              ,descripcion=cnf.descripcion
                              ,precision=dr.presicion#listaPresicion[-1]
                              ,perdida=perdida
                              ,cantidadDeEpocas=len(listaPresicion))
        print("guardo la entidad modelo")
        # print("dr.matriz_DM_DatoEnHistorialDeEntrenamiento=",dr.matriz_DM_DatoEnHistorialDeEntrenamiento)
        ent=bd.saveEntrenamiento(total_De_Epocas=len(dr.matriz_DM_DatoEnHistorialDeEntrenamiento)
                             ,modeloNeuronal=m
                             ,dataset=dts)
        print("guardo la entidad entrenamiento")
        print("guardando datos del entrenamiento....")
        for i,lL in enumerate(dr.matriz_DM_DatoEnHistorialDeEntrenamiento):
            # print("i=",i)
            if not i<len(listaPresicion):
                break
            lotes=dr.matriz_DM_DatoEnHistorialDeEntrenamiento[i]
            epoca=bd.saveEpoca(numero_De_Epoca=i+1
                               ,total_De_Lotes=len(lotes)
                               ,precision=listaPresicion[i]
                               ,perdida=listaDePerdidas[i]
                               ,entrenamiento=ent
                               )
            for j,lote in enumerate(lotes):
                bd.saveDatoEnHistorialDeEntrenamiento(
                    epoca=epoca
                    ,lote=lote.lote
                    ,precision=lote.precision
                    ,perdida=lote.perdida
                )
        porcentaje_Utilizado_Del_Dataset=100
        if cnf.usarPorcentajeParaValidacion:
            porcentaje_Utilizado_Del_Dataset=cnf.porcentajeParaValidacion*100
        else:
            dts = bd.getDataset_id(cnf.idDelDatasetParaValidacion)

        print("guardo las entidades datos de entrenamiento")

        vali=bd.saveValidacion(
            precision=dr.presicion
            ,porcentaje_Utilizado_Del_Dataset=porcentaje_Utilizado_Del_Dataset
            ,modeloNeuronal=m
            ,dataset=dts
        )
        print("guardo la entidad validacion")
        print("guardando datos de  matriz de confusion...")
        for f,fila in enumerate(dr.matrizDeConfusion):
            for c,cantidad in enumerate(fila):
                bd.saveDatoEnMatrizDeConfusion(
                    clasificacion_predicha=dr.clases[c]
                    , clasificacion_real=dr.clases[f]
                    , indice_columna=c
                    , indice_fila=f
                    , cantidad=cantidad
                    ,validacion=vali
                )
        print("guardo la entidad entrenamiento")

        self.__alTomarAccionUnaVesTerminadoUnEntrenamiento(request)
        print("realizó todos los procedimientos con exito")


    def setConf(self,request,cnf:ConfiguracionDeEntrenamiento):
        self.dm.put(request, KEY_CONFIGURACION, cnf)
    def getConf(self,request)->ConfiguracionDeEntrenamiento_BD:
        return self.dm.get(request,KEY_CONFIGURACION,ConfiguracionDeEntrenamiento_BD())
    def getDatosResultadoDelEntrenamiento(self,request):
        return self.getDatosEnMemoriaDeEntrenamiento(request).datosResultadoDelEntrenamiento
    def comenzarEntrenamiento(self,request,cnf:ConfiguracionDeEntrenamiento_BD):



        def alComenzarElEntrenamiento():
            #self.__restearMemoriaEntrenamiento(request)
            #self.dm.put(request, KEY_fase_entrenamiento_terminado, False)
            dme = self.getDatosEnMemoriaDeEntrenamiento(request)
            dme.fase_entrenamiento_en_curso = True
            dme.detener_entrenamiento = False
            #dme.fase_entrenamiento_terminado=False
            dme.llamo_a_detener_entrenamiento=False
            dme.lista_perdida = []
            dme.lista_presicion = []
            dme.fechaDeInicio=datetime.now()

            dme.lista_DM_DatoEnHistorialDeEntrenamiento=[]

            self.__resetearDatosDeAvanzeDelFinal(request)
            self.pasarAFaseEntrenamientoComenzando(request)
            self.setConf(request,cnf)

            self.__restearDatosDeLote(request)
        def condicionDeDetencion():
            #return self.dm.get(request, KEY_DETENER_ENTRENAMIENTO)
            return self.getDatosEnMemoriaDeEntrenamiento(request).detener_entrenamiento

        def alTerminarUnaEpoca(args: ArgumentosDeAlTerminarUnaEpoca):
            dme=self.getDatosEnMemoriaDeEntrenamiento(request)
            dme.lista_perdida.append(args.perdida)
            dme.lista_presicion.append(args.presicion)
            dme.fase_entrenamiento_comenzando = False

            self.__restearDatosDeLote(request)

            # listaPerdida: List = self.dm.get(request, KEY_LISTA_PERDIDA)
            # listaPrecision: List = self.dm.get(request, KEY_LISTA_PRECISION)

            # listaPerdida.append(args.perdida)
            # listaPrecision.append(args.presicion)

            # self.dm.put(request, KEY_LISTA_PERDIDA, listaPerdida)
            # self.dm.put(request, KEY_LISTA_PRECISION, listaPrecision)
        def alTerminarUnLote(args:ArgumentosDeAlTerminarUnLote):
            dme = self.getDatosEnMemoriaDeEntrenamiento(request)
            dme.lista_perdida_lote.append(args.perdida)
            dme.lista_presicion_lote.append(args.presicion)
            dme.lote_actual=args.lote
            dme.cantidad_de_lotes = args.cantidadDeLotes



            #dme.lista_DM_DatoEnHistorialDeEntrenamiento.append(args.dm_DatoEnHistorialDeEntrenamiento)
            if dme.fase_entrenamiento_comenzando:
                dme.fase_entrenamiento_comenzando = False
                print("t7 fin ------------------------------------")
        def alTerminarYAntesDeOptenerLosDatos():
            dme = self.getDatosEnMemoriaDeEntrenamiento(request)
            dme.fase_pasos_de_terminacion = True
            dme.fase_entrenamiento_comenzando = False
            dme.pasoDeFinal = 0
            self.__restearDatosDeLote(request)
        def alAvanzarEnEntrenamientoTerminado():
            dme = self.getDatosEnMemoriaDeEntrenamiento(request)
            dme.pasoDeFinal += 1

        def alTerminarElEntrenamiento(dr:DatosDeResultadoDeEntrenamiento):
            #self.dm.put(request, KEY_fase_entrenamiento_terminado, True)
            dme = self.getDatosEnMemoriaDeEntrenamiento(request)

            #self.__restearMemoriaEntrenamiento(request)

            # dme.detener_entrenamiento = False
            dme.fechaDeFin = datetime.now()

            # print("0 matris de confusion++++++++++++++")
            # for f in dr.matrizDeConfusion:
            #     print(f)

            organizarClasesEnDatosResultadoDeEntrenamiento(dr=dr, idDataset=cnf.idDelDataset)

            # print("1 matris de confusion+++++++++++++++")
            # for f in dr.matrizDeConfusion:
            #     print(f)

            dme.datosResultadoDelEntrenamiento=dr


            self.__restearDatosDeLote(request)
            dme.fase_entrenamiento_comenzando = False
            dme.fase_pasos_de_terminacion = False
            dme.fase_entrenamiento_en_curso = False
            dme.fase_entrenamiento_terminado = True

            #print("self.yaHayUnEntrenamientoEnCurso(request)=",self.yaHayUnEntrenamientoEnCurso(request))

        def alDetenerElEntrenamiento():
            self.__alTomarAccionUnaVesTerminadoUnEntrenamiento(request)

        dme = self.getDatosEnMemoriaDeEntrenamiento(request)
        dme.nombreDelModelo=cnf.nombreDelModelo
        self.addNombreDeModeloEnProceso(dme.nombreDelModelo)

        if not ia.comenzarEntrenamiento(request,EventosDeEntrenamiento(alComenzarElEntrenamiento=alComenzarElEntrenamiento
            ,alTerminarUnLote=alTerminarUnLote
                                                        ,alTerminarUnaEpoca=alTerminarUnaEpoca
                                                        , condicionDeDetencion=condicionDeDetencion
            ,alTerminarYAntesDeOptenerLosDatos=alTerminarYAntesDeOptenerLosDatos
            ,alAvanzarEnEntrenamientoTerminado=alAvanzarEnEntrenamientoTerminado
                                                        ,alTerminarYGuardarLosDatosDelEntrenamiento=alTerminarElEntrenamiento
            ,alDetenerElEntrenamiento=alDetenerElEntrenamiento
                                                        ),cnf=cnf):
            self.removeNombreDeModeloEnProceso(dme.nombreDelModelo)
            dme.fase_entrenamiento_comenzando = False
    def detenerEntrenamiento(self,request):
        #self.dm.put(request, KEY_DETENER_ENTRENAMIENTO, True)
        dme=self.getDatosEnMemoriaDeEntrenamiento(request)
        dme.fase_entrenamiento_en_curso = False
        dme.fase_entrenamiento_comenzando=False
        dme.fase_entrenamiento_terminado=False



        dme.detener_entrenamiento=True
        dme.llamo_a_detener_entrenamiento=True



    def getDatosDeProgresoDeEntrenamiento(self,request):
        dme = self.getDatosEnMemoriaDeEntrenamiento(request)
        # listaPerdida: List = self.dm.get(request, KEY_LISTA_PERDIDA)
        # listaPrecision: List = self.dm.get(request, KEY_LISTA_PRECISION)
        dp=DatosDeProgresoDeEntrenamiento()
        # dp.listaDePerdidas=listaPerdida
        # dp.listaDePrecisiones=listaPrecision
        dp.listaDePerdidas = dme.lista_perdida
        dp.listaDePrecisiones = dme.lista_presicion
        dp.cnf.cantidadDeEpocas=self.getConf(request).cantidadDeEpocas#self.dm.get(request,KEY_CANTIDAD_DE_EPOCAS)

        dp.listaDePrecisionesLote=dme.lista_presicion_lote
        dp.listaDePerdidasLote=dme.lista_perdida_lote
        dp.totalDeLotes=dme.cantidad_de_lotes

        dp.estaEnFasePasosDeTerminacion=self.estaEnFasePasosDeTerminacion(request)
        dp.pasoDeFinal=dme.pasoDeFinal
        return dp

logicaDeEntrenamiento = LogicaParaEntrenamiento(app_config=APP_CNF)

# def getClasificacion(self,request,nombreModeloNeuronal:str,nombreImg):#idModeloNeuronal   nombreModeloNeuronal:str
#     strDate=getStrDateEnImgNow()
#     formato=getFormato(nombreImg)
#
#     modelo: ModeloNeuronal =bd.getModelo(nombreModeloNeuronal)#bd.getModeloNeuronal_id(idModeloNeuronal) #
#
#     r = RespuestaClasificacionYProcesamiento()
#
#     r.clases=get_nombresDeClasesOrganizados_De_ModeloNeuronal(modelo)
#
#
#     r.datosDeImagenOriginal = APP_CNF.getDatosDeImagenTempDj_DeNombre(nombreImg)
#
#     urlEntrada = r.datosDeImagenOriginal.url_relativa_completa
#
#     r.datosDeImagenGrayWorld = APP_CNF.getDatosDeImagenTempDj(request, strDate+NOMBRE_IMG_ALGORITMO_GRAY_WORD+formato)
#
#     urlSalida = r.datosDeImagenGrayWorld.url_relativa_completa
#
#     print("0--------------------------------------------")
#     grayWorld(urlEntrada, urlSalida)
#     print("1--------------------------------------------")
#     r.datosDeImagenBoundingBox = APP_CNF.getDatosDeImagenTempDj(request, strDate+NOMBRE_IMG_ALGORITMO_BOUNDING_BOX+formato)
#
#     urlEntrada = urlSalida
#
#     urlSalida = r.datosDeImagenBoundingBox.url_relativa_completa
#
#     boundingBox(urlEntrada, urlSalida)
#     print("2--------------------------------------------")
#     r.datosDeImagenMResize = APP_CNF.getDatosDeImagenTempDj(request, strDate+NOMBRE_IMG_ALGORITMO_M_RESIZE+formato)
#
#     urlEntrada = urlSalida
#
#     urlSalida = r.datosDeImagenMResize.url_relativa_completa
#
#     mresize(urlEntrada, urlSalida)
#     print("3--------------------------------------------")
#     r.datosDeImagenCielAB = APP_CNF.getDatosDeImagenTempDj(request, strDate+NOMBRE_IMG_ALGORITMO_CIEL_AB+formato)
#
#     urlEntrada = urlSalida
#
#     urlSalida = r.datosDeImagenCielAB.url_relativa_completa
#
#     cielAB(urlEntrada, urlSalida)
#     print("4--------------------------------------------")
#
#     r.clasificacion = obtenerPrediccion(
#         urlDelModelo=getDireccionCompletaModelo(modelo)#modelo.Direccion
#         , urlImagenProcesada=urlSalida
#         , listaDeNombresDeClases=r.clases)
#     r.crearClasesDeRespuesta()
#
#     imgOriginal = APP_CNF.getDireccionRelativa_DeCampoImagen(r.datosDeImagenOriginal.url_relativa_completa)
#     imgGrayWorld = APP_CNF.getDireccionRelativa_DeCampoImagen(r.datosDeImagenGrayWorld.url_relativa_completa)
#     imgBoundingBox = APP_CNF.getDireccionRelativa_DeCampoImagen(r.datosDeImagenBoundingBox.url_relativa_completa)
#     imgMresize = APP_CNF.getDireccionRelativa_DeCampoImagen(r.datosDeImagenMResize.url_relativa_completa)
#     imgCielAB = APP_CNF.getDireccionRelativa_DeCampoImagen(r.datosDeImagenCielAB.url_relativa_completa)
#     pro = bd.saveProcesamientoImagen(imgOriginal, request.user)
#     bd.saveImagenProcesada(imgGrayWorld, pro, "default", NOMBRE_ALGORITMO_GRAY_WORD)
#     bd.saveImagenProcesada(imgBoundingBox, pro, "default", NOMBRE_ALGORITMO_BOUNDING_BOX)
#     bd.saveImagenProcesada(imgMresize, pro, "default", NOMBRE_ALGORITMO_M_RESIZE)
#     imgpCielAb=bd.saveImagenProcesada(imgCielAB, pro, "default", NOMBRE_ALGORITMO_CIEL_AB)
#     cla=bd.saveClasificacion(procesamiento=pro
#                         ,imagen=imgpCielAb
#                         ,resultado=r.clasificacion
#                         ,user= request.user
#                         ,modelo= modelo)
#     r.idClasificacion = cla.id
#     r.idProcesamientoDeImagen = pro.id
#     return r
#