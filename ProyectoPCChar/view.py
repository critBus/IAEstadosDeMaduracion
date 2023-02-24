from builtins import staticmethod

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from django.contrib.auth.decorators import login_required, user_passes_test

from django.template import RequestContext

from django.contrib import auth
from django.contrib import admin

from ProyectoPCChar.forms import FormularioDePrueba

from Aplicacion.UtilesAplicacion.UtilesApp import *
from Aplicacion.UtilesAplicacion.LogicaBD import *

from Aplicacion.UtilesAplicacion.ClasesLogica import *
from Aplicacion.UtilesAplicacion.ClasesFormularios import *


def seguridadMinima(user:User):
    return  (not user.is_anonymous) and user.is_authenticated and user.is_active and (bd.esInvestigador(user) or bd.esAdmin(user))

def seguridadAdmin(user:User):
    return (not user.is_anonymous) and user.is_authenticated and user.is_active  and (bd.esAdmin(user) or user.is_staff or user.is_superuser)


from Aplicacion.UtilesAplicacion.LogicaIA import *

#
# def metodoClasificarPost(request):
#     nombre_modelo = getSes(request, KEY_NOMBRE_MODELO)
#     nombre_img = getSes(request, KEY_NOMBRE_IMAGEN)
#     resultado = ia.getClasificacion(request=request
#                                     , nombreModeloNeuronal=nombre_modelo
#                                     , nombreImg=nombre_img)
#     putSes(request, KEY_ID_CLASIFICACION, resultado.idClasificacion)
#     putSes(request, KEY_ID_PROCESAMIENTO_DE_IMAGEN, resultado.idProcesamientoDeImagen)
#     listaClasesDeClases = []
#     for cla in resultado.clases:
#         dicCla = {'nombre': cla.nombre
#             , 'seleccionada': cla.seleccionada}
#         listaClasesDeClases.append(dicCla)
#     dic = {'clases': listaClasesDeClases
#         , 'clasificacion': resultado.clasificacion
#            }
#     putSes(request, KEY_RESULTADO, dic)
#
#     return JsonResponse({
#         'content': {
#             'resultado': dic,
#
#         }
#     })
#
def vistaError_MultivalueKeyPost(request):
    lcp = LocalizacionDePagina("Advertencia", "Error en url")

    return renderAppActual(request, 'Visual/ErrorUrlGet.html',
                           {}
                           , lcp)

from django.utils.datastructures import MultiValueDictKeyError
from builtins import KeyError
def seguridadError(vista):
    def zz(*args,**keywords):
        try:
            return vista(*args,**keywords)
        except MultiValueDictKeyError:
            verException()
            return vistaError_MultivalueKeyPost(args[0])
        except KeyError:
            verException()
            return vistaError_MultivalueKeyPost(args[0])
        except:

            verException()
            lcp = LocalizacionDePagina("Advertencia", "Error en url")

            return renderAppActual(args[0], 'Visual/ErrorGeneral.html',
                                   {}
                                   , lcp)

    return zz

def vistaErrorUrl(request):
    lcp = LocalizacionDePagina("Advertencia", "Error en url")

    return renderAppActual(request, 'Visual/Error404.html',
                           {}
                           , lcp)


#@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
@seguridadError
def vistaClasificar(request):
    #nombre_formulario_clasificar_imagen = 'formulario1'



    mostrarResultado = False
    resultado = None

    lanzarMetodoPostClasificar = False

    #listaParNombreFrutoYId=

    if APP_CNF.isPost(request, APP_CNF.forms.CLASIFICAR_IMAGEN):
        # indice_fruto = getPostInt(request, NOMBRE_SELECT_FRUTO)
        # indice_modelo = getPostInt(request, NOMBRE_SELECT_MODELO)

        idModelo = getPostInt(request,APP_CNF.inputs.SELECT_FRUTO )
        #indice_modelo = getPostInt(request, APP_CNF.inputs.SELECT_MODELO)

        #nombre_modelo = bd.getFrutoYModelos_All()[indice_fruto].listaDeModelos[indice_modelo]

        modelo=bd.getModeloNeuronal_id(idModelo)

        nombre_imagen = APP_CNF.crearImgTempDj(request, 'imagen',
                                               getStrDateEnImgNow() + NOMBRE_IMG_TEMP_ORIGINAL + getExtencionPostFile(
                                                   request, 'imagen')).nombre

        putSes(request, KEY_NOMBRE_IMAGEN, nombre_imagen)
        putSes(request, KEY_NOMBRE_MODELO, modelo.Nombre)
        lanzarMetodoPostClasificar = True


    #elif APP_CNF.isPost(request, NOMBRE_TERMINO_DE_CLASIFICAR):
    elif APP_CNF.isPost(request, APP_CNF.forms.TERMINO_DE_CLASIFICAR):
        resultado = getSes(request, KEY_RESULTADO)#'resultado')
        mostrarResultado = True

    formulario = FormularioDePrueba()
    return renderAppActual(request, 'Visual/Principal.html', {'form': formulario
        , 'lanzarMetodoPostClasificar': lanzarMetodoPostClasificar
        # , 'select_fruto': NOMBRE_SELECT_FRUTO
        # , 'select_modelo': NOMBRE_SELECT_MODELO
        # , 'nombre_formulario_detalles_resultado': NOMBRE_FORM_DETALLES_AL_CLASIFICAR
        # , 'nombre_formulario_clasificar_imagen': nombre_formulario_clasificar_imagen
        , 'mostrarResultado': mostrarResultado
        , 'resultado': resultado
        , 'listaDeFrutosYModelos': bd.getListaParNombresFrutosYIdModeloNeuronal()
      ,'datosModelos':bd.getDatosDeModelos_ParaCalsificar()
        # , 'nombre_formulario_termino_de_clasificar': NOMBRE_TERMINO_DE_CLASIFICAR

                                                              }
                           , LocalizacionDePagina(LP_APLICACION,"Clasificar Imagen "))


#@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
@seguridadError
def vistaDetalles(request):
    class DatosDetalles:
        def __init__(self):
            self.mostrarConjuntoDeImgs = False
            self.direccionImgOriginal = ""
            self.direccionImgGrayWorld = ""
            self.direccionImgBoundingBox = ""
            self.direccionImgMresize = ""
            self.direccionImgCielAB = ""
            self.resultado = ""

    dd = DatosDetalles()

    def actualizarDetalles(dd, idClasificacion, idProcesamientoDeImagen=None):
        dd.mostrarConjuntoDeImgs = True
        d = getDatosDeClasificacionDetalles(request=request
                                            , idClasificacion=idClasificacion
                                            , idProcesamientoDeImagen=idProcesamientoDeImagen)

        dd.direccionImgOriginal = d.datosDeImagenOriginal  # .url_relativa_carpeta_static
        dd.direccionImgGrayWorld = d.datosDeImagenGrayWorld  # .url_relativa_carpeta_static
        dd.direccionImgBoundingBox = d.datosDeImagenBoundingBox  # .url_relativa_carpeta_static
        dd.direccionImgMresize = d.datosDeImagenMResize  # .url_relativa_carpeta_static
        dd.direccionImgCielAB = d.datosDeImagenCielAB  # .url_relativa_carpeta_static
        dd.resultado = d.clasificacion

    #if APP_CNF.isPost(request, NOMBRE_FORM_DETALLES_AL_CLASIFICAR):
    if APP_CNF.isPost(request, APP_CNF.forms.DETALLES_AL_CLASIFICAR):

        idClasificacion = getSes(request, KEY_ID_CLASIFICACION)
        idProcesamientoDeImagen = getSes(request, KEY_ID_CLASIFICACION)

        actualizarDetalles(dd, idClasificacion, idProcesamientoDeImagen)

    #elif APP_CNF.isPost(request, NOMBRE_FORM_DETALLES_LISTA_DE_CLASIFICACIONES_USUARIO):
    elif APP_CNF.isPost(request, APP_CNF.forms.DETALLES_LISTA_DE_CLASIFICACIONES_USUARIO):
        #idClasificacion = getPostInt(request, NOMBRE_ID_CLASIFICACION)
        idClasificacion = getPostInt(request, APP_CNF.inputs.ID_CLASIFICACION)
        actualizarDetalles(dd, idClasificacion)

    return renderAppActual(request, 'Visual/Detalles.html', {
        'mostrarConjuntoDeImgs': dd.mostrarConjuntoDeImgs
        , 'direccionImgOriginal': dd.direccionImgOriginal
        , 'direccionImgGrayWorld': dd.direccionImgGrayWorld
        , 'direccionImgBoundingBox': dd.direccionImgBoundingBox
        , 'direccionImgMresize': dd.direccionImgMresize
        , 'direccionImgCielAB': dd.direccionImgCielAB
        , 'resultado': dd.resultado
    }, LocalizacionDePagina(LP_APLICACION,"Detalles Clasificación De Imagen "))


#@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
@seguridadError
def vistaClasificaciones(request):
    d = DatosDeBusqueda()
    mostrarMensajeSeBorroCorrectamenteLaClasificacion = False

    def aplicarFiltroDeSerNecesario(ldcl):
        try:
            aplicarFiltro = getSesBool(request, KEY_APLICAR_FILTRO)
            # print('aplicarFiltro0=', aplicarFiltro)
        except:
            putSes(request, KEY_APLICAR_FILTRO, False)
            aplicarFiltro = False
            # print('aplicarFiltro que tiene que ser false ', aplicarFiltro)
        # print('aplicarFiltro=',aplicarFiltro)
        if aplicarFiltro:
            tipoDeFiltro = getSes(request, KEY_RADIO_FILTRO)
            valorAComparar = getSes(request, KEY_TEXT_FILTRO)
            if len(valorAComparar) > 0:
                ldcl = getDatosDeClasificacion_All_user(request, "ClasificacionesActuales"
                                                        , tipoDeFiltro=tipoDeFiltro
                                                        , valorAComparar=valorAComparar)
                d.seBuscoSobre(valorAComparar)

        return ldcl

    p = PaginacionDeSession(app_config=APP_CNF
                            , cantidadMaximaAMostrar=20
                            , crearListaCompleta=lambda r: aplicarFiltroDeSerNecesario(
            getDatosDeClasificacion_All_user(request, "ClasificacionesActuales"))
                            )

    #if APP_CNF.isPost(request, NOMBRE_FORM_DELETE_CLASIFICAION_LISTA_DE_CLASIFICACIONES_USUARIO):
    if APP_CNF.isPost(request, APP_CNF.forms.DELETE_CLASIFICAION_LISTA_DE_CLASIFICACIONES_USUARIO):

        #idClasificacion = getPostInt(request, NOMBRE_ID_CLASIFICACION)
        idClasificacion = getPostInt(request,APP_CNF.inputs.ID_CLASIFICACION)
        bd.deleteClasificacion_YProcesamiento_idClasificacion_(idClasificacion)
        mostrarMensajeSeBorroCorrectamenteLaClasificacion = True
        p.realizarPagincacionDeSerNecesario(request)
    elif APP_CNF.isPost(request, APP_CNF.forms.FILTRO):
        tipoDeFiltro = getPost(request, APP_CNF.inputs.RADIO_FILTRO)
        valorAComparar = getPost(request, APP_CNF.inputs.TEXT_FILTRO)

        if len(valorAComparar) > 0:
            putSes(request, KEY_APLICAR_FILTRO, True)
            putSes(request, KEY_RADIO_FILTRO, tipoDeFiltro)
            putSes(request, KEY_TEXT_FILTRO, valorAComparar)
        else:
            putSes(request, KEY_APLICAR_FILTRO, False)
            putSes(request, KEY_TEXT_FILTRO, "")

        p.getListaConPaginacionDefault(request)

    elif p.isPostPaginacion(request):
        pass


    else:
        putSes(request, KEY_APLICAR_FILTRO, False)
        p.getListaConPaginacionDefault(request)



    return renderAppActual(request, 'Visual/Clasificaciones.html', {

        'datosDePaginacion': p.getDatosPaginacion(request)

        # , 'filtro_fruto': VALOR_RADIO_FRUTO
        # , 'filtro_modelo': VALOR_RADIO_MODELO
        # , 'filtro_clasificacion': VALOR_RADIO_CLASIFICACION
        # , 'filtro_fecha': VALOR_RADIO_FECHA
        # , 'filtro_todo': VALOR_RADIO_TODO
        #
        # , 'nombre_radio_filtro': NOMBRE_RADIO_FILTRO
        # , 'nombre_text_filtro': NOMBRE_TEXT_FILTRO
        , 'listaDatosClasificacion': p.getListaPaginada(request)
        # , 'idClasificacionActual': NOMBRE_ID_CLASIFICACION
        # , 'formularioDetalles': NOMBRE_FORM_DETALLES_LISTA_DE_CLASIFICACIONES_USUARIO
        #
        # , 'nombre_formulario_filtro': NOMBRE_FORM_FILTRO
        # , 'nombre_formulario_delete': NOMBRE_FORM_DELETE_CLASIFICAION_LISTA_DE_CLASIFICACIONES_USUARIO
        , 'mostrarMensajeSeBorroCorrectamenteLaClasificacion': mostrarMensajeSeBorroCorrectamenteLaClasificacion
        , 'datosDeBusqueda': d
    }, LocalizacionDePagina(LP_APLICACION, "Clasificaciones Realizadas "))



@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
@seguridadError
def vistaEntrenamiento(request):
    try:
        pass
    except:
        print("algo dio error")

    # print("va a mostrar el reques")
    # print(request)

    form=Formulario_ConfiguracionDeEntrenamiento()

    # print("paso el formulario !!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    lcp = LocalizacionDePagina(LP_INVESTIGACION, "Entrenamiento")
    yaHayUnEntrenamientoEnCurso = logicaDeEntrenamiento.yaHayUnEntrenamientoEnCurso(request)

    fueComenzarEntrenamiento = APP_CNF.isPost(request,form)#APP_CNF.forms.COMENZAR_ENTRENAMIENTO

    if fueComenzarEntrenamiento:
        form.comprobarValidacion(request)
        form.verValoresDeCampos()


    datosDeProgreso = logicaDeEntrenamiento.getDatosDeProgresoDeEntrenamiento(request)

    if yaHayUnEntrenamientoEnCurso or (fueComenzarEntrenamiento and form.valido) \
            or logicaDeEntrenamiento.estaEnFaseEntrenamientoComenzando(request):

        if fueComenzarEntrenamiento:

            cnf = ConfiguracionDeEntrenamiento_BD()
            cnf.cantidadDeEpocas =form.cantidadDeEpocas.valor #getPostInt(request,APP_CNF.inputs.CANTIDAD_DE_EPOCAS)
            # print("0 cantidadDeEpocas=", cnf.cantidadDeEpocas)
            cnf.idDelDataset =form.idDataset.valor #getPostInt(request,APP_CNF.inputs.ID_DATASET)  # bd.getDataset_id(getPostInt(request,NOMBRE_INPUT_ID_DATASET))
            cnf.direccionDelDataset =bd.getDataset_id(cnf.idDelDataset).Direccion_Imagenes_Procesadas #.Direccion
            cnf.usarPorcentajeParaValidacion =form.usarPorcentajeParaValidacion.valor #getPost(request,APP_CNF.inputs.TIPO_DE_VALIDACION) == APP_CNF.radios.PORCENTAJE_DE_VALIDACION
            if cnf.usarPorcentajeParaValidacion:
                cnf.porcentajeParaValidacion =form.porsentajeParaValidacion.valor #getPostFloat(request, APP_CNF.inputs.PORCENTAJE_DE_VALIDACION)
            else:
                cnf.idDelDatasetParaValidacion =form.idDatasetParaValidacion.valor #getPostInt(request, APP_CNF.inputs.ID_DATASET_PARA_VALIDACION)
                cnf.direccionDelDatasetParaValidacion = bd.getDataset_id(cnf.idDelDataset).Direccion_Imagenes_Procesadas
            cnf.detenerSiLlegaAMaximoDePrecision =form.usarLimiteDePrecision.valor #getPostBool(request, APP_CNF.inputs.USAR_LIMITE_DE_PRECISION)
            if cnf.detenerSiLlegaAMaximoDePrecision:
                cnf.maximoDePrecision =form.limiteDePrecision.valor #getPostFloat(request, APP_CNF.inputs.LIMITE_DE_PRECISION)
                # print("%%%%%%%%%%%%%%%%%% cnf.maximoDePrecision=",cnf.maximoDePrecision)

            cnf.nombreDelModelo = form.nombre.valor#getPost(request, APP_CNF.inputs.NOMBRE_DEL_MODELO)
            #cnf.tipoDeFruto = form.tipoDeFruto.valor#getPost(request, APP_CNF.inputs.TIPO_DE_FRUTO)
            cnf.descripcion =form.descripcion.valor #getPost(request, APP_CNF.inputs.DESCRIPCION)
            cnf.guardarMejorEntrenamiento=form.guardarMaximaPrecision.valor

            logicaDeEntrenamiento.setConf(request, cnf)
            datosDeProgreso = logicaDeEntrenamiento.getDatosDeProgresoDeEntrenamiento(request)
            logicaDeEntrenamiento.pasarAFaseEntrenamientoComenzando(request)

            # estaEnComenzando = logicaDeEntrenamiento.estaEnFaseEntrenamientoComenzando(request)
            # print("0 estaEnComenzando=", estaEnComenzando)

        # cantidadDeEpocas = datosDeProgreso.conf.cantidadDeEpocas
        # print("cantidadDeEpocas=",cantidadDeEpocas)
        return renderAppActual(request, 'Visual/ProgresoDeEntrenamiento.html', {
            # 'nombre_detener_entrenamiento': NOMBRE_FORM_DETENER_ENTRENAMIENTO
            # , 'nombre_termino_el_entrenamiento': NOMBRE_FORM_TERMINO_EL_ENTRENAMIENTO
             'fueComenzarEntrenamiento': fueComenzarEntrenamiento

            , 'datosDeProgresoDeEntrenamiento': datosDeProgreso

        }, lcp)

    elif logicaDeEntrenamiento.estaEnFaseEntrenamientoTerminado(
            request) and not logicaDeEntrenamiento.llamoADetenerEntrenamiento(request):
        cnf = logicaDeEntrenamiento.getConf(request)
        if APP_CNF.isPost(request, APP_CNF.forms.CANCELAR_MODELO):
            eliminarArchivoDelModelo(cnf)
            logicaDeEntrenamiento.llamoACancelarEntrenamientoTerminado(request)
        elif APP_CNF.isPost(request, APP_CNF.forms.GUARDAR_MODELO):
            print("va a guardar las entidades en la bd")
            logicaDeEntrenamiento.llamoAGuardarModelo(request)
            print("se guardo el modelo !!!!!!!!!!!!!!!!!")
        else:
            dr=logicaDeEntrenamiento.getDatosResultadoDelEntrenamiento(request)
            for metrica in dr.metricas:
                print("exactitud=",metrica.exactitud)
                print("metrica=",metrica.sensibilidad)

            print("matris de confusion-------------------")
            for f in dr.matrizDeConfusion:
                print(f)
            # print("pre=",datosDeProgreso.listaDePrecisiones)
            # print("per=", datosDeProgreso.listaDePerdidas)

            return renderAppActual(request, 'Visual/ResultadosDelEntrenamiento.html', {
                'cnf': cnf
                , 'datosResultadoDelEntrenamiento': dr

                # , "nombre_formulario_guardar_modelo": NOMBRE_FORM_GUARDAR_MODELO
                # , 'nombre_formulario_cancelar_modelo': NOMBRE_FORM_CANCELAR_MODELO
                , 'datosDeProgresoDeEntrenamiento': datosDeProgreso
                ,'datosDataset':DatosDataset(bd.getDataset_id(cnf.idDelDataset),bd)

            }, lcp)

    #else:
        # if APP_CNF.isPost(request, NOMBRE_FORM_DETENER_ENTRENAMIENTO):
        #     logicaDeEntrenamiento.detenerEntrenamiento(request)
    cnf:ConfiguracionDeEntrenamiento=logicaDeEntrenamiento.getConf(request)
    #print("cnf.maximoDePrecision=",cnf.maximoDePrecision)
    return renderAppActual(request, 'Visual/ComienzoDeEntrenamiento.html', {
           #  'nombre_comenzar_entrenamiento':NOMBRE_FORM_COMENZAR_ENTRENAMIENTO
           #  ,'nombre_detener_entrenamiento':NOMBRE_FORM_DETENER_ENTRENAMIENTO
           #
           #  ,'nombre_input_nombre_del_modelo':NOMBRE_INPUT_NOMBRE_DEL_MODELO
           #  ,'nombre_input_id_dataset':NOMBRE_INPUT_ID_DATASET
           #  ,'nombre_input_id_dataset_para_validacion':NOMBRE_INPUT_ID_DATASET_PARA_VALIDACION
           #  ,'nombre_input_tipo_de_fruto':NOMBRE_INPUT_TIPO_DE_FRUTO
           #  ,'nombre_input_descripcion':NOMBRE_INPUT_DESCRIPCION
           # , 'nombre_input_cantidad_de_epocas':NOMBRE_INPUT_CANTIDAD_DE_EPOCAS
           #  , 'nombre_input_tipo_de_validacion':NOMBRE_INPUT_TIPO_DE_VALIDACION
           #  , 'nombre_input_porcentaje_de_validacion':NOMBRE_INPUT_PORCENTAJE_DE_VALIDACION
           #  , 'nombre_input_usar_limite_de_precision':NOMBRE_INPUT_USAR_LIMITE_DE_PRECISION
           #  , 'nombre_input_limite_de_precision':NOMBRE_INPUT_LIMITE_DE_PRECISION
           #  , 'valor_radio_porcentaje_de_validacion':VALOR_RADIO_PORCENTAJE_DE_VALIDACION
           #  ,'valor_radio_dataset_para_validacion':VALOR_RADIO_DATASET_PARA_VALIDACION

            'listaDatosDeDataset':DatosDataset.getDatosDataset(bd)
            ,'cnf':cnf
        , 'form': form
        }, lcp)







@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
def metodoLlamarAComenzarEntrenamiento(request):
    #yaHayUnEntrenamientoEnCurso=dm.get(KEY_ENTRENAMIENTO_EN_CURSO,False)
    yaHayUnEntrenamientoEnCurso=logicaDeEntrenamiento.yaHayUnEntrenamientoEnCurso(request)
    if not yaHayUnEntrenamientoEnCurso and not logicaDeEntrenamiento.estaEnFaseEntrenamientoTerminado(request):
        cnf=logicaDeEntrenamiento.getConf(request)

        logicaDeEntrenamiento.comenzarEntrenamiento(request,cnf)

    return JsonResponse({
        'content': {
            'yaHayUnEntrenamientoEnCurso': yaHayUnEntrenamientoEnCurso
            , 'dioError': False

        }
    })

@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
def metodoLlamarADetenerEntrenamiento(request):
    #dm.put(request, KEY_DETENER_ENTRENAMIENTO, True)
    print("se va a llamar a detener entrenamiento")
    cnf = logicaDeEntrenamiento.getConf(request)

    logicaDeEntrenamiento.detenerEntrenamiento(request)

    eliminarArchivoDelModelo(cnf)
    print("se  llamo a detener entrenamiento")
    return JsonResponse({
        'content': {
            'resultado': {}
            , 'dioError': False

        }
    })

@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
def metodoGetEstadoDeEntrenamiento(request):
    #hayUnEntrenamientoEnCurso=dm.get(request,KEY_ENTRENAMIENTO_EN_CURSO,False)
    hayUnEntrenamientoEnCurso =logicaDeEntrenamiento.yaHayUnEntrenamientoEnCurso(request)
    #print("00000000000000000 hayUnEntrenamientoEnCurso=",hayUnEntrenamientoEnCurso)
    #estaEnFaseEntrenamientoTerminado=logicaDeEntrenamiento.estaEnFaseEntrenamientoTerminado(request)
    datosDeProgreso=DatosDeProgresoDeEntrenamiento()
    # listaPerdida=[]
    # listaPrecision=[]
    if hayUnEntrenamientoEnCurso:
        datosDeProgreso=logicaDeEntrenamiento.getDatosDeProgresoDeEntrenamiento(request)

        # listaPerdida: List = dm.get(request, KEY_LISTA_PERDIDA)
        # listaPrecision: List = dm.get(request, KEY_LISTA_PRECISION)
        # print("\nlistaPerdida=",listaPerdida)
        # print("listaPrecision=", listaPrecision)
    estaEnComenzando=logicaDeEntrenamiento.estaEnFaseEntrenamientoComenzando(request)
    estaEnFasePasosTerminado=datosDeProgreso.estaEnFasePasosDeTerminacion
    pasosDelFinal=datosDeProgreso.pasoDeFinal
    # if estaEnFasePasosTerminado:
    #     print("datosDeProgreso.pasoDeFinal=",pasosDelFinal)
    #     print("ty datosDeProgreso.pasoDeFinal=", type(pasosDelFinal))
    #print("estaEnFasePasosTerminado=", estaEnFasePasosTerminado)
    # print("estaEnComenzando=",estaEnComenzando)
    return JsonResponse({
        'content': {
            'listaPerdida': datosDeProgreso.listaDePerdidas
            ,'listaPrecision':datosDeProgreso.listaDePrecisiones
            , 'cantidadDeEpocas': datosDeProgreso.cnf.cantidadDeEpocas
            ,'hayUnEntrenamientoEnCurso':hayUnEntrenamientoEnCurso
            ,'estaEnFaseEntrenamientoTerminado':logicaDeEntrenamiento.estaEnFaseEntrenamientoTerminado(request)
            ,'llamoADetenerElEntrenamiento':logicaDeEntrenamiento.llamoADetenerEntrenamiento(request)
            ,'estaEnFaseEntrenamientoComenzando':estaEnComenzando
            , 'dioError': False

            ,'listaPerdidaLote': datosDeProgreso.listaDePerdidasLote
            ,'listaPrecisionLote':datosDeProgreso.listaDePrecisionesLote
            ,'totalDeLotes':datosDeProgreso.totalDeLotes

            ,'estaEnFasePasosDeTerminacion':estaEnFasePasosTerminado
            ,'pasoDeFinal':pasosDelFinal

        }
    })


def metodoPasoGrayWordPost(request):
    nombre_img = getSes(request, KEY_NOMBRE_IMAGEN)
    strDate = getStrDateEnImgNow()
    formato = getFormato(nombre_img)

    dioError=False
    dic={}
    try:
        resultado = ia.realizarPasoGrayWord(request=request
                                            ,nombreImg=nombre_img
                                            ,formato=formato
                                            ,strDate=strDate)
        dic = {
            KEY_STR_DATE: strDate
            , KEY_FORMATO: formato
            , KEY_IMG_ORIGINAL: resultado.datosDeImagenOriginal.crearDic()
            , KEY_IMG_GRAY_WORD: resultado.datosDeImagenGrayWorld.crearDic()

        }
    except:
        dioError = True


    putSes(request, KEY_DATOS_RESPUESTA, dic)

    return JsonResponse({
        'content': {
            'resultado': dic
            ,'dioError':dioError

        }
    })

def metodoPasoBoundingBoxPost(request):
    dioError = False
    dic = getSes(request,KEY_DATOS_RESPUESTA)
    # print("dic=",dic)
    # print("dic t=", type(dic))
    r = RespuestaClasificacionYProcesamiento()
    r.datosDeImagenGrayWorld=DatosDeImagenTempDj.getDeDic(dic[KEY_IMG_GRAY_WORD])

    try:
        resultado = ia.realizarPasoBoundingBox(request=request
                                               ,r=r
                                               ,formato=dic[KEY_FORMATO]
                                               ,strDate=dic[KEY_STR_DATE])
        dic = appenDic(dic,{
            KEY_IMG_BOUNDING_BOX: resultado.datosDeImagenBoundingBox.crearDic()
           })
    # print("2dic=",dic)
    except:
        dioError = True

    putSes(request, KEY_DATOS_RESPUESTA, dic)

    return JsonResponse({
        'content': {
            'resultado': dic
            , 'dioError': dioError

        }
    })

def metodoPasoMResizePost(request):
    dioError = False
    dic = getSes(request, KEY_DATOS_RESPUESTA)
    # print("3dic=", dic)
    r = RespuestaClasificacionYProcesamiento()
    r.datosDeImagenBoundingBox = DatosDeImagenTempDj.getDeDic(dic[KEY_IMG_BOUNDING_BOX])

    try:
        resultado = ia.realizarPasoMResize(request=request
                                               , r=r
                                               , formato=dic[KEY_FORMATO]
                                               , strDate=dic[KEY_STR_DATE])
        dic = appenDic(dic, {
            KEY_IMG_M_RESIZE: resultado.datosDeImagenMResize.crearDic()
        })
    except:
        dioError = True

    putSes(request, KEY_DATOS_RESPUESTA, dic)

    return JsonResponse({
        'content': {
            'resultado': dic
            , 'dioError': dioError

        }
    })

def metodoPasoCielABPost(request):
    dioError = False
    dic = getSes(request, KEY_DATOS_RESPUESTA)
    r = RespuestaClasificacionYProcesamiento()
    r.datosDeImagenMResize = DatosDeImagenTempDj.getDeDic(dic[KEY_IMG_M_RESIZE])

    try:
        resultado = ia.realizarPasoCielAB(request=request
                                               , r=r
                                          , formato=dic[KEY_FORMATO]
                                          , strDate=dic[KEY_STR_DATE])
        dic = appenDic(dic, {
            KEY_IMG_CIEL_AB: resultado.datosDeImagenCielAB.crearDic()
        })
    except:
        print('eroror uno')
        dioError = True

    putSes(request, KEY_DATOS_RESPUESTA, dic)

    return JsonResponse({
        'content': {
            'resultado': dic
            , 'dioError': dioError

        }
    })

def metodoPasoPrediccionPost(request):
    nombre_modelo = getSes(request, KEY_NOMBRE_MODELO)
    dioError = False
    dic = getSes(request, KEY_DATOS_RESPUESTA)
    r = RespuestaClasificacionYProcesamiento()
    r.datosDeImagenOriginal = DatosDeImagenTempDj.getDeDic(dic[KEY_IMG_ORIGINAL])
    r.datosDeImagenGrayWorld = DatosDeImagenTempDj.getDeDic(dic[KEY_IMG_GRAY_WORD])
    r.datosDeImagenBoundingBox = DatosDeImagenTempDj.getDeDic(dic[KEY_IMG_BOUNDING_BOX])
    r.datosDeImagenMResize = DatosDeImagenTempDj.getDeDic(dic[KEY_IMG_M_RESIZE])
    r.datosDeImagenCielAB = DatosDeImagenTempDj.getDeDic(dic[KEY_IMG_CIEL_AB])



    resultado = ia.realizarPasoPrediccion(request=request
                                          , nombreModeloNeuronal=nombre_modelo
                                          , r=r
                                          , formato=dic[KEY_FORMATO]
                                          , strDate=dic[KEY_STR_DATE]
                                          )

    putSes(request, KEY_ID_CLASIFICACION, resultado.idClasificacion)
    putSes(request, KEY_ID_PROCESAMIENTO_DE_IMAGEN, resultado.idProcesamientoDeImagen)
    listaClasesDeClases = []
    for cla in resultado.clases:
        dicCla = {'nombre': cla.nombre
            , 'seleccionada': cla.seleccionada}
        listaClasesDeClases.append(dicCla)
    dic = {'clases': listaClasesDeClases
        , 'clasificacion': resultado.clasificacion
           }
    putSes(request, KEY_RESULTADO, dic)

    # try:
    #
    #
    #
    # except:
    #
    #     print("dio error22")
    #     dioError = True



    return JsonResponse({
        'content': {
            'resultado': dic
        , 'dioError': dioError

        }
    })


def page_not_found(request):
    return render(request,"404.html",status=404)

@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
@seguridadError
def vistaAgregarDataset(request):
    hayQueRecuperarDatos=False
    idUltimoFrutoAgregado=None
    if existeSes(request,APP_CNF.consts.KEY_ULTIMA_URL_AGREGAR_FRUTO_EXTERNO):
        hayQueRecuperarDatos=getSes(request,APP_CNF.consts.KEY_ULTIMA_URL_AGREGAR_FRUTO_EXTERNO)==APP_CNF.urls.URL_VISTA_AGREGAR_DATASET \
                             and existeSes(request, APP_CNF.consts.KEY_ID_ULTIMO_FRUTO_AGREGADO)

        if hayQueRecuperarDatos:
            idUltimoFrutoAgregado=getSes(request,APP_CNF.consts.KEY_ID_ULTIMO_FRUTO_AGREGADO)
            putSes(request,APP_CNF.consts.KEY_ULTIMA_URL_AGREGAR_FRUTO_EXTERNO,None)
            putSes(request, APP_CNF.consts.KEY_ID_ULTIMO_FRUTO_AGREGADO, None)



    form = Formulario_AgregarDataset()
    lcp = LocalizacionDePagina(LP_INVESTIGACION, "Crear Dataset")

    return renderAppActual(request, 'Visual/AgregarDataset.html', {
    'form':form
        ,'listaDatosDeFrutos': DatosDeFruto.getDatosDeFrutos(bd)
        ,"hayQueRecuperarDatos":hayQueRecuperarDatos
        ,"idUltimoFrutoAgregado":idUltimoFrutoAgregado
    }, lcp)

@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
@seguridadError
def vistaAgregarDataset_MandoARecargar(request):
    logicaUploadDataset.intentarPasarAFaseComienzo(request)
    return vistaAgregarDataset(request)

from ReneDjangoApp.Utiles.Clases.Upload.ClasesUpload import *
from Aplicacion.UtilesAplicacion.LogicaUpload import logicaUploadDataset,LogicaUploadDataset,UploadManager

@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
def metodoSuviendoArchivo(request):
    print("mando a suvir dataset")
    umng:UploadManager=logicaUploadDataset.getUploadManagerInicializado(request)
    return umng.uploadIfPost(request)

@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
def metodoDetenerDescompresionDataset(request):
    # print("llamada metodo post detener descompresion")
    logicaUploadDataset.detenerDescompresion(request)
    return JsonResponse({'data': 'terminado'})
@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
def metodoDetenerUploadDataset(request):
    #print("llamada metodo post detener")
    logicaUploadDataset.detenerUpload(request)
    return JsonResponse({'data': 'terminado'})

@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
def metodoEliminarDatasetSubido(request):
    logicaUploadDataset.eliminarDatasetSubido(request)
    return JsonResponse({'data': 'terminado'})

@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
def metodoGetEstadoVistaEntradaDataset(request):
    dmuld = logicaUploadDataset.getDatosEnMemoriaUploadDataset(request)
    estaEnFaseComienzo=dmuld.estaEnFase_COMIENZO()
    estaEnSuviendoDataset = dmuld.estaEnFase_SUVIENDO_DATASET()
    estaEnDeteniendoUploadDataset = dmuld.estaEnFase_DETENIENDO_UPLOAD_DATASET()
    estaEnDeteniendoDescompresionDataset=dmuld.estaEnFase_DETENIENDO_DESCOMPRESION_DATASET()
    estaEnErrorSuviendoDataset = dmuld.estaEnFase_ERROR_SUVIENDO_DATASET()
    estaEnFaseArchivoDatasetSuvido = dmuld.estaEnFase_ARCHIVO_DATASET_SUVIDO()


    progresoUpload=dmuld.datosDeFileDj.porcientoActual#logicaUploadDataset.getProgresoActual(request)
    nombreArchivo=dmuld.datosDeFileDj.name#logicaUploadDataset.getNombreArchivo(request)
    progresoDeDescompresion= dmuld.progresoDeDescompresion  # logicaUploadDataset.getProgresoActual(request)

    estaEnFaseDeteniendoProcesamientoDeImagenes=dmuld.estaEnFase_DETENIENDO_PROCESAMIENTO_DE_IMAGENES()
    estaEnFaseProcesandoImagenes=dmuld.estaEnFase_DATASET_PROCESANDO_IMAGENES()

    d={
            'estaEnFaseComienzo': estaEnFaseComienzo
            ,'estaEnSuviendoDataset':estaEnSuviendoDataset
            ,'estaEnDeteniendoUploadDataset':estaEnDeteniendoUploadDataset
            ,'estaEnErrorSuviendoDataset':estaEnErrorSuviendoDataset
            ,'estaEnFaseArchivoDatasetSuvido':estaEnFaseArchivoDatasetSuvido
            ,'estaEnFaseDescomprimiendoDataset':dmuld.estaEnFase_DESCOMPRIMIENDO_DATASET()
            ,'estaEnDeteniendoDescompresionDataset':estaEnDeteniendoDescompresionDataset
            ,'estaEnFaseDatasetDescomprimidoConError':dmuld.estaEnFase_DATASET_DESCOMPRIMIDO_CON_ERROR()
            ,'estaEnFaseDatasetDescomprimido':dmuld.estaEnFase_DATASET_DESCOMPRIMIDO()
            ,'progresoActualUpload':progresoUpload
            ,'nombreArchivo':nombreArchivo
            ,'listaDeCarpetasEnDatasetDescomprimido':dmuld.listaDeCarpetasEnDatasetDescomprimido
            ,'progresoDeDescompresion':progresoDeDescompresion
            ,'estaEnFaseDeteniendoProcesamientoDeImagenes':estaEnFaseDeteniendoProcesamientoDeImagenes
            ,'estaEnFaseProcesandoImagenes':estaEnFaseProcesandoImagenes
            ,'estaEnFaseTerminoLaCreacionDelDataset':dmuld.estaEnFase_TERMINO_LA_CREACION_DEL_DATASET()
            ,'estaEnFaseTerminandoLaCreacionDelDataset':dmuld.estaEnFase_TERMINANDO_LA_CREACION_DEL_DATASET()
            }
    if estaEnFaseDeteniendoProcesamientoDeImagenes or estaEnFaseProcesandoImagenes:
        args:ArgumentosDeEventosAlProcesarYcrearDataSet=dmuld.estadoDeProcesamientoDeImagenes
        d['hayArgs']=args is not None
        if args is not None:
            d['nombreImagen']=args.nombreImagen
            d['nombreCarpetaPadre'] = args.nombreCarpetaPadre
            d['indiceDeCarpeta'] = args.indiceDeCarpeta
            d['indiceDeImagenEnCarpeta'] = args.indiceDeImagenEnCarpeta
            d['indiceImagen'] = args.indiceImagen
            d['porcientoDeImagenConRespectoAlTotal'] = args.porcientoDeImagenConRespectoAlTotal
            d['porcientoDeImagenConRespectoAlaCarpeta'] = args.porcientoDeImagenConRespectoAlaCarpeta
            d['porcientoDeCarpeta'] = args.porcientoDeCarpeta
            d['cantidadTotalDeImagenes'] = args.cantidadTotalDeImagenes
            d['cantidadTotalDeImagenesEnEstaCarpeta'] = args.cantidadTotalDeImagenesEnEstaCarpeta
            d['indiceDeFaseDeImagen'] = args.indiceDeFaseDeImagen
            d['cantidadTotalDeFasesDeImagen'] = args.cantidadTotalDeFasesDeImagen
            d['progresoDeFasesDeImagen'] = args.progresoDeFasesDeImagen
            d['cantidadDeCarpetas'] = args.cantidadDeCarpetas

    return JsonResponse({
        'content': d
    })



@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
def metodoIntentarComenzarProcesoAgregarDataset(request):
    esValido=False
    llegoAlFinal=False
    mensaje=""
    mandoADetener=False

    form = Formulario_AgregarDataset()
    form.comprobarValidacion(request)



    if form.esValido():
        # print(request.POST)
        # d=qdict_to_dict(request.POST)
        # print("d=",d)
        listaDeCarpetas=getPost(request,"listaDeCarpetas")
        listaDeCalificaciones =getPost(request,"listaDeCalificaciones")
        listaDeDetalles = getPost(request, "listaDeDetalles")
        #leng=getPostInt(request,"leng_matrisDeNombreDeClasificaciones")
        matrisDeNombreDeClasificaciones=[]
        for i in range(len(listaDeCarpetas)):
            #fila=getPost(request,"matrisDeNombreDeClasificaciones["+str(i)+"][]")
            #print("i=",i," fila=",fila," len",len(fila))
            #matrisDeNombreDeClasificaciones.append(fila)
            matrisDeNombreDeClasificaciones.append([listaDeCalificaciones[i],listaDeCarpetas[i]])
        #matrisDeNombreDeClasificaciones=getPost(request,"matrisDeNombreDeClasificaciones")
        respestaDeValidacionDe_matrisDeNombreDeClasificaciones=logicaUploadDataset.esValidoMatrisDeclasificaciones(request,matrisDeNombreDeClasificaciones)
        if respestaDeValidacionDe_matrisDeNombreDeClasificaciones.esValido:
            logicaUploadDataset.addNombreDeDatasetEnProceso(form.nombre.valor)
            esValido=True
            dt:DatosDelDataset=DatosDelDataset()
            dt.nombre=form.nombre.valor
            dt.tipoDeFruto=form.tipoDeFruto.valor
            dt.descripcion=form.descripcion.valor
            dt.matrizPar_Clasificacion_Carpeta=matrisDeNombreDeClasificaciones
            for i in range(len(listaDeCarpetas)):
                dt.matris_Clasificacion_Carpeta_Descripcion.append([listaDeCalificaciones[i],listaDeCarpetas[i],listaDeDetalles[i]])
            print("intenta crear el dataset !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!111")
            r:RespestaDeMetodoIntentarCrearDataset=logicaUploadDataset.crearDatasetProcesado(request,dt)
            print("00000000000000000000000000  r.mandoADetener",r.mandoADetener)
            if r.mandoADetener or not (logicaUploadDataset.getDatosEnMemoriaUploadDataset(request).estaEnFase_TERMINO_LA_CREACION_DEL_DATASET()):
                mandoADetener=True
            logicaUploadDataset.removeNombreDeDatasetEnProceso(form.nombre.valor)
            llegoAlFinal=True
            print("fue valido")
        else:
            print("la matriz no fue valida !!!!!!!!!!!!!!!!!!!!!!")
            esValido = False
            mensaje = respestaDeValidacionDe_matrisDeNombreDeClasificaciones.mensaje
    else:
        print("el formulario  no fue valido !!!!!!!!!!!!!!!!!!!!!!")
        esValido = False
        mensaje = form.mensajeNoValido

    return JsonResponse({'fueValido': esValido,'mensaje':mensaje,"llegoAlFinal":llegoAlFinal,'mandoAdetener':mandoADetener})

@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
def metodoDetenerProcesamientoDeImagenes(request):
    logicaUploadDataset.llamoADetener_ProcesamientoDeImagenes(request)
    return JsonResponse({
        'content': "todoBien"
    })


@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
@seguridadError
def vistaListarDataset(request):

    lcp = LocalizacionDePagina(LP_INVESTIGACION,LP_GESTION, "Lista de Datasets")

    return renderAppActual(request, 'Visual/ListarDasets.html', {
    'listaDatosDeDataset':DatosDataset.getDatosDataset(bd)
    }, lcp)


@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
def metodoEliminarDataset(request):
    idDataset=getPostInt(request,"idDataset")
    #print("idDataset=",idDataset)
    existeDataset=bd.existeDataset_ID(idDataset)
    if existeDataset:
        #datasetNombre=bd.getDataset_id(idDataset).Nombre
        dataset=bd.getDataset_id(idDataset)
        direccion=dataset.Direccion_Imagenes_Originales
        lm = bd.getModeloNeuronal_All_Dataset(dataset)
        for m in lm:
            eliminar_Archivo_ModeloNeuronalFisico(m.Direccion)
        bd.deleteDataset_Cascada_id(idDataset)
        #eliminar_CarpetaContenedoraDeDatasetCompleto_ProcesadoYNoProcesado_Si_hay_carpetas_o_archivos(request,datasetNombre)
        eliminar_CarpetaContenedoraDeDatasetCompleto_ProcesadoYNoProcesado_EnDireccion(direccion)
    return JsonResponse({
        'existeDataset': existeDataset
    })

#@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
def metodoGetImagenDeEjemploDataset50px(request):
    idDataset = getPostInt(request, "idDataset")
    indiceDeImagen=getPostInt(request, "indiceDeImagen")
    existeDataset = bd.existeDataset_ID(idDataset)

    imgBase64=""
    if existeDataset:
        dataset=bd.getDataset_id(idDataset)
        listaClasesClasificacion=bd.getClaseDeClasificacion_All_Dataset(dataset)
        carpetaClasificacion=None
        for c in listaClasesClasificacion:
            if c.Indice==indiceDeImagen:
                carpetaClasificacion=c.NombreCarpetaCorrespondiente
                break
        # carpetaImagenDeEjemplo:File = getYCrear_CarpetaContenedoraDeDatasetCompleto_ImagenDeEjemplo50px(request, dataset.Nombre,
        #                                                                                        carpetaClasificacion)
        # print("--------------------------------------")
        carpetaImagenDeEjemplo: File = get_CarpetaContenedoraDeDatasetCompleto_DatasetID_ImagenDeEjemplo50px(dataset.Direccion_Imagenes_Originales,
                                                                                                         carpetaClasificacion)
        # print("carpetaImagenDeEjemplo=",carpetaImagenDeEjemplo)
        imagenDeEjemplo=carpetaImagenDeEjemplo.listFiles()[0]

        imgBase64=toBase64Str_Img(str(imagenDeEjemplo))
    return JsonResponse({
        'existeDataset': existeDataset,'imgBase64':imgBase64
    })


#@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
def metodoGetImagenDeEjemploDataset900_600px(request):
    idDataset = getPostInt(request, "idDataset")
    indiceDeImagen=getPostInt(request, "indiceDeImagen")
    existeDataset = bd.existeDataset_ID(idDataset)

    imgBase64=""
    if existeDataset:
        dataset=bd.getDataset_id(idDataset)
        listaClasesClasificacion=bd.getClaseDeClasificacion_All_Dataset(dataset)
        carpetaClasificacion=None
        for c in listaClasesClasificacion:
            if c.Indice==indiceDeImagen:
                carpetaClasificacion=c.NombreCarpetaCorrespondiente
                break
        # carpetaImagenDeEjemplo:File = getYCrear_CarpetaContenedoraDeDatasetCompleto_ImagenDeEjemplo900_600px(request, dataset.Nombre,
        #                                                                                        carpetaClasificacion)
        carpetaImagenDeEjemplo: File = get_CarpetaContenedoraDeDatasetCompleto_DatasetID_ImagenDeEjemplo900_600px(
                                                                                                              dataset.Direccion_Imagenes_Originales,
                                                                                                              carpetaClasificacion)
        imagenDeEjemplo=carpetaImagenDeEjemplo.listFiles()[0]
        imgBase64=toBase64Str_Img(str(imagenDeEjemplo))
    return JsonResponse({
        'existeDataset': existeDataset,'imgBase64':imgBase64
    })


def __getDic_ListaImagenesDeDataset(request
                                    ,seEncuentraSeleccionadaImagenesProcesadas
                                    ,dataset:Dataset
                                    ,clasificacion
                                    ,indiceDeLasImagenes

                                    ,keyDicDeImagenes='dicDeImagenes'
                                    ,keyCantidadDeImg="cantidadDeImg"
                                    ,keyListaDeIndices='listaDeIndices'
                                    ,keyIActual="iActual"
                                    ,keyPrimerIndiceDeImagen="primerIndiceDeImagen"
                                    ,):
    dicDeImagenes = {}
    cantidadDeImg = 0
    listaDeIndices = []
    iActual = -1
    primerIndiceDeImagen = -1

    if seEncuentraSeleccionadaImagenesProcesadas:
        #url = getUrlCarpetaContenedoraDeDatasetCompleto_Procesado(request, dataset.Nombre)
        url =dataset.Direccion_Imagenes_Procesadas

    else:
        url = dataset.Direccion_Imagenes_Originales
        #url = getUrlCarpetaContenedoraDeDatasetCompleto_NoProcesado(request, dataset.Nombre)
    #f = File.castear(url)
    f = getFile_DireccionCompleta_Dataset(url)
    #f= f.listFiles()[0]
    f.append(bd.getNombreCarpeta_deClasificacion(dataset, clasificacion))

    lf = f.listFiles()
    primerIndiceDeImagen = ConfiguracionDePaginacionDeImg.STEP * (indiceDeLasImagenes - 1)
    li: List[File] = lf[primerIndiceDeImagen:ConfiguracionDePaginacionDeImg.STEP * (indiceDeLasImagenes)]
    for i, v in enumerate(li):
        dicDeImagenes[str(primerIndiceDeImagen + i)] = v.getName()
    cantidadDeImg = len(li)
    p = PaginacionSimple(indiceActual=indiceDeLasImagenes
                         , cantidadDeElementos=len(lf)#cantidadDeImg
                         , step=ConfiguracionDePaginacionDeImg.STEP
                         , cantidadDeIndicesAMostrarMaximo=ConfiguracionDePaginacionDeImg.INDICES)
    listaDeIndices = p.listaDeIndices
    iActual = p.iActual

    #print("dicDeImagenes=",dicDeImagenes)
    dic={keyDicDeImagenes:dicDeImagenes
        ,keyCantidadDeImg:cantidadDeImg
        ,keyListaDeIndices:listaDeIndices
        ,keyIActual:iActual
        ,keyPrimerIndiceDeImagen:primerIndiceDeImagen}
    return dic


#@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
def metodoGetListaImagenesDeDataset(request):


    existeDataset=False
    # dicDeImagenes={}
    # cantidadDeImg=0
    # listaDeIndices=[]
    # iActual=-1
    # primerIndiceDeImagen=-1

    idDelDataset=getPostInt(request,"idDelDataset")
    indiceDeLasImagenes=getPostInt(request,"indiceDeLasImagenes")
    seEncuentraSeleccionadaImagenesProcesadas=getPostBool(request,"seEncuentraSeleccionadaImagenesProcesadas")
    clasificacion=getPost(request,"clasificacion")

    #dic={}
    dicImg=None
    if bd.existeDataset_ID(idDelDataset):
        dataset=bd.getDataset_id(idDelDataset)
        existeDataset=True

        dicImg=__getDic_ListaImagenesDeDataset(request=request
                                            ,seEncuentraSeleccionadaImagenesProcesadas=seEncuentraSeleccionadaImagenesProcesadas
                                            ,dataset=dataset
                                            ,clasificacion=clasificacion
                                            ,indiceDeLasImagenes=indiceDeLasImagenes)
        #print("dicImg=",dicImg)

    return JsonResponse(appenDic(
        {'existeDataset': existeDataset}
        ,dicImg
    ))


def __getDicDetallesDataset_Json(request):
    existeDataset = False
    idDelDataset = getPostInt(request, "idDelDataset")
    print("idDelDataset=",idDelDataset)
    dicImg = None
    dicDS = None
    if bd.existeDataset_ID(idDelDataset):
        existeDataset = True
        dataset = bd.getDataset_id(idDelDataset)

        dicImg = __getDic_ListaImagenesDeDataset(request=request
                                                 , seEncuentraSeleccionadaImagenesProcesadas=True
                                                 , dataset=dataset
                                                 ,
                                                 clasificacion=bd.getClaseDeClasificacion_All_Dataset(dataset)[0].Nombre
                                                 , indiceDeLasImagenes=1)
        dt=DatosDataset(dataset, bd)

        dic={
            "nombre":dt.nombre
             ,"descripcion":dt.descripcion
             ,"id":dt.id
             ,"clasificaciones":dt.clasificaciones
             ,"cantidadDeImagenes":dt.cantidadDeImagenes
             ,"cantidadDeClasificaciones":dt.cantidadDeClasificaciones
             ,"fechaDeCreacion":{
                "day":dt.fechaDeCreacion.day
                ,"month":dt.fechaDeCreacion.month
                , "year": dt.fechaDeCreacion.year
                }
            ,"fruto":dt.fruto
            , "variedadFruto": dt.variedadFruto
            , "nombreCientificoFruto": dt.nombreCientificoFruto
            ,"matris_Clasificacion_CantidadDeImagenes":dt.matris_Clasificacion_CantidadDeImagenes
            ,"nombreUsuario":dt.nombreUsuario
            ,"matris_Clasificacion_Carpeta_Descripcion":dt.matris_Clasificacion_Carpeta_Descripcion

             }
        dicDS = {
            "datosDataset": dic
        }


    return appenDic(
        {'existeDataset': existeDataset}
        , [dicImg, dicDS]
    )

def __getDicDetallesDataset(request
                            ,keyDatosDataset="datosDataset"
                            ,keyExisteDataset='existeDataset'
                            ,metodoObtenerIdDelDataset=None


                                    ,keyDicDeImagenes='dicDeImagenes'
                                    ,keyCantidadDeImg="cantidadDeImg"
                                    ,keyListaDeIndices='listaDeIndices'
                                    ,keyIActual="iActual"
                                    ,keyPrimerIndiceDeImagen="primerIndiceDeImagen"
                            ):

    existeDataset = False
    if metodoObtenerIdDelDataset is None:
        idDelDataset = getPostInt(request, "idDelDataset")
    else:
        idDelDataset=metodoObtenerIdDelDataset()
    dicImg = None
    dicDS = None
    if bd.existeDataset_ID(idDelDataset):
        existeDataset = True
        dataset = bd.getDataset_id(idDelDataset)

        dicImg = __getDic_ListaImagenesDeDataset(request=request
                                                 , seEncuentraSeleccionadaImagenesProcesadas=True
                                                 , dataset=dataset
                                                 ,
                                                 clasificacion=bd.getClaseDeClasificacion_SortVisual_All_Dataset(dataset)[0].Nombre
                                                 , indiceDeLasImagenes=1

                                                 ,keyDicDeImagenes=keyDicDeImagenes
                                                 , keyCantidadDeImg=keyCantidadDeImg
                                                 , keyListaDeIndices=keyListaDeIndices
                                                 , keyIActual=keyIActual
                                                 , keyPrimerIndiceDeImagen=keyPrimerIndiceDeImagen

                                                 )

        dicDS = {
            keyDatosDataset: DatosDataset(dataset, bd)
        }
        return appenDic(
        {keyExisteDataset: existeDataset}
        ,[dicImg,dicDS]
    )
@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
def metodoGetDetallesDataset(request):
    return JsonResponse(__getDicDetallesDataset_Json(request))

@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
@seguridadError
def vistaDetallesDataset(request):


    lcp = LocalizacionDePagina(LP_INVESTIGACION,LP_GESTION, "Detalles del Dataset")

    return renderAppActual(request, 'Visual/DetallesDataset.html', __getDicDetallesDataset(request), lcp)

    # return renderAppActual(request, 'Visual/DetallesDataset.html',appenDic(
    #     {'existeDataset': existeDataset}
    #     ,[dicImg,dicDS]
    # ), lcp)



#@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
def metodoGetImagenDataset_ProcesadaONo_900_600px(request):
    idDataset = getPostInt(request, "idDelDataset")
    indiceDeImagen=getPostInt(request, "indiceDeImagen")
    #print("indiceDeImagen=",indiceDeImagen)

    seEncuentraSeleccionadaImagenesProcesadas = getPostBool(request, "seEncuentraSeleccionadaImagenesProcesadas")
    clasificacion = getPost(request, "clasificacion")

    existeDataset = bd.existeDataset_ID(idDataset)

    imgBase64=""
    if existeDataset:
        dataset=bd.getDataset_id(idDataset)
        # listaClasesClasificacion=bd.getClaseDeClasificacion_All_Dataset(dataset)

        # if seEncuentraSeleccionadaImagenesProcesadas:
        #     url = getUrlCarpetaContenedoraDeDatasetCompleto_Procesado(request, dataset.Nombre)
        # else:
        #     url = getUrlCarpetaContenedoraDeDatasetCompleto_NoProcesado(request, dataset.Nombre)
        # f = File.castear(url)
        # f = f.listFiles()[0]
        # f.append(bd.getNombreCarpeta_deClasificacion(dataset, clasificacion))

        if seEncuentraSeleccionadaImagenesProcesadas:
            # url = getUrlCarpetaContenedoraDeDatasetCompleto_Procesado(request, dataset.Nombre)
            url = dataset.Direccion_Imagenes_Procesadas

        else:
            url = dataset.Direccion_Imagenes_Originales
            # url = getUrlCarpetaContenedoraDeDatasetCompleto_NoProcesado(request, dataset.Nombre)
        # f = File.castear(url)
        f = getFile_DireccionCompleta_Dataset(url)
        # f= f.listFiles()[0]
        f.append(bd.getNombreCarpeta_deClasificacion(dataset, clasificacion))

        lf = f.listFiles()

        # carpetaClasificacion=None
        # for c in listaClasesClasificacion:
        #     if c.Indice==indiceDeImagen:
        #         carpetaClasificacion=c.NombreCarpetaCorrespondiente
        #         break
        # carpetaImagenDeEjemplo:File = getYCrear_CarpetaContenedoraDeDatasetCompleto_ImagenDeEjemplo900_600px(request, dataset.Nombre,
        #                                                                                        carpetaClasificacion)
        # imagenDeEjemplo=carpetaImagenDeEjemplo.listFiles()[0]
        #print("str(lf[indiceDeImagen])=",str(lf[indiceDeImagen]))
        imgBase64=toBase64Str_Img(str(lf[indiceDeImagen]))
    return JsonResponse({
        'existeDataset': existeDataset,'imgBase64':imgBase64
    })

#@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
def metodo_ResetearEstadoAlTerminar_AgregarDataset(request):
    logicaUploadDataset.llamoAResetearEstados(request)
    return JsonResponse({})



@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
@seguridadError
def vistaListarModeloNeuronal(request):

    lcp = LocalizacionDePagina(LP_INVESTIGACION,LP_GESTION, "Lista de Modelos Neuronales")

    return renderAppActual(request, 'Visual/listarModeloNeuronal.html', {
    'listaDatosDeModeloNeuronales':DatosModeloNeuronal.getDatosModelosNeuronales(bd)
    }, lcp)


@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
def metodoEliminarModeloNeuronal(request):
    print("va a eliminar al modelo...")
    idDelModelo=getPostInt(request,"idDelModelo")
    existeModelo=bd.existeModeloNeuronal_ID(idDelModelo)
    if existeModelo:
        direccion=bd.getModeloNeuronal_id(idDelModelo).Direccion
        bd.deleteModeloNeuronal_Cascada_id(idDelModelo)
        eliminar_Archivo_ModeloNeuronalFisico(direccion)
    print("modelo eliminado")
    return JsonResponse({
        'existeModelo': existeModelo
    })



# @user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
@seguridadError
def vistaDetallesModeloNeuronal(request):

    idDelModelo=getPostInt(request,"idDelModelo")
    existeModelo = bd.existeModeloNeuronal_ID(idDelModelo)
    # dicImg=None
    # dicDS=None
    dic={'existeModelo':existeModelo}
    if existeModelo:

        modelo = bd.getModeloNeuronal_id(idDelModelo)

        datosDeModelo=DatosModeloNeuronal(modelo=modelo,bd=bd)

        def getDicDetallesDataset(idDataset):#exte,
            return __getDicDetallesDataset(request
                                           # , keyDatosDataset="datosDataset"+exte
                                           # , keyExisteDataset='existeDataset'+exte
                                           , metodoObtenerIdDelDataset=lambda :idDataset

                                           # , keyDicDeImagenes='dicDeImagenes'+exte
                                           # , keyCantidadDeImg="cantidadDeImg"+exte
                                           # , keyListaDeIndices='listaDeIndices'+exte
                                           # , keyIActual="iActual"+exte
                                           # , keyPrimerIndiceDeImagen="primerIndiceDeImagen"+exte
                                           )

        dicDetallesDatasetEntrenamiento =getDicDetallesDataset(datosDeModelo.idDataset)#"Entrenamiento",
        dicDetallesDatasetValidacion = getDicDetallesDataset( datosDeModelo.idDatasetValidacion)#"Validacion",

        dic = appenDic(dic,{
            'datosDelModelo': datosDeModelo
            ,"datosDatasetEntrenamiento":dicDetallesDatasetEntrenamiento
            ,"datosDatasetValidacion":dicDetallesDatasetValidacion
        })
        # dic=appenDic(dic,dicDetallesDatasetEntrenamiento)
        # dic=appenDic(dic,dicDetallesDatasetValidacion)




    lcp = LocalizacionDePagina(LP_INVESTIGACION,LP_GESTION, "Detalles del Modelo Neuronal")



    return renderAppActual(request, 'Visual/DetallesModeloNeuronal.html',dic, lcp)

@user_passes_test(seguridadAdmin, login_url=APP_CNF.loguin_redirect)
@seguridadError
def vistaListarUsuarios(request):

    lcp = LocalizacionDePagina(LP_ADMINSITRACION,LP_GESTION, "Lista de Usuarios")

    return renderAppActual(request, 'Visual/listarUsuarios.html', {
    'listaDatosDeUsuarios':bd.getRepresentacionDeUsuario_All()

    }, lcp)

@user_passes_test(seguridadAdmin, login_url=APP_CNF.loguin_redirect)
@seguridadError
def vistaGuardarUsuario(request):
    lcp = LocalizacionDePagina(LP_ADMINSITRACION,LP_GESTION, "Agregar Usuario")
    return renderAppActual(request, 'Visual/AgregarUsuario.html', {
         'form': Formulario_AgregarUsuario()
    }, lcp)

@user_passes_test(seguridadAdmin, login_url=APP_CNF.loguin_redirect)
@seguridadError
def metodoGuardarUsuario(request):
    esValido=False
    mensaje=""
    formulario=Formulario_AgregarUsuario()
    esValido=formulario.comprobarValidacion(request)
    if esValido:

        print("existeUsuario=",bd.existeUsuario(str(formulario.usuario.valor).strip()))
        esValido = True
        valorEnPermiso=formulario.permisosDeUsuario.valor
        if valorEnPermiso=="1":
            valorEnPermiso=APP_CNF.consts.PERMISO_USUARIO
        elif valorEnPermiso=="2":
            valorEnPermiso = APP_CNF.consts.PERMISO_INVESTIGADOR
        else:
            valorEnPermiso = APP_CNF.consts.PERMISO_ADMIN
        bd.crearUsuario(
            username=formulario.usuario.valor
            ,password=formulario.contraseña.valor
            ,nombre=formulario.nombre.valor
            ,apellido=formulario.apellidos.valor
            ,correo=formulario.correo.valor
            ,esInvestigador=valorEnPermiso == APP_CNF.consts.PERMISO_INVESTIGADOR or valorEnPermiso == APP_CNF.consts.PERMISO_ADMIN
            ,esAdmin=valorEnPermiso == APP_CNF.consts.PERMISO_ADMIN
                        )


    else:
        mensaje = formulario.mensajeNoValido
        print("mensaje=",mensaje)

    formulario.verValoresDeCampos()

    print("Es valido=",esValido)

    return JsonResponse(
        {'fueValido': esValido, 'mensaje': mensaje})

def metodoCambiarContraseña(request):
    esValido = False
    mensaje = ""
    user:User= getUserRequest(request)
    if (not user.is_anonymous):
        if user.is_authenticated:
            formulario = Formulario_CambiarContraseñaUsuario()
            esValido = formulario.comprobarValidacion(request)
            if esValido:
                usernameACambiar=formulario.usuario.valor
                if  user.username!=usernameACambiar and not bd.esAdmin(user):
                    esValido=False
                    mensaje="No eres administrador"
                else:
                    bd.cambiarContraseñaUsuario(bd.getUser_username(usernameACambiar),formulario.contraseña.valor)
                    if user.username==usernameACambiar:
                        desloguearse(request,APP_CNF)
                        intentarLoguearse(request,user.username,formulario.contraseña.valor)
            else:
                mensaje = formulario.mensajeNoValido
                print("mensaje=", mensaje)
            formulario.verValoresDeCampos()

    print("Es valido=", esValido)

    return JsonResponse(
        {'fueValido': esValido, 'mensaje': mensaje})


def __vistaCambiarContrasena(request,usernameAModificar,urlSalida):
    formUsuario=Formulario_CambiarContraseñaUsuario()
    formUsuario.usuario.valor=usernameAModificar
    lcp = LocalizacionDePagina(LP_APLICACION,LP_GESTION, "Cambiar Contraseña")
    return renderAppActual(request, 'Visual/CambiarContrasena.html', {
        'form': formUsuario
        ,"urlSalida":urlSalida
        #,'usernameAModificar':usernameAModificar
    }, lcp)


@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
@seguridadError
def vistaCambiarContrasenaPropia(request):
    return __vistaCambiarContrasena(request,getUsernameRequest(request),APP_CNF.urls.URL_VISTA_CLASIFICAR_IMAGEN)


@user_passes_test(seguridadAdmin, login_url=APP_CNF.loguin_redirect)
@seguridadError
def vistaCambiarContrasenaExterna(request):
    username=getPost(request,"username")
    return __vistaCambiarContrasena(request,username,APP_CNF.urls.URL_VISTA_LISTAR_USUARIO)


@user_passes_test(seguridadAdmin, login_url=APP_CNF.loguin_redirect)
def metodoEliminarUsuario(request):
    print("va a eliminar al usuario...")
    idDelUsuario=getPostInt(request,"idDelUsuario")
    existeUsuario=bd.existeUsuario_id(idDelUsuario)
    esValido=False
    mensaje=""
    if existeUsuario:
        usuario:User=bd.getUser_id(idDelUsuario)
        if getUsernameRequest(request)!= usuario.username:
            esValido=True
            lm = bd.getModelosNeuronalesAll_Usuario(usuario)
            for m in lm:
                eliminar_Archivo_ModeloNeuronalFisico(m.Direccion)
            dt = bd.getDatasetAll_Usuario(usuario)
            for d in dt:
                eliminar_CarpetaContenedoraDeDatasetCompleto_ProcesadoYNoProcesado_EnDireccion(d.Direccion_Imagenes_Originales)
            bd.deleteUsuario_Cascada(usuario)
            print("usuario eliminado")
        else:
            mensaje = "No se puede eliminar al usuario que lo representa a usted actualmente "
    else:
        mensaje="No existe el usuario solicitado"
    print("existeUsuario:",existeUsuario)
    return JsonResponse({
        'existeUsuario': existeUsuario
        ,'fueValido': esValido, 'mensaje': mensaje
    })


@user_passes_test(seguridadAdmin, login_url=APP_CNF.loguin_redirect)
@seguridadError
def vistaEditarUsuario(request):
    idDelUsuario = getPostInt(request, "idDelUsuario")
    existeUsuario = bd.existeUsuario_id(idDelUsuario)
    esValido = existeUsuario
    mensaje = ""
    representacionDeUsuario=None
    if existeUsuario:
        representacionDeUsuario=bd.getRepresentacionDeUsuario_id(idDelUsuario)
    else:
        mensaje="No existe el usuario solicitado"
    print("existeUsuario:",existeUsuario)

    lcp = LocalizacionDePagina(LP_ADMINSITRACION,LP_GESTION, "Editar Usuario")
    return renderAppActual(request, 'Visual/EditarUsuario.html', {
        'existeUsuario': existeUsuario
        ,'fueValido': esValido, 'mensaje': mensaje
        ,'representacionDeUsuario':representacionDeUsuario
        ,'form':Formulario_EditarUsuario()
    }, lcp)


@user_passes_test(seguridadAdmin, login_url=APP_CNF.loguin_redirect)
def metodoEditarUsuario(request):
    #idDelUsuario = getPostInt(request, "idDelUsuario")
    #existeUsuario = bd.existeUsuario_id(idDelUsuario)
    print("se va a intentar editar usuario...")
    mensaje = ""
    #representacionDeUsuario=None
    formulario=Formulario_EditarUsuario()



    esValido = formulario.comprobarValidacion(request)
    formulario.verValoresDeCampos()
    print("esValido=",esValido)

    if esValido:
        valorEnPermiso = formulario.permisosDeUsuario.valor
        if valorEnPermiso == "1":
            valorEnPermiso = APP_CNF.consts.PERMISO_USUARIO
        elif valorEnPermiso == "2":
            valorEnPermiso = APP_CNF.consts.PERMISO_INVESTIGADOR
        else:
            valorEnPermiso = APP_CNF.consts.PERMISO_ADMIN
        bd.editarUsuario(
            id=formulario.id.valor
            ,nombre=formulario.nombre.valor
            ,apellido=formulario.apellidos.valor
            ,correo=formulario.correo.valor
            , esInvestigador=valorEnPermiso == APP_CNF.consts.PERMISO_INVESTIGADOR or valorEnPermiso == APP_CNF.consts.PERMISO_ADMIN
            , esAdmin=valorEnPermiso == APP_CNF.consts.PERMISO_ADMIN
            ,activo=formulario.activo.valor
                         )
        print("termino de editar el usuario")
    else:
        mensaje=formulario.mensajeNoValido
        print("mensaje=",mensaje)
    #print("existeUsuario:",existeUsuario)

    return JsonResponse({
        #'existeUsuario': existeUsuario
         'fueValido': esValido, 'mensaje': mensaje, "dioError":False
    })


@user_passes_test(seguridadAdmin, login_url=APP_CNF.loguin_redirect)
@seguridadError
def vistaDetallesUsuario(request):
    idDelUsuario = getPostInt(request, "idDelUsuario")
    existeUsuario = bd.existeUsuario_id(idDelUsuario)
    esValido = existeUsuario
    mensaje = ""
    representacionDeUsuario=None
    if existeUsuario:
        representacionDeUsuario=bd.getRepresentacionDeUsuario_id(idDelUsuario)
    else:
        mensaje="No existe el usuario solicitado"
    print("existeUsuario:",existeUsuario)

    lcp = LocalizacionDePagina(LP_ADMINSITRACION,LP_GESTION, "Detalles de Usuario")
    return renderAppActual(request, 'Visual/DetallesUsuario.html', {
        'existeUsuario': existeUsuario
        ,'fueValido': esValido, 'mensaje': mensaje
        ,'representacionDeUsuario':representacionDeUsuario
        ,'form':Formulario_EditarUsuario()
    }, lcp)


@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
@seguridadError
def vistaEditarDataset(request):
    hayQueRecuperarDatos = False
    idUltimoFrutoAgregado = None

    metodoObtenerElID=None
    if existeSes(request, APP_CNF.consts.KEY_ULTIMA_URL_AGREGAR_FRUTO_EXTERNO):
        hayQueRecuperarDatos = getSes(request,
                                      APP_CNF.consts.KEY_ULTIMA_URL_AGREGAR_FRUTO_EXTERNO) == APP_CNF.urls.URL_VISTA_EDITAR_DATASET \
                               and existeSes(request, APP_CNF.consts.KEY_ID_ULTIMO_FRUTO_AGREGADO)

        if hayQueRecuperarDatos:
            idUltimoFrutoAgregado = getSes(request, APP_CNF.consts.KEY_ID_ULTIMO_FRUTO_AGREGADO)
            putSes(request, APP_CNF.consts.KEY_ULTIMA_URL_AGREGAR_FRUTO_EXTERNO, None)
            putSes(request, APP_CNF.consts.KEY_ID_ULTIMO_FRUTO_AGREGADO, None)
            metodoObtenerElID=lambda :getSes(request,APP_CNF.consts.KEY_ID_ULTIMO_DATASET_A_EDITAR)

    lcp = LocalizacionDePagina(LP_ADMINSITRACION,LP_GESTION, "Editar Dataset")


    return renderAppActual(request, 'Visual/EditarDataset.html',appenDic(__getDicDetallesDataset(request
                                                                                                 ,metodoObtenerIdDelDataset=metodoObtenerElID
                                                                                                 )
                                                                         ,{"form": Formulario_EditarDataset()
                                                                             ,
                                                                           'listaDatosDeFrutos': DatosDeFruto.getDatosDeFrutos(
                                                                               bd)
                                                                             ,
                                                                           "hayQueRecuperarDatos": hayQueRecuperarDatos
                                                                             ,
                                                                           "idUltimoFrutoAgregado": idUltimoFrutoAgregado
                                                                           })
                           , lcp)

@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
def metodoAlmacenarIdDataset(request):
    putSes(request,APP_CNF.consts.KEY_ID_ULTIMO_DATASET_A_EDITAR,getPost(request,"idDataset"))
    return JsonResponse({
        # 'existeUsuario': existeUsuario
        'fueValido': True, 'mensaje': "", "dioError": False
    })

@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
def metodoEditarDataset(request):
    print("se va a intentar editar el dataset...")
    esValido = False
    mensaje = ""

    dioError = False



    form = Formulario_EditarDataset()
    esValido = form.comprobarValidacion(request)
    print("esValido=", esValido)
    if esValido:

        listaDeCarpetas = getPost(request, "listaDeCarpetas")
        listaDeCalificaciones = getPost(request, "listaDeCalificaciones")
        listaDeDetalles = getPost(request, "listaDeDetalles")
        matrisDeNombreDeClasificaciones = []
        listaNombreCarpetas=[c.NombreCarpetaCorrespondiente for c in bd.getClaseDeClasificacion_All_Dataset(bd.getDataset_id(form.id.valor))]
        for i in range(len(listaDeCarpetas)):
            matrisDeNombreDeClasificaciones.append([listaDeCalificaciones[i], listaDeCarpetas[i]])
        respestaDeValidacionDe_matrisDeNombreDeClasificaciones =RespuestaDeValidacionDeMarisDeclasificaciones \
            .esValidoMatrisDeclasificaciones(
            matrisDeNombreDeClasificaciones, listaNombreCarpetas
        )
        esValido=respestaDeValidacionDe_matrisDeNombreDeClasificaciones.esValido
        if esValido:
            for i,l in enumerate(matrisDeNombreDeClasificaciones):
                l.append(listaDeDetalles[i])
                #l.insert(0,listaDeDetalles[i])
            bd.editarDataset(
                id=form.id.valor
                , nombre=form.nombre.valor
                , fruto=bd.getFruto_id(form.tipoDeFruto.valor)
                , descripcion=form.descripcion.valor
                ,matrisDeNombreDeClasificaciones=matrisDeNombreDeClasificaciones
            )
            print("termino de editar el dataset")
        else:
            mensaje =respestaDeValidacionDe_matrisDeNombreDeClasificaciones.mensaje
            print("mensaje=", mensaje)




    else:
        mensaje = form.mensajeNoValido
        print("mensaje=", mensaje)
    return JsonResponse({
        # 'existeUsuario': existeUsuario
        'fueValido': esValido, 'mensaje': mensaje, "dioError": dioError
    })


@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
@seguridadError
def vistaEditarModeloNeuronal(request):

    idDelModelo=getPostInt(request,"idDelModelo")
    existeModelo = bd.existeModeloNeuronal_ID(idDelModelo)
    # dicImg=None
    # dicDS=None
    dic={'existeModelo':existeModelo}
    if existeModelo:

        modelo = bd.getModeloNeuronal_id(idDelModelo)

        datosDeModelo=DatosModeloNeuronal(modelo=modelo,bd=bd)

        def getDicDetallesDataset(idDataset):#exte,
            return __getDicDetallesDataset(request
                                           # , keyDatosDataset="datosDataset"+exte
                                           # , keyExisteDataset='existeDataset'+exte
                                           , metodoObtenerIdDelDataset=lambda :idDataset

                                           # , keyDicDeImagenes='dicDeImagenes'+exte
                                           # , keyCantidadDeImg="cantidadDeImg"+exte
                                           # , keyListaDeIndices='listaDeIndices'+exte
                                           # , keyIActual="iActual"+exte
                                           # , keyPrimerIndiceDeImagen="primerIndiceDeImagen"+exte
                                           )

        dicDetallesDatasetEntrenamiento =getDicDetallesDataset(datosDeModelo.idDataset)#"Entrenamiento",
        dicDetallesDatasetValidacion = getDicDetallesDataset( datosDeModelo.idDatasetValidacion)#"Validacion",

        dic = appenDic(dic,{
            'datosDelModelo': datosDeModelo
            ,"datosDatasetEntrenamiento":dicDetallesDatasetEntrenamiento
            ,"datosDatasetValidacion":dicDetallesDatasetValidacion
            ,"form":Formulario_EditarModeloNeuronal()
        })
        # dic=appenDic(dic,dicDetallesDatasetEntrenamiento)
        # dic=appenDic(dic,dicDetallesDatasetValidacion)




    lcp = LocalizacionDePagina(LP_INVESTIGACION,LP_GESTION, "Editar Modelo Neuronal")



    return renderAppActual(request, 'Visual/EditarModeloNeuronal.html',dic, lcp)


@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
def metodoEditarModelo(request):
    print("se va a intentar editar el modelo...")
    esValido = False
    mensaje = ""

    dioError = False



    form = Formulario_EditarModeloNeuronal()
    esValido = form.comprobarValidacion(request)
    print("esValido=", esValido)
    if esValido:
        bd.editarModeloNeuronal(
            id=form.id.valor
            ,nombre=form.nombre.valor
            #,fruto=form.tipoDeFruto.valor
            ,descripcion=form.descripcion.valor
        )
        print("termino de editar el modelo")
    else:
        mensaje = form.mensajeNoValido
        print("mensaje=", mensaje)
    return JsonResponse({
        # 'existeUsuario': existeUsuario
        'fueValido': esValido, 'mensaje': mensaje, "dioError": dioError
    })

def __getvistaAgregarTipoDeFruto(request,urlSalida):
    lcp = LocalizacionDePagina(LP_INVESTIGACION,LP_GESTION, "Agregar Fruto")

    return renderAppActual(request, 'Visual/AgregarTipoDeFruto.html', {
        "form": Formulario_AgregarTipoDeFruto()
        , "urlSalida": urlSalida
    }, lcp)

@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
@seguridadError
def vistaAgregarTipoDeFruto(request):
    return __getvistaAgregarTipoDeFruto(request,APP_CNF.urls.URL_VISTA_LISTAR_FRUTO)

@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
@seguridadError
def vistaAgregarTipoDeFruto_desdeExterno(request):
    urlSalida=getPost(request,"urlSalida")
    putSes(request,APP_CNF.consts.KEY_ULTIMA_URL_AGREGAR_FRUTO_EXTERNO,urlSalida)
    return __getvistaAgregarTipoDeFruto(request,urlSalida)



@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
def metodoAgregarTipoDeFruto(request):
    esValido = False
    mensaje = ""
    print("va intentar validar campos agregar fruto...")
    dioError = False
    form=Formulario_AgregarTipoDeFruto()
    esValido=form.comprobarValidacion(request)
    print("esValido=", esValido)
    form.verValoresDeCampos()
    if esValido:
        print("creando archivos de tipo de fruto...")
        urlRelativa=crearArchivosDe_TipoDeFruto(request=request
                                    , nombreDelFruto=form.nombre.valor
                                    , nombreDeLaImagen=form.nombreImagen.valor
                                    ,nombreKeyArchivo=str(form.ArchivoImagen)
                                                                    )
        print("guardando fruto")
        fruto:Fruto=bd.saveFruto(nombre=form.nombre.valor
                     ,nombreCientifico=form.nombreCientifico.valor
                     ,variedad=form.variedad.valor
                     ,descripcion=form.descripcion.valor
                     ,direccionImagen=urlRelativa)
        putSes(request,APP_CNF.consts.KEY_ID_ULTIMO_FRUTO_AGREGADO,fruto.id)
        print("creo el fruto")
    else:
        mensaje = form.mensajeNoValido
        print("mensaje=", mensaje)


    return JsonResponse({
        # 'existeUsuario': existeUsuario
        'fueValido': esValido, 'mensaje': mensaje, "dioError": dioError
    })


def metodoGetImagenDeEjemplo_TipoDeFruto50px(request):
    idDelFruto = getPostInt(request, "idDelFruto")

    existeFruto = bd.existeFruto_id(idDelFruto)

    imgBase64=""
    if existeFruto:
        fruto=bd.getFruto_id(idDelFruto)


        imagenDeEjemplo=getDireccionCompleta_ImagenTipoDeFruto50px(fruto.DireccionImagen)

        imgBase64=toBase64Str_Img(str(imagenDeEjemplo))
    return JsonResponse({
        'existeFruto': existeFruto,'imgBase64':imgBase64
    })


def metodoGetImagenDeEjemplo_TipoDeFruto900_900px(request):
    idDelFruto = getPostInt(request, "idDelFruto")

    existeFruto = bd.existeFruto_id(idDelFruto)

    imgBase64 = ""
    if existeFruto:
        fruto = bd.getFruto_id(idDelFruto)

        imagenDeEjemplo = getDireccionCompleta_ImagenTipoDeFruto900_900px(fruto.DireccionImagen)

        imgBase64 = toBase64Str_Img(str(imagenDeEjemplo))
    return JsonResponse({
        'existeFruto': existeFruto, 'imgBase64': imgBase64
    })

@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
@seguridadError
def vistaListarFrutos(request):

    lcp = LocalizacionDePagina(LP_INVESTIGACION,LP_GESTION, "Lista de Frutos")

    return renderAppActual(request, 'Visual/listarFrutos.html', {
    'listaDatosDeFrutos':DatosDeFruto.getDatosDeFrutos(bd)
    }, lcp)

@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
def metodoEliminarFruto(request):

    mensaje = ""

    idDelFruto = getPostInt(request, "idDelFruto")
    print("idDelFruto=",idDelFruto)

    esValido = bd.existeFruto_id(idDelFruto)

    print("va ha intentar eliminar al fruto..")
    if esValido:
        fruto=bd.getFruto_id(idDelFruto)
        ld=bd.getDatasetAll_Fruto(fruto)
        for dataset in ld:
            direccion = dataset.Direccion_Imagenes_Originales
            lm = bd.getModeloNeuronal_All_Dataset(dataset)
            for m in lm:
                eliminar_Archivo_ModeloNeuronalFisico(m.Direccion)
            eliminar_CarpetaContenedoraDeDatasetCompleto_ProcesadoYNoProcesado_EnDireccion(direccion)
        eliminarArchivosFruto(fruto.DireccionImagen)

        bd.deleteFruto_id_Cascada(idDelFruto)

        print("fruto eliminado")

    else:
        mensaje = "No existe el fruto solicitado"
    print("esValido:", esValido)

    return JsonResponse({
         'fueValido': esValido, 'mensaje': mensaje
    })

@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
def metodoEliminarTodosLosFrutos(request):
    dioError=False
    mensaje = ""
    lf=bd.getFrutosAll()
    for f in lf:
        fruto = f
        ld = bd.getDatasetAll_Fruto(fruto)
        for dataset in ld:
            direccion = dataset.Direccion_Imagenes_Originales
            lm = bd.getModeloNeuronal_All_Dataset(dataset)
            for m in lm:
                eliminar_Archivo_ModeloNeuronalFisico(m.Direccion)
            eliminar_CarpetaContenedoraDeDatasetCompleto_ProcesadoYNoProcesado_EnDireccion(direccion)
        eliminarArchivosFruto(fruto.DireccionImagen)

        bd.deleteFruto_id_Cascada(f.id)
    return JsonResponse({
        'dioError': dioError, 'mensaje': mensaje
    })

@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
def metodoEliminarTodosLosFrutosSeleccionados(request):
    dioError=False
    mensaje = ""
    print("request=",request)
    listaIds = getPost(request, "listaIds")

    #lf=[bd.getFruto_id(id) for id in listaIds]
    for id in listaIds:
        dioError=not bd.existeFruto_id(id)
        if not dioError:
            fruto = bd.getFruto_id(id)
            ld = bd.getDatasetAll_Fruto(fruto)
            for dataset in ld:
                direccion = dataset.Direccion_Imagenes_Originales
                lm = bd.getModeloNeuronal_All_Dataset(dataset)
                for m in lm:
                    eliminar_Archivo_ModeloNeuronalFisico(m.Direccion)
                eliminar_CarpetaContenedoraDeDatasetCompleto_ProcesadoYNoProcesado_EnDireccion(direccion)
            eliminarArchivosFruto(fruto.DireccionImagen)

            bd.deleteFruto_id_Cascada(id)
        else:
            mensaje="Un fruto ya fue eliminado con anterioridad"
    return JsonResponse({
        'dioError': dioError, 'mensaje': mensaje
    })



def __getVistaEditarFruto(request,urlSalida):
    mensaje = ""

    idDelFruto = getPostInt(request, "idDelFruto")
    print("idDelFruto=", idDelFruto)

    esValido = bd.existeFruto_id(idDelFruto)

    dic = {"fueValido": esValido}
    if esValido:
        dic = appenDic(dic, {
            "datosFruto": DatosDeFruto(bd.getFruto_id(idDelFruto))
        })

    else:
        mensaje = "No existe el fruto solicitado"
    print("esValido:", esValido)

    lcp = LocalizacionDePagina(LP_INVESTIGACION,LP_GESTION, "Editar Fruto")

    return renderAppActual(request, 'Visual/EditarTipoDeFruto.html',
                           appenDic(dic, {
                               "form": Formulario_EditarTipoDeFruto()
                               , "mensaje": mensaje
                               , "urlSalida": urlSalida

                           })
                           , lcp)

@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
@seguridadError
def vistaEditarFruto(request):#EditarTipoDeFruto.html
    return __getVistaEditarFruto(request,APP_CNF.urls.URL_VISTA_LISTAR_FRUTO)

@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
@seguridadError
def vistaEditarFruto_desdeExterno(request):
    urlSalida=getPost(request,"urlSalida")
    putSes(request,APP_CNF.consts.KEY_ULTIMA_URL_AGREGAR_FRUTO_EXTERNO,urlSalida)
    return __getVistaEditarFruto(request,urlSalida)

@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
def metodoEditarFruto(request):#EditarTipoDeFruto.html

    mensaje = ""

    #idDelFruto = getPostInt(request, "idDelFruto")
    #print("idDelFruto=", idDelFruto)
    form = Formulario_EditarTipoDeFruto()
    form.verValoresDeCampos()
    print("va intentar validar campos agregar fruto...")
    esValido = form.comprobarValidacion(request)
    print("esValido=", esValido)
    if esValido:
        fruto: Fruto=bd.getFruto_id(form.id.valor)
        urlRelativa=None
        if form.agregoUnaNuevaImagen.valor:
            print("creando archivos de tipo de fruto...")
            eliminarArchivosFruto(fruto.DireccionImagen)
            urlRelativa = crearArchivosDe_TipoDeFruto(request=request
                                                      , nombreDelFruto=form.nombre.valor
                                                      , nombreDeLaImagen=form.nombreImagen.valor
                                                      , nombreKeyArchivo=str(form.ArchivoImagen)
                                                      )
        print("editando fruto...")
        fruto=bd.editarFruto(id=form.id.valor
                        ,nombre=form.nombre.valor
                       ,nombreCientifico=form.nombreCientifico.valor
                       ,variedad=form.variedad.valor
                       ,descripcion=form.descripcion.valor
                             ,direccionImagen=urlRelativa)
        putSes(request, APP_CNF.consts.KEY_ID_ULTIMO_FRUTO_AGREGADO, fruto.id)
        print("edito el fruto")

            #urlCompleta=getDireccionCompleta_ImagenTipoDeFruto_DireccionRelativa(fruto.)
    else:
        mensaje = "No existe el fruto solicitado"
    print("esValido:", esValido)
    return JsonResponse({
        'fueValido': esValido, 'mensaje': mensaje
    })




@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
def metodoEliminarTodosLosDataset(request):
    dioError=False
    mensaje = ""
    print("va a eliminar todos los dataset...")
    ld=bd.getDatasetAll()
    for d in ld:
        dataset =d
        direccion = dataset.Direccion_Imagenes_Originales
        lm = bd.getModeloNeuronal_All_Dataset(dataset)
        for m in lm:
            eliminar_Archivo_ModeloNeuronalFisico(m.Direccion)
        bd.deleteDataset_Cascada_id(dataset.id)
        eliminar_CarpetaContenedoraDeDatasetCompleto_ProcesadoYNoProcesado_EnDireccion(direccion)
    print("dataset eliminados")
    return JsonResponse({
        'dioError': dioError, 'mensaje': mensaje
    })


@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
def metodoEliminarTodosLosDatasetsSeleccionados(request):
    dioError=False
    mensaje = ""
    print("request=",request)
    listaIds = getPost(request, "listaIds")

    #lf=[bd.getFruto_id(id) for id in listaIds]
    for id in listaIds:
        dioError=not bd.existeDataset_ID(id)
        if not dioError:
            dataset = bd.getDataset_id(id)
            direccion = dataset.Direccion_Imagenes_Originales
            lm = bd.getModeloNeuronal_All_Dataset(dataset)
            for m in lm:
                eliminar_Archivo_ModeloNeuronalFisico(m.Direccion)
            bd.deleteDataset_Cascada_id(dataset.id)
            eliminar_CarpetaContenedoraDeDatasetCompleto_ProcesadoYNoProcesado_EnDireccion(direccion)
        else:
            mensaje="Un dataset ya fue eliminado con anterioridad"
    return JsonResponse({
        'dioError': dioError, 'mensaje': mensaje
    })

@seguridadError
def vistaDetallesFruto(request):#EditarTipoDeFruto.html

    mensaje = ""

    idDelFruto = getPostInt(request, "idDelFruto")
    print("idDelFruto=", idDelFruto)

    esValido = bd.existeFruto_id(idDelFruto)

    df=None
    if esValido:
        df=DatosDeFruto(bd.getFruto_id(idDelFruto))



    else:
        mensaje = "No existe el fruto solicitado"
    print("esValido:", esValido)

    #
    lcp = LocalizacionDePagina(LP_INVESTIGACION,LP_GESTION, "Detalles Del Fruto")

    return renderAppActual(request, 'Visual/DetallesFruto.html',
                           {'fueValido': esValido, 'mensaje': mensaje, "datosFruto":df}
                           , lcp)



@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
def metodoEliminarTodosLosModelosNeuronales(request):
    dioError=False
    mensaje = ""
    print("va a eliminar todos los dataset...")
    lm=bd.getModelosNeuronalesAll()
    for m in lm:
        modelo=m
        direccion = modelo.Direccion
        bd.deleteModeloNeuronal_Cascada_id(modelo.id)
        eliminar_Archivo_ModeloNeuronalFisico(direccion)
    print("dataset eliminados")
    return JsonResponse({
        'dioError': dioError, 'mensaje': mensaje
    })


@user_passes_test(seguridadMinima, login_url=APP_CNF.loguin_redirect)
def metodoEliminarTodosLosModelosNeuronalesSeleccionados(request):
    dioError=False
    mensaje = ""
    print("request=",request)
    listaIds = getPost(request, "listaIds")

    #lf=[bd.getFruto_id(id) for id in listaIds]
    for id in listaIds:
        dioError=not bd.existeModeloNeuronal_ID(id)
        if not dioError:
            modelo = bd.getModeloNeuronal_id(id)
            direccion = modelo.Direccion
            bd.deleteModeloNeuronal_Cascada_id(modelo.id)
            eliminar_Archivo_ModeloNeuronalFisico(direccion)
        else:
            mensaje="Un modelo ya fue eliminado con anterioridad"
    return JsonResponse({
        'dioError': dioError, 'mensaje': mensaje
    })






@user_passes_test(seguridadAdmin, login_url=APP_CNF.loguin_redirect)
def metodoEliminarTodosLosUsauriosSeleccionados(request):
    dioError=False
    mensaje = ""
    print("request=",request)
    listaIds = getPost(request, "listaIds")

    #lf=[bd.getFruto_id(id) for id in listaIds]
    for id in listaIds:
        dioError=not bd.existeUsuario_id(id)
        if not dioError:
            usuario:User=bd.getUser_id(id)
            lm = bd.getModelosNeuronalesAll_Usuario(usuario)
            for m in lm:
                eliminar_Archivo_ModeloNeuronalFisico(m.Direccion)
            dt = bd.getDatasetAll_Usuario(usuario)
            for d in dt:
                eliminar_CarpetaContenedoraDeDatasetCompleto_ProcesadoYNoProcesado_EnDireccion(
                    d.Direccion_Imagenes_Originales)
            bd.deleteUsuario_Cascada(usuario)
        else:
            mensaje="Un usuario ya fue eliminado con anterioridad"
    return JsonResponse({
        'dioError': dioError, 'mensaje': mensaje
    })



def metodoGetImagenDeFruto(request):
    idDelFruto = getPostInt(request, "idDelFruto")

    existeFruto = bd.existeFruto_id(idDelFruto)

    imgBase64 = ""
    if existeFruto:
        fruto = bd.getFruto_id(idDelFruto)
        dire=getDireccionCompleta_ImagenTipoDeFruto_DireccionRelativa(fruto.DireccionImagen)
        #imagenDeEjemplo = getDireccionCompleta_ImagenTipoDeFruto900_900px(fruto.DireccionImagen)

        imgBase64 = toBase64Str_Img(str(dire))
    return JsonResponse({
        'existeFruto': existeFruto, 'imgBase64': imgBase64
    })


def vistaDetallesClasificacion(request):
    class DatosClasificacion:
        def __init__(self):
            self.mostrarConjuntoDeImgs = False
            self.direccionImgOriginal = ""
            self.direccionImgGrayWorld = ""
            self.direccionImgBoundingBox = ""
            self.direccionImgMresize = ""
            self.direccionImgCielAB = ""
            self.resultado = ""

            self.username=None
            self.fecha=None
            self.ip=None

    dd = DatosClasificacion()



    def actualizarDetalles(dd, idClasificacion, idProcesamientoDeImagen=None):
        dd.mostrarConjuntoDeImgs = True
        d = getDatosDeClasificacionDetalles(request=request
                                            , idClasificacion=idClasificacion
                                            , idProcesamientoDeImagen=idProcesamientoDeImagen)

        dd.direccionImgOriginal = d.datosDeImagenOriginal
        dd.direccionImgGrayWorld = d.datosDeImagenGrayWorld
        dd.direccionImgBoundingBox = d.datosDeImagenBoundingBox
        dd.direccionImgMresize = d.datosDeImagenMResize
        dd.direccionImgCielAB = d.datosDeImagenCielAB
        dd.resultado = d.clasificacion

    idClasificacion =None
    if APP_CNF.isPost(request, APP_CNF.forms.DETALLES_AL_CLASIFICAR):

        idClasificacion = getSes(request, KEY_ID_CLASIFICACION)
        idProcesamientoDeImagen = getSes(request, KEY_ID_CLASIFICACION)

        actualizarDetalles(dd, idClasificacion, idProcesamientoDeImagen)

    elif APP_CNF.isPost(request, APP_CNF.forms.DETALLES_LISTA_DE_CLASIFICACIONES_USUARIO):

        idClasificacion = getPostInt(request, APP_CNF.inputs.ID_CLASIFICACION)
        actualizarDetalles(dd, idClasificacion)

    datosDelModelo=None
    datosDeDataset=None
    datosDelFruto=None

    esValido = idClasificacion is not None
    mensaje=None
    dioError=False

    if esValido:
        clasi:Clasificacion=bd.getClasificacion_id(idClasificacion)

        dd.username=clasi.Username
        dd.fecha=clasi.Fecha
        dd.ip=clasi.id

        modelo:ModeloNeuronal=clasi.ModeloNeuronal

        datosDelModelo=DatosModeloNeuronal(modelo,bd)
        dataset:Dataset=bd.getEntrenamiento_ModeloNeuronal(modelo).Dataset
        datosDeDataset=DatosDataset(dataset,bd)
        datosDelFruto = DatosDeFruto(dataset.Fruto)
    else:
        mensaje="No existe esta clasificación  "
        return vistaError_MultivalueKeyPost(request)







    return renderAppActual(request, 'Visual/Detalles Clasificacion.html', {
        # 'mostrarConjuntoDeImgs': dd.mostrarConjuntoDeImgs
        # , 'direccionImgOriginal': dd.direccionImgOriginal
        # , 'direccionImgGrayWorld': dd.direccionImgGrayWorld
        # , 'direccionImgBoundingBox': dd.direccionImgBoundingBox
        # , 'direccionImgMresize': dd.direccionImgMresize
        # , 'direccionImgCielAB': dd.direccionImgCielAB
        # , 'resultado': dd.resultado
        'datosDelModelo':datosDelModelo
        ,'datosDataset':datosDeDataset
        ,'datosFruto':datosDelFruto
        ,'fueValido':esValido
        ,'mensaje': mensaje
        ,'dioError':dioError
        ,'datosClasificacion':dd
    }, LocalizacionDePagina(LP_APLICACION,"Detalles Clasificación De Imagen "))

def metodoGetImagenDeClasificacion(request):
    idClasificacion = getPostInt(request, "idClasificacion")

    existeClasificacion = bd.existeClasificacion_id(idClasificacion)

    imgBase64 = ""
    if existeClasificacion:
        clasi=bd.getClasificacion_id(idClasificacion)

        dire=APP_CNF.detURL_Completa_CampoImagen(clasi.Procesamiento.ImagenOriginal)

        imgBase64 = toBase64Str_Img(str(dire))
    return JsonResponse({
        'existeClasificacion': existeClasificacion, 'imgBase64': imgBase64
    })