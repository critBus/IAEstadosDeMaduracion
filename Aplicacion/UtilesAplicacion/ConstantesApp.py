from ProyectoPCChar.settings import BASE_DIR
from ReneDjangoApp.Utiles.Utiles import *
from ReneDjangoApp.Utiles.Clases.ClasesDeConstantes import *



class UrlsApp(URL_Constants):
    URL_VISTA_CLASIFICAR_IMAGEN = 'plantilla'
    URL_VISTA_DETALLES_CLASIFICACION = 'detalles'
    URL_VISTA_LISTA_CLASIFICACIONES_USUARIO='clasificaciones'
    URL_VISTA_ENTRENAMIENTO = 'entrenamiento'
    URL_VISTA_AGREGAR_DATASET="agregar_dataset"
    URL_VISTA_AGREGAR_DATASET_RECARGAR="agregar_dataset_recargar"
    URL_VISTA_LISTAR_DATASET="listar_dataset"
    URL_VISTA_DETALLES_DEL_DATASET="vista_detalles_del_dataset"
    URL_VISTA_LISTAR_MODELO_NEURONAL = "listar_modelo_neuronal"
    URL_VISTA_DETALLES_DEL_MODELO_NEURONAL = "vista_detalles_del_modelo_neuronal"
    URL_VISTA_LISTAR_USUARIO = "listar_usuario"
    URL_VISTA_AGREGAR_USUARIO = "agregar_usuario"
    URL_VISTA_CAMBIAR_CONTRASENA_PROPIA = "cambiar_contrasena_propia"
    URL_VISTA_CAMBIAR_CONTRASENA_EXTERNA = "cambiar_contrasena_externa"
    URL_VISTA_EDITAR_USUARIO = "editar_usuario"
    URL_VISTA_DETALLES_USUARIO = "detalles_usuario"
    URL_VISTA_EDITAR_DATASET = "editar_dataset"
    URL_VISTA_EDITAR_MODELO_NEURONAL = "editar_modelo_neuronal"
    URL_VISTA_AGREGAR_FRUTO = "agregar_fruto"
    URL_VISTA_AGREGAR_FRUTO_DESDE_EXTERNO = "agregar_fruto_desde_externo"
    URL_VISTA_LISTAR_FRUTO = "listar_fruto"
    URL_VISTA_EDITAR_FRUTO = "editar_fruto"
    URL_VISTA_EDITAR_FRUTO_DESDE_EXTERNO = "editar_fruto_desde_externo"
    #URL_VISTA_EDITAR_FRUTO_DESDE_EXTERNO_EDITAR_DATASET = "editar_fruto_desde_externo_editar_dataset"
    URL_VISTA_DETALLES_FRUTO = "detalles_fruto"

    URL_POST_METODO_CLASIFICAR='clasificar_img'

    URL_POST_METODO_PASO_GRAY_WORD = 'clasificar_img_GRAY_WORD'
    URL_POST_METODO_PASO_BOUNDING_BOX = 'clasificar_img_BOUNDING_BOX'
    URL_POST_METODO_PASO_MRESIZE = 'clasificar_img_MRESIZE'
    URL_POST_METODO_PASO_CIELAB = 'clasificar_img_CIELAB'
    URL_POST_METODO_PASO_PREDICCION = 'clasificar_img_PREDICCION'

    URL_POST_METODO_COMENZAR_ENTRENAMIENTO = 'comenzar_entrenamiento'
    URL_POST_METODO_DETENER_ENTRENAMIENTO = 'detener_entrenamiento'
    URL_POST_GET_ESTADO_ENTRENAMIENTO = 'get_estado_entrenamiento'

    URL_POST_SUBIR_ARCHIVO='suvir_archivo'
    URL_POST_METODO_DETENER_UPLOAD_DATASET="detener_upload_dataset"
    URL_POST_METODO_DETENER_DESCOMPRESION_DATASET = "detener_descompresion_dataset"
    URL_POST_METODO_GET_ESTADO_VISTA_ENTRADA_DATASET = "get_estado_vista_entrada_dataset"
    URL_POST_METODO_ELIMINAR_DATASET_SUBIDO="eliminar_dataset_subido"
    URL_POST_METODO_INTENTAR_COMENZAR_PROCESO_AGREGAR_DATASET="intentar_comenzar_proceso_agregar_dataset"
    URL_POST_METODO_DETENER_PROCESAMIENTO_DE_IMAGENES="detener_procesamiento_de_imagenes"
    URL_POST_METODO_ELIMINAR_DATASET="eliminar_dataset"
    URL_POST_METODO_GET_IMG_DE_EJEMPLO_50_PX="get_imagen_de_ejemplo_50px"
    URL_POST_METODO_GET_IMG_DE_EJEMPLO_900_600_PX = "get_imagen_de_ejemplo_900_600px"
    URL_POST_METODO_GET_LISTA_IMAGENES_DEL_DATASET="get_lista_imagenes_del_dataset"
    URL_POST_METODO_GET_IMG_DATASET_900_600_PX="get_imagen_de_dataset_900_600px"
    URL_POST_METODO_GET_DETALLES_DEL_DATASET = "get_detalles_del_dataset"
    URL_POST_METODO_RESETEAR_ESTADOS_AGREGAR_DATASET="get_resetear_estados_agregar_dataset"
    URL_POST_METODO_ELIMINAR_MODELO_NUERONAL = "eliminar_modelo_neuronal"
    URL_POST_METODO_INTENTAR_AGREGAR_USUARIO="intentar_agregar_usuario"
    URL_POST_METODO_INTENTAR_CAMBIAR_CONTRASENA = "intentar_cambiar_contrasena"
    URL_POST_METODO_INTENTAR_ELIMINAR_USUARIO = "intentar_eliminar_usuario"
    URL_POST_METODO_INTENTAR_EDITAR_USUARIO = "intentar_editar_usuario"
    URL_POST_METODO_INTENTAR_EDITAR_DATASET = "intentar_editar_dataset"
    URL_POST_METODO_INTENTAR_EDITAR_MODELO_NEURONAL = "intentar_editar_modelo_nuronal"
    URL_POST_METODO_INTENTAR_AGREGAR_TIPO_DE_FRUTO = "intentar_agregar_tipo_de_fruto"
    URL_POST_METODO_GET_IMG_DE_EJEMPLO_50_PX_FRUTO = "get_imagen_de_ejemplo_50px_fruto"
    URL_POST_METODO_GET_IMG_DE_EJEMPLO_900_900_PX_FRUTO = "get_imagen_de_ejemplo_900_900px_fruto"
    URL_POST_METODO_INTENTAR_ELIMINAR_FRUTO = "intentar_eliminar_fruto"
    URL_POST_METODO_INTENTAR_ELIMINAR_TODOS_LOS_FRUTO = "intentar_eliminar_todos_los_fruto"
    URL_POST_METODO_INTENTAR_ELIMINAR_TODOS_LOS_FRUTO_SELECCIONADOS = "intentar_eliminar_todos_los_fruto_seleccionados"
    URL_POST_METODO_INTENTAR_EDITAR_FRUTO = "intentar_editar_fruto"
    URL_POST_METODO_INTENTAR_ELIMINAR_TODOS_LOS_DATASETS = "intentar_eliminar_todos_los_datasets"
    URL_POST_METODO_INTENTAR_ELIMINAR_TODOS_LOS_DATASETS_SELECCIONADOS = "intentar_eliminar_todos_los_datasets_seleccionados"
    URL_POST_METODO_INTENTAR_ELIMINAR_TODOS_LOS_MODELOS_NEURONALES = "intentar_eliminar_todos_los_modelos_neuronales"
    URL_POST_METODO_INTENTAR_ELIMINAR_TODOS_LOS_MODELOS_NEURONALES_SELECCIONADOS = "intentar_eliminar_todos_los_modelos_neuronales_seleccionados"
    URL_POST_METODO_INTENTAR_ELIMINAR_TODOS_LOS_USUARIOS_SELECCIONADOS = "intentar_eliminar_todos_los_usuarios_seleccionados"

    URL_POST_METODO_GET_IMG_DE_FRUTO = "get_imagen_de_fruto"
    URL_POST_METODO_GET_IMG_ORIGINAL_DEL_CLASIFICACION = "get_imagen_original_de_clasificacion"

    URL_POST_METODO_ALMACENAR_ID_DATASET_EDITAR="llamar_a_alamacenar_id_dataset"


class Constantes_Valores_Radio(Nombre_Input_Constants):
    FRUTO = 'radio_fruto'
    MODELO = 'radio_modelo'
    FECHA = 'radio_fecha'
    CLASIFICACION = 'radio_clasificacion'
    TODO = 'radio_todo'
    # PORCENTAJE_DE_VALIDACION = "valor_radio_porcentaje_de_validacion"
    # DATASET_PARA_VALIDACION = "valor_radio_dataset_para_validacion"


class Constantes_Nombre_Form(Nombre_Form_Constants):
    DETALLES_AL_CLASIFICAR = 'nombre_formulario_detalles_resultado'
    DETALLES_LISTA_DE_CLASIFICACIONES_USUARIO = "nombre_formulario_detalles_lista_clasifcaciones_usuarios"
    DELETE_CLASIFICAION_LISTA_DE_CLASIFICACIONES_USUARIO = "nombre_formulario_delete_lista_clasifcaciones_usuarios"
    FILTRO = 'nombre_formulario_filtro'

    TERMINO_EL_ENTRENAMIENTO = 'nombre_termino_el_entrenamiento'
    COMENZAR_ENTRENAMIENTO = 'nombre_comenzar_entrenamiento'
    DETENER_ENTRENAMIENTO = 'nombre_detener_entrenamiento'
    GUARDAR_MODELO = "nombre_formulario_guardar_modelo"
    CANCELAR_MODELO = "nombre_formulario_cancelar_modelo"
    TERMINO_DE_CLASIFICAR = 'nombre_formulario_termino_de_clasificar'
    CLASIFICAR_IMAGEN="nombre_formulario_clasificar_imagen"


class Constantes_Nombre_Input(Nombre_Input_Constants):
    ID_CLASIFICACION = "diClasificacionActual"
    SELECT_FRUTO = 'select_fruto'
    SELECT_MODELO = 'select_modelo'
    RADIO_FILTRO = 'radio_filtro'
    TEXT_FILTRO = 'text_filtro'

    #ID_DATASET = "nombre_input_id_dataset"
    ID_DATASET_PARA_VALIDACION = "nombre_input_id_dataset_para_validacion"
    #NOMBRE_DEL_MODELO = "nombre_input_nombre_del_modelo"
    #TIPO_DE_FRUTO = "nombre_input_tipo_de_fruto"
    DESCRIPCION = "nombre_input_descripcion"
    #CANTIDAD_DE_EPOCAS = "nombre_input_cantidad_de_epocas"
    TIPO_DE_VALIDACION = "nombre_input_tipo_de_validacion"
    #PORCENTAJE_DE_VALIDACION = "nombre_input_porcentaje_de_validacion"
    #USAR_LIMITE_DE_PRECISION = "nombre_input_usar_limite_de_precision"
    #LIMITE_DE_PRECISION = "nombre_input_limite_de_precision"

class Constantes_Str():
    PERMISO_ADMIN = 'ADMIN'
    PERMISO_INVESTIGADOR = 'INVESTIGADOR'
    PERMISO_USUARIO = 'USUARIO'
    NOMBRE_USUARIO_ANONIMO="USUARIO_ANONIMO"
    NOMBRE_IP_ANONIMO = "IP_ANONIMO"

    KEY_ID_ULTIMO_FRUTO_AGREGADO="KEY_ID_ULTIMO_FRUTO_AGREGADO"
    KEY_ULTIMA_URL_AGREGAR_FRUTO_EXTERNO="KEY_ULTIMA_URL_AGREGAR_FRUTO_EXTERNO"
    KEY_ID_ULTIMO_DATASET_A_EDITAR = "KEY_ID_ULTIMO_DATASET_A_EDITAR"




APP_CNF=AppDjImpl(base_dir=BASE_DIR
            ,nombre_app="Aplicacion"
              ,carpeta_static="static"
              ,carpeta_img_tem="img/temp"
                ,carpeta_archivos_temporales="archivosTemp/temp"
                  #,nombre_form_ubicacion_post='enviadoPorFormulario'
                  ,urls=UrlsApp()
                  ,urlHome=UrlsApp().URL_VISTA_CLASIFICAR_IMAGEN#UrlsApp().URL_VISTA_CLASIFICAR_IMAGEN
                  ,nombre_Form_Constants=Constantes_Nombre_Form()
                  ,nombre_Input_Constants=Constantes_Nombre_Input()
                  ,valor_Radio_Constants=Constantes_Valores_Radio()
                  ,consts=Constantes_Str()
                  )#,metodoOpen=open2
#dm=APP_CNF.datos_en_memoria

KEY_RESULTADO_CLASIFICAR="resultado"
KEY_ID_PROCESAMIENTO_DE_IMAGEN="procesamiento_de_imagen"
KEY_ID_CLASIFICACION="clasificacion"
#KEY_INDICE_PAGINACION="paginacionKey"
KEY_APLICAR_FILTRO="aplicarfiltro"
KEY_NOMBRE_IMAGEN="key_nombre_imagen"
KEY_NOMBRE_MODELO="key_nombre_modelo"
KEY_DATOS_RESPUESTA="key_datos_respuesta"

KEY_CONFIGURACION="key_configuracion"
KEY_DATOS_EN_MEMORIA_DE_ENTRENAMIENTO="datos_en_memoria_de_entrenamiento"
KEY_DATOS_EN_MEMORIA_DE_UPLOAD_DATASET="datos_en_memoria_de_upload_dataset"

KEY_RADIO_FILTRO = 'key_radio_filtro'
KEY_TEXT_FILTRO = 'key_text_filtro'

KEY_RESULTADO='key_resultado'

KEY_IMG_GRAY_WORD ='datosDeImagenGrayWorld'
KEY_IMG_BOUNDING_BOX='datosDeImagenBoundingBox'
KEY_IMG_M_RESIZE='datosDeImagenMResize'
KEY_IMG_ORIGINAL="datosDeImagenOriginal"
KEY_IMG_CIEL_AB="datosDeImagenCielAB"
KEY_FORMATO="formato"
KEY_STR_DATE="strDate"

NOMBRE_IMG_TEMP_ORIGINAL = "ImagenOriginalTemp"
NOMBRE_IMG_ALGORITMO_GRAY_WORD = "GrayWorld"
NOMBRE_IMG_ALGORITMO_BOUNDING_BOX = "BoundingBox"
NOMBRE_IMG_ALGORITMO_M_RESIZE = "MResize"
NOMBRE_IMG_ALGORITMO_CIEL_AB = "CielAB"

NOMBRE_ALGORITMO_GRAY_WORD = "GrayWorld"
NOMBRE_ALGORITMO_BOUNDING_BOX = "BoundingBox"
NOMBRE_ALGORITMO_M_RESIZE = "MResize"
NOMBRE_ALGORITMO_CIEL_AB = "CielAB"


LP_APLICACION="Aplicación"
LP_INVESTIGACION="Investigación"
LP_ADMINSITRACION="Administración"
LP_GESTION="Gestión"