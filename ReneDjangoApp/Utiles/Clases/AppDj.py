from ReneDjangoApp.Utiles.Clases.URL_Constants import URL_Constants
from ReneDjangoApp.Utiles.Clases.DatosFormularioLoguin import DatosFormularioLoguin
from ReneDjangoApp.Utiles.Clases.ClasesDeConstantes import *
class AppDj:
    def __init__(self
                 ,base_dir
                 ,nombre_app
                 ,carpeta_static
                 ,carpeta_img_tem
                 ,carpeta_archivos_temporales


                 ,urls:URL_Constants
                 ,urlHome
                 ,datos_formulario_loguin=None
                 , loguin_redirect=None
                 ,nombre_Form_Constants=None
                 , nombre_Input_Constants=None
                 , valor_Radio_Constants=None

                 ,consts=None
                 ):
        #,nombre_form_ubicacion_post
        if nombre_Form_Constants is None:
            nombre_Form_Constants=Nombre_Form_Constants()
        if nombre_Input_Constants is None:
            nombre_Input_Constants=Nombre_Input_Constants()
        if valor_Radio_Constants is None:
            valor_Radio_Constants=Valor_Radio_Constants()

        self.forms=nombre_Form_Constants
        self.inputs=nombre_Input_Constants
        self.radios=valor_Radio_Constants

        self.nombre_app=nombre_app
        self.carpeta_static=carpeta_static
        self.carpeta_img_tem=carpeta_img_tem

        self.nombre_form_ubicacion_post =nombre_Input_Constants.UBICACION_POST

        self.base_dir=base_dir
        self.urls:URL_Constants=urls
        self.urlHome=urlHome

        self.carpeta_archivos_temporales=carpeta_archivos_temporales

        if loguin_redirect is None:
            loguin_redirect="/"+urls.URL_VISTA_LOGUIN+"/"
        self.loguin_redirect = loguin_redirect
        #print("self.loguin_redirect=",self.loguin_redirect)
        if datos_formulario_loguin is None:
            datos_formulario_loguin=DatosFormularioLoguin()
            datos_formulario_loguin.url_loguin=urls.URL_VISTA_LOGUIN
        self.datos_formulario_loguin:DatosFormularioLoguin=datos_formulario_loguin
        self.datos_en_memoria=None#DatosEnMemoria()
        self.metodoAlDesloguearse=None
        self.metodoAlLoguearse = None

        self.consts=consts
        #self.metodoOpen=metodoOpen
    def getRutaCarpetaImg(self)->str:
        return self.nombre_app+"/"+self.carpeta_static+"/"+self.carpeta_img_tem

    def getRutaCarpeta_archivos_temporales(self)->str:
        return self.nombre_app+"/"+self.carpeta_static+"/"+self.carpeta_archivos_temporales

    def getRutaImgTem(self,nombreImg):
        return self.carpeta_img_tem+"/"+nombreImg

    def getRuta_archivo_temporal(self,nombreImg):
        return self.carpeta_archivos_temporales+"/"+nombreImg

    def alDesloguearse(self,request):
        if self.metodoAlDesloguearse is not None:
            self.metodoAlDesloguearse(request)
    def alLoguearse(self,request):
        if self.metodoAlLoguearse is not None:
            self.metodoAlLoguearse(request)


