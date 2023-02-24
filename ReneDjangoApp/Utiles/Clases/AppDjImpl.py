from ReneDjangoApp.Utiles.Clases.AppDj import AppDj
from ReneDjangoApp.Utiles.MetodosUtiles.UtilesDjango import isPost,crearImgTempDj,DatosDeImagenTempDj,getNombreImagenTemp_Aleatorios,crearDatosDeImagenTempDj,setTiempoDeExpiracionDeSession,pathR_Logout,pathR_Admin,pathR_loguin,getDatosDeImagenTempDj_DeNombre,deleteCampoImg,DatosDeArchivo_DesdeUploadDj,crearArchivo_DesdeUpload_Dj
from django.shortcuts import render
from ReneDjangoApp.Utiles.Clases.DatosPaginacion import PaginacionDeSession
from ReneDjangoApp.Utiles.Clases.URL_Constants import URL_Constants
from ReneDjangoApp.Utiles.Clases.DatosEnMemoria import DatosEnMemoria
import os

class AppDjImpl(AppDj):
    def __init__(self,base_dir
                 ,nombre_app
                 ,carpeta_static
                 ,carpeta_img_tem
                 , carpeta_archivos_temporales

                 #,nombre_form_ubicacion_post
                 ,urls:URL_Constants
                 ,urlHome
                 ,datos_formulario_loguin=None
                 , loguin_redirect=None

                 , nombre_Form_Constants=None
                 , nombre_Input_Constants=None
                 , valor_Radio_Constants=None
                 , consts=None
                 ):
        AppDj.__init__(self,base_dir=base_dir
                       ,nombre_app=nombre_app
                       ,carpeta_static=carpeta_static
                       ,carpeta_img_tem=carpeta_img_tem
                       ,carpeta_archivos_temporales=carpeta_archivos_temporales
                       #,nombre_form_ubicacion_post=nombre_form_ubicacion_post
                       ,urls=urls
                       ,urlHome=urlHome
                       ,datos_formulario_loguin=datos_formulario_loguin
                       ,loguin_redirect=loguin_redirect

                       , nombre_Form_Constants=nombre_Form_Constants
                       , nombre_Input_Constants=nombre_Input_Constants
                       , valor_Radio_Constants=valor_Radio_Constants
                       ,consts=consts
                       )
        self.datos_en_memoria=DatosEnMemoria()
    def isPost(self,request,nombreformularioActualPost)->bool:
        return isPost(request,self,nombreformularioActualPost)

    def crearImgTempDj(self,request, nombrePostFileImagen, nombreImg, extencion=None) -> DatosDeImagenTempDj:
        return crearImgTempDj(request,self,nombrePostFileImagen, nombreImg, extencion)

    def crearArchivo_DesdeUpload(self,request, nombrePostFileImagen, nombreArchivo)->DatosDeArchivo_DesdeUploadDj:
        return crearArchivo_DesdeUpload_Dj(request, self, nombrePostFileImagen, nombreArchivo)

    def getDireccionRelativa_DeCampoImagen(self,campoImg):
        return self.getDatosDeImagenTempDj_DeNombre(
            os.path.basename(str(campoImg))).url_relativa_carpeta_static
    def getDatosDeImagenTempDj_DeNombre(self,nombreImg):
        return getDatosDeImagenTempDj_DeNombre(self,nombreImg)
    def getDatosDeImagenTempDj(self,request,nombreImg,extencion=None)->DatosDeImagenTempDj:
        # img=DatosDeImagenTempDj()
        # img.nombre = getNombreImagenTemp(request, nombreImg, extencion)
        # img.url_relativa_completa=self.getRutaCarpetaImg() + "/" +img.nombre
        # img.url_relativa_carpeta_static=self.getRutaImgTem(img.nombre)
        # return img
        return crearDatosDeImagenTempDj(request,self,nombreImg,extencion)

    def getDic(self,dic,loc=None):

        default = {'nombre_form_ubicacion_post': self.nombre_form_ubicacion_post
            , 'urls': self.urls
                   ,'idIndiceDePaginacion':PaginacionDeSession.KEY_INDICE_PAGINACION
            , 'valor_paginacion_anterior': PaginacionDeSession.VALOR_PAGINACION_ANTERIOR
            , 'valor_paginacion_siguiente': PaginacionDeSession.VALOR_PAGINACION_SIGUIENTE
            , 'formuarioPaginacion': PaginacionDeSession.NOMBRE_FORM_PAGINACION
           ,'forms':self.forms
            , 'inputs': self.inputs
            , 'radios': self.radios
                   ,'consts':self.consts

                   }
        if loc is not None:
            default['localizacionDePagina']=loc
        if dic is not None:
            for k in dic.keys():
                default[k] = dic[k]
        return default

    def renderApp(self,request, template, dic=None,loc=None):
        setTiempoDeExpiracionDeSession(request)
        return render(request, template, self.getDic(dic,loc))
    def pathR_Logout(self,url=None):
        if url is None:
            url=self.urls.URL_VISTA_DESLOGUEARSE
        return pathR_Logout(url,self)

    def pathR_Admin(self, url=None):
        if url is None:
            url = self.urls.URL_VISTA_ADMINISTRACION
        return pathR_Admin(url)
    def pathR_loguin(self, plantilla):
        return pathR_loguin(plantilla,self)
    def detURL_Completa_CampoImagen(self,img):
        url = self.getDatosDeImagenTempDj_DeNombre(
            os.path.basename(str(img))).url_relativa_completa
        return url

    def deleteCampoImg(self,img):
        url=self.getDatosDeImagenTempDj_DeNombre(
            os.path.basename(str(img))).url_relativa_completa
        deleteCampoImg(url)

    def addMetodoAlDesloguearse(self,metodo):
        if self.metodoAlDesloguearse is not None:
            anterior=self.metodoAlDesloguearse
            def nuevo(r):
                anterior(r)
                metodo(r)

            self.metodoAlDesloguearse=nuevo
        else:
            self.metodoAlDesloguearse = metodo

    def addMetodoAlLoguearse(self,metodo):
        if self.metodoAlLoguearse is not None:
            anterior=self.metodoAlLoguearse
            def nuevo(r):
                anterior(r)
                metodo(r)

            self.metodoAlLoguearse=nuevo
        else:
            self.metodoAlLoguearse = metodo