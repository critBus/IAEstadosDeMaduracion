"""ProyectoPCChar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
# from ProyectoPCChar import settings
from django.conf import settings
from django.conf.urls.static import static

from ReneDjangoApp.Utiles.Utiles import *
from Aplicacion.UtilesAplicacion.ConstantesApp import APP_CNF


from ProyectoPCChar.view import *
admin.AdminSite.site_header="Administración"
admin.AdminSite.site_title="Administración"

from django.conf.urls import url

#admin.AdminSite.index_title="Administración"
urlpatterns = [
    path(APP_CNF.urls.URL_POST_SUBIR_ARCHIVO+"/",metodoSuviendoArchivo),
    path(APP_CNF.urls.URL_POST_METODO_DETENER_UPLOAD_DATASET+"/",metodoDetenerUploadDataset),
    path(APP_CNF.urls.URL_POST_METODO_DETENER_DESCOMPRESION_DATASET+"/",metodoDetenerDescompresionDataset),
    path(APP_CNF.urls.URL_POST_METODO_DETENER_PROCESAMIENTO_DE_IMAGENES+"/",metodoDetenerProcesamientoDeImagenes),
    path(APP_CNF.urls.URL_POST_METODO_GET_ESTADO_VISTA_ENTRADA_DATASET+"/",metodoGetEstadoVistaEntradaDataset),
    path(APP_CNF.urls.URL_POST_METODO_ELIMINAR_DATASET_SUBIDO+"/",metodoEliminarDatasetSubido),
    path(APP_CNF.urls.URL_POST_METODO_INTENTAR_COMENZAR_PROCESO_AGREGAR_DATASET+"/",metodoIntentarComenzarProcesoAgregarDataset),

    # path(APP_CNF.urls.URL_POST_METODO_CLASIFICAR+"/",metodoClasificarPost),

    path(APP_CNF.urls.URL_POST_METODO_PASO_GRAY_WORD+"/",metodoPasoGrayWordPost),
    path(APP_CNF.urls.URL_POST_METODO_PASO_BOUNDING_BOX+"/",metodoPasoBoundingBoxPost),
    path(APP_CNF.urls.URL_POST_METODO_PASO_MRESIZE+"/",metodoPasoMResizePost),
    path(APP_CNF.urls.URL_POST_METODO_PASO_CIELAB+"/",metodoPasoCielABPost),
    path(APP_CNF.urls.URL_POST_METODO_PASO_PREDICCION+"/",metodoPasoPrediccionPost),

    path(APP_CNF.urls.URL_POST_METODO_COMENZAR_ENTRENAMIENTO+"/",metodoLlamarAComenzarEntrenamiento),
    path(APP_CNF.urls.URL_POST_METODO_DETENER_ENTRENAMIENTO+"/",metodoLlamarADetenerEntrenamiento),
    path(APP_CNF.urls.URL_POST_GET_ESTADO_ENTRENAMIENTO+"/",metodoGetEstadoDeEntrenamiento),

    path(APP_CNF.urls.URL_POST_METODO_ELIMINAR_DATASET+"/",metodoEliminarDataset),
    path(APP_CNF.urls.URL_POST_METODO_GET_IMG_DE_EJEMPLO_50_PX+"/",metodoGetImagenDeEjemploDataset50px),
    path(APP_CNF.urls.URL_POST_METODO_GET_IMG_DE_EJEMPLO_900_600_PX+"/",metodoGetImagenDeEjemploDataset900_600px),
    path(APP_CNF.urls.URL_POST_METODO_GET_LISTA_IMAGENES_DEL_DATASET+"/",metodoGetListaImagenesDeDataset),
    path(APP_CNF.urls.URL_POST_METODO_GET_IMG_DATASET_900_600_PX+"/",metodoGetImagenDataset_ProcesadaONo_900_600px),
    path(APP_CNF.urls.URL_POST_METODO_GET_DETALLES_DEL_DATASET+"/",metodoGetDetallesDataset),
    path(APP_CNF.urls.URL_POST_METODO_RESETEAR_ESTADOS_AGREGAR_DATASET+"/",metodo_ResetearEstadoAlTerminar_AgregarDataset),

    path(APP_CNF.urls.URL_POST_METODO_ELIMINAR_MODELO_NUERONAL+"/",metodoEliminarModeloNeuronal),
    path(APP_CNF.urls.URL_POST_METODO_INTENTAR_AGREGAR_USUARIO+"/",metodoGuardarUsuario),
    path(APP_CNF.urls.URL_POST_METODO_INTENTAR_CAMBIAR_CONTRASENA+"/",metodoCambiarContraseña),
    path(APP_CNF.urls.URL_POST_METODO_INTENTAR_ELIMINAR_USUARIO+"/",metodoEliminarUsuario),
    path(APP_CNF.urls.URL_POST_METODO_INTENTAR_EDITAR_USUARIO+"/",metodoEditarUsuario),
    path(APP_CNF.urls.URL_POST_METODO_INTENTAR_EDITAR_DATASET+"/",metodoEditarDataset),
    path(APP_CNF.urls.URL_POST_METODO_INTENTAR_EDITAR_MODELO_NEURONAL+"/",metodoEditarModelo),
    path(APP_CNF.urls.URL_POST_METODO_INTENTAR_AGREGAR_TIPO_DE_FRUTO+"/",metodoAgregarTipoDeFruto),

    path(APP_CNF.urls.URL_POST_METODO_GET_IMG_DE_EJEMPLO_50_PX_FRUTO+"/",metodoGetImagenDeEjemplo_TipoDeFruto50px),
    path(APP_CNF.urls.URL_POST_METODO_GET_IMG_DE_EJEMPLO_900_900_PX_FRUTO+"/",metodoGetImagenDeEjemplo_TipoDeFruto900_900px),
    path(APP_CNF.urls.URL_POST_METODO_INTENTAR_ELIMINAR_FRUTO+"/",metodoEliminarFruto),
    path(APP_CNF.urls.URL_POST_METODO_INTENTAR_ELIMINAR_TODOS_LOS_FRUTO+"/",metodoEliminarTodosLosFrutos),
    path(APP_CNF.urls.URL_POST_METODO_INTENTAR_ELIMINAR_TODOS_LOS_FRUTO_SELECCIONADOS+"/",metodoEliminarTodosLosFrutosSeleccionados),
    path(APP_CNF.urls.URL_POST_METODO_INTENTAR_EDITAR_FRUTO+"/",metodoEditarFruto),
    path(APP_CNF.urls.URL_POST_METODO_INTENTAR_ELIMINAR_TODOS_LOS_DATASETS+"/",metodoEliminarTodosLosDataset),
    path(APP_CNF.urls.URL_POST_METODO_INTENTAR_ELIMINAR_TODOS_LOS_DATASETS_SELECCIONADOS+"/",metodoEliminarTodosLosDatasetsSeleccionados),
    path(APP_CNF.urls.URL_POST_METODO_INTENTAR_ELIMINAR_TODOS_LOS_MODELOS_NEURONALES+"/",metodoEliminarTodosLosModelosNeuronales),
    path(APP_CNF.urls.URL_POST_METODO_INTENTAR_ELIMINAR_TODOS_LOS_MODELOS_NEURONALES_SELECCIONADOS+"/",metodoEliminarTodosLosModelosNeuronalesSeleccionados),
    path(APP_CNF.urls.URL_POST_METODO_ALMACENAR_ID_DATASET_EDITAR+"/",metodoAlmacenarIdDataset),
    path(APP_CNF.urls.URL_POST_METODO_INTENTAR_ELIMINAR_TODOS_LOS_USUARIOS_SELECCIONADOS+"/",metodoEliminarTodosLosUsauriosSeleccionados),
    path(APP_CNF.urls.URL_POST_METODO_GET_IMG_DE_FRUTO+"/",metodoGetImagenDeFruto),
path(APP_CNF.urls.URL_POST_METODO_GET_IMG_ORIGINAL_DEL_CLASIFICACION+"/",metodoGetImagenDeClasificacion),



    path("",vistaClasificar),

    path('admin/', admin.site.urls),

    pathR(APP_CNF.urls.URL_VISTA_CLASIFICAR_IMAGEN,vistaClasificar),
    pathR(APP_CNF.urls.URL_VISTA_DETALLES_CLASIFICACION,vistaDetallesClasificacion ),
    pathR(APP_CNF.urls.URL_VISTA_LISTA_CLASIFICACIONES_USUARIO, vistaClasificaciones),
    pathR(APP_CNF.urls.URL_VISTA_ENTRENAMIENTO,vistaEntrenamiento ),
    pathR(APP_CNF.urls.URL_VISTA_AGREGAR_DATASET,vistaAgregarDataset ),
    pathR(APP_CNF.urls.URL_VISTA_AGREGAR_DATASET_RECARGAR,vistaAgregarDataset_MandoARecargar ),
    pathR(APP_CNF.urls.URL_VISTA_LISTAR_DATASET,vistaListarDataset ),
    pathR(APP_CNF.urls.URL_VISTA_DETALLES_DEL_DATASET,vistaDetallesDataset ),
    pathR(APP_CNF.urls.URL_VISTA_LISTAR_MODELO_NEURONAL,vistaListarModeloNeuronal ),
    pathR(APP_CNF.urls.URL_VISTA_DETALLES_DEL_MODELO_NEURONAL,vistaDetallesModeloNeuronal ),
    pathR(APP_CNF.urls.URL_VISTA_LISTAR_USUARIO,vistaListarUsuarios ),
    pathR(APP_CNF.urls.URL_VISTA_AGREGAR_USUARIO,vistaGuardarUsuario ),
    pathR(APP_CNF.urls.URL_VISTA_CAMBIAR_CONTRASENA_PROPIA,vistaCambiarContrasenaPropia ),
    pathR(APP_CNF.urls.URL_VISTA_CAMBIAR_CONTRASENA_EXTERNA,vistaCambiarContrasenaExterna ),
    pathR(APP_CNF.urls.URL_VISTA_EDITAR_USUARIO,vistaEditarUsuario ),
    pathR(APP_CNF.urls.URL_VISTA_DETALLES_USUARIO,vistaDetallesUsuario ),
    pathR(APP_CNF.urls.URL_VISTA_EDITAR_DATASET,vistaEditarDataset ),
    pathR(APP_CNF.urls.URL_VISTA_EDITAR_MODELO_NEURONAL,vistaEditarModeloNeuronal ),
    pathR(APP_CNF.urls.URL_VISTA_AGREGAR_FRUTO,vistaAgregarTipoDeFruto ),
    pathR(APP_CNF.urls.URL_VISTA_LISTAR_FRUTO,vistaListarFrutos ),
    pathR(APP_CNF.urls.URL_VISTA_EDITAR_FRUTO,vistaEditarFruto ),
    pathR(APP_CNF.urls.URL_VISTA_DETALLES_FRUTO,vistaDetallesFruto ),
    pathR(APP_CNF.urls.URL_VISTA_AGREGAR_FRUTO_DESDE_EXTERNO,vistaAgregarTipoDeFruto_desdeExterno ),
    pathR(APP_CNF.urls.URL_VISTA_EDITAR_FRUTO_DESDE_EXTERNO,vistaEditarFruto_desdeExterno ),

    APP_CNF.pathR_loguin("Visual/loguin.html"),
    APP_CNF.pathR_Logout(),
    APP_CNF.pathR_Admin(),
    url(r'^.+$', vistaErrorUrl),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# path(APP_CNF.urls.URL_VISTA_DETALLES_CLASIFICACION+"/",vistaDetalles ,name=APP_CNF.urls.URL_VISTA_DETALLES_CLASIFICACION),
    # path(APP_CNF.urls.URL_VISTA_LISTA_CLASIFICACIONES_USUARIO+"/", vistaPruebas,name=APP_CNF.urls.URL_VISTA_LISTA_CLASIFICACIONES_USUARIO),
    # path('admin/', admin.site.urls),#,{'next':'pwVista/'}
#pathR('asd', vistaIrAadministracion),
# path("pruebas/",vistaPruebas),
# pathR_Admin(APP_CNF.urls.URL_VISTA_ADMINISTRACION),
# path('pruebas/', vistaPruebas),
# path('pwVista/', primeraVista),
# path('pwVista2/<p1>/<int:p2>', segundaVista),
# path('pwVista3/', terceraVista),
# path('pwVista4/', cuartaVista),
# path('pwVista5/', quintaVista),

# path('accounts/', include('django.contrib.auth.urls')),
# path('logearse/', vistaLogearse),
#pathR(APP_CNF.urls.URL_VISTA_DESLOGUEARSE, vistaDesloguearse),

# urlpatterns+=static(settings.MEDIA_URL,document_rot=settings.MEDIA_ROOT)
