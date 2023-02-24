from django.http import  JsonResponse
from ReneDjangoApp.Utiles.Clases.File import File
class DatosDeFileDj:
    def __init__(self):
        self.existingPath = None
        self.eof = None
        self.name = ""
        self.porcientoActual=0

    def eliminar(self):
        f = File(self.existingPath)

        try:
            print("str f=", str(f))
            print("f.existe()=", f.existe())
            if f.existe():
                f.delete()
                print("lo elimino")
        except:
            print("error al intentar elminar a ",f)
        return self

class GestorDeDatosUpload:
    def __init__(self):
        self.datoActual=None
    def guardarDatosDeFileDj(self,request,datosDeFileDj):#tiene que actualizar si ya existe
        self.datoActual=datosDeFileDj
        #print("lo guardo self.datoActual=",self.datoActual)
    def cargarDatosDeFileDj(self,request,existingPath)->DatosDeFileDj:
        #print("va a cargarlo self.datoActual=",self.datoActual)
        return self.datoActual

class UploadManager:
    KEY_DATA = 'data'
    KEY_EXISTING_PATH = 'existingPath'
    KEY_TERMINO_CON_ERROR="termino_con_error"
    def __init__(self):
        self.gestorDeDatos:GestorDeDatosUpload=GestorDeDatosUpload()

        #self.nameInputFile=None
        self.key_name_file='file'
        self.key_name_filename='filename'
        self.key_name_existingPath = 'existingPath'
        self.key_name_end = 'end'
        self.key_name_nextSlice = 'nextSlice'




        self.key_name_porciento_actual='porciento'

        self.mensaje_si_es_un_pedido_invalido='Invalid Request'
        self.mensaje_si_termino_con_exito = 'Uploaded Successfully'
        self.mensaje_pedido_invalido='EOF found. Invalid request'
        self.mensaje_no_encontro_la_direccion='No such file exists in the existingPath'

        self.metodoGetUrlSalidaArchivo=lambda r,s,fileName:'media/' + fileName#(reques,UploadManager,nombreDeArchivo)->str
        self.metodoAlAvanzar=None#(reques,UploadManager,DatosDeFileDj)->{}  lambda r,s,DatosDeFileDj:
        self.metodoAlTerminarConExito=None#(reques,UploadManager,DatosDeFileDj)->{}
        #self.metodoAlNoEncontrarLaDireccion=None#(reques,UploadManager,DatosDeFileDj,mensaje)->{}
        self.metodoAlDarError=None#(reques,UploadManager,mensaje)->{}
        #deveria de aqui usar a media/   #Tener en cuenta que este metodo puede que se llame mas de una ves

        self.ya_termino_con_exito=False
        self.metodoAlComenzarADetener=None#(reques,UploadManager,DatosDeFileDj)->{}
        self.metodoAlTerminarDeDetener=None#(reques,UploadManager,DatosDeFileDj)->{}

        self.mensaje_fue_mandado_a_detener = 'mensaje_fue_mandado_a_detener'

        #self.detener_upload=False
        self.condicionDetenerUpload=lambda r,uploadoManager:False
        self.yaDetuvoElUpload=False

        self.ultimaDireccion=None

    def alDarError(self,request,mensaje):
        if self.metodoAlDarError is not None:
            self.metodoAlDarError(request,self,mensaje)
    # def alNoEncontrarLaDireccion(self,request,datosDeFileDj:DatosDeFileDj,mensaje):
    #     if self.metodoAlNoEncontrarLaDireccion is not None:
    #         self.metodoAlNoEncontrarLaDireccion(request,self,datosDeFileDj,mensaje)
    def alDetenerUpload(self,request,datosDeFileDj:DatosDeFileDj):
        if self.metodoAlComenzarADetener is not None:
            self.metodoAlComenzarADetener(request,self,datosDeFileDj)
        #print("Va a comenzar a detener!!!!!!!!!!!!!!!!!!!!!!!!!")
        datosDeFileDj.eliminar()
        # f=File(datosDeFileDj.existingPath)
        # print("str f=",str(f))
        # print("f.existe()=",f.existe())
        # if f.existe():
        #     f.delete()
        #     print("lo elimino")
        if self.metodoAlTerminarDeDetener is not None:
            self.metodoAlTerminarDeDetener(request,self,datosDeFileDj)
        self.yaDetuvoElUpload=True


    def getUrlSalidaArchivo(self,request,nombreDeArchivo):
        return self.metodoGetUrlSalidaArchivo(request,self,nombreDeArchivo)
    def alTerminarConExito(self,request,datosDeFileDj:DatosDeFileDj):
        #Tener en cuenta que este metodo puede que se llame mas de una ves
        if self.metodoAlTerminarConExito is not None:
            self.metodoAlTerminarConExito(request,self,datosDeFileDj)
        self.ya_termino_con_exito = True
    def alAvanzar(self,request,datosDeFileDj:DatosDeFileDj):
        if self.metodoAlAvanzar is not None:
            self.metodoAlAvanzar(request,self,datosDeFileDj)


    def uploadIfPost(self,request):
        if request.method == 'POST':
            return self.upload(request)
        res = JsonResponse({UploadManager.KEY_DATA: self.mensaje_pedido_invalido})
        return res
    def __upload(self,request):


        file = request.FILES[self.key_name_file].read()
        fileName = request.POST[self.key_name_filename]
        existingPath = request.POST[self.key_name_existingPath]
        end = request.POST[self.key_name_end]
        nextSlice = request.POST[self.key_name_nextSlice]



        if file == "" or fileName == "" or existingPath == "" or end == "" or nextSlice == "":
            self.alDarError(request,self.mensaje_si_es_un_pedido_invalido)
            res = JsonResponse({UploadManager.KEY_DATA: self.mensaje_si_es_un_pedido_invalido
                                ,UploadManager.KEY_TERMINO_CON_ERROR:True})
            print("error 0 en proceso de suvida")

            return res
        else:
            if existingPath == 'null':

                self.ya_termino_con_exito=False

                path = self.getUrlSalidaArchivo(request,fileName)#'media/' + fileName
                with open(path, 'wb+') as destination:
                    destination.write(file)
                FileFolder = DatosDeFileDj()
                FileFolder.existingPath =path #fileName
                FileFolder.eof = end
                FileFolder.name = fileName

                self.gestorDeDatos.guardarDatosDeFileDj(request, FileFolder)
                self.ultimaDireccion=FileFolder.existingPath
                if self.condicionDetenerUpload(request,self):#self.detener_upload:
                    #print("va a detener!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    self.alDetenerUpload(request,FileFolder)
                    res = JsonResponse({UploadManager.KEY_DATA: self.mensaje_fue_mandado_a_detener
                                ,UploadManager.KEY_TERMINO_CON_ERROR:False})

                else:

                    #self.gestorDeDatos.guardarDatosDeFileDj(request, FileFolder)
                    if int(end):
                        print("suvida: termino anticipado")
                        self.alTerminarConExito(request,FileFolder)
                        #res = JsonResponse({KEY_DATA:self.mensaje_si_termino_con_exito ,KEY_EXISTING_PATH : fileName})
                        res = JsonResponse({UploadManager.KEY_DATA: self.mensaje_si_termino_con_exito, UploadManager.KEY_EXISTING_PATH: path
                                ,UploadManager.KEY_TERMINO_CON_ERROR:False})
                    else:
                        print("suvida: va a continuar")
                        #res = JsonResponse({KEY_EXISTING_PATH: fileName})

                        res = JsonResponse({UploadManager.KEY_EXISTING_PATH: path
                                ,UploadManager.KEY_TERMINO_CON_ERROR:False})
                return res
            else:

                path = self.getUrlSalidaArchivo(request,fileName)#'media/' + existingPath
                self.ultimaDireccion = path
                #model_id = File.objects.get(existingPath=existingPath)
                model_id:DatosDeFileDj=self.gestorDeDatos.cargarDatosDeFileDj(request,existingPath=existingPath)

                if model_id.name == fileName:
                    if not int(model_id.eof):
                        if self.condicionDetenerUpload(request,self):#if self.detener_upload:
                            #print("1 va a detener!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                            self.alDetenerUpload(request, model_id)
                            res = JsonResponse({UploadManager.KEY_DATA: self.mensaje_fue_mandado_a_detener
                                ,UploadManager.KEY_TERMINO_CON_ERROR:False})

                        else:

                            model_id.porcientoActual=int(request.POST[self.key_name_porciento_actual])
                            self.alAvanzar(request,model_id)


                            with open(path, 'ab+') as destination:
                                destination.write(file)

                            if int(end):
                                print("suvida: termino completo")
                                model_id.eof = int(end)
                                self.gestorDeDatos.guardarDatosDeFileDj(request, model_id)
                                self.alTerminarConExito(request, model_id)
                                res = JsonResponse({UploadManager.KEY_DATA: self.mensaje_si_termino_con_exito
                                                       , UploadManager.KEY_EXISTING_PATH: model_id.existingPath
                                ,UploadManager.KEY_TERMINO_CON_ERROR:False})
                            else:
                                print("suvida: continua2")
                                res = JsonResponse({UploadManager.KEY_EXISTING_PATH: model_id.existingPath
                                ,UploadManager.KEY_TERMINO_CON_ERROR:False})
                        return res
                    else:
                        print("error 1 en proceso de suvida")
                        self.alDarError(request, self.mensaje_pedido_invalido)
                        res = JsonResponse({UploadManager.KEY_DATA: self.mensaje_pedido_invalido
                                ,UploadManager.KEY_TERMINO_CON_ERROR:True})
                        return res
                else:
                    #self.alNoEncontrarLaDireccion(request,model_id,self.mensaje_no_encontro_la_direccion)
                    print("error 2 en proceso de suvida")
                    self.alDarError(request, self.mensaje_no_encontro_la_direccion)
                    res = JsonResponse({UploadManager.KEY_DATA: self.mensaje_no_encontro_la_direccion
                                ,UploadManager.KEY_TERMINO_CON_ERROR:True})
                    return res
        print("error 3 en proceso de suvida")
        self.alDarError(request, self.mensaje_pedido_invalido)
        res = JsonResponse({UploadManager.KEY_DATA: self.mensaje_pedido_invalido
                                ,UploadManager.KEY_TERMINO_CON_ERROR:True})
        return res

    def upload(self, request):
        res=self.__upload(request)
        if  self.condicionDetenerUpload(request,self) and not self.yaDetuvoElUpload:
            existingPath = self.ultimaDireccion
            if existingPath is not None and existingPath != "" :
                model_id: DatosDeFileDj = self.gestorDeDatos.cargarDatosDeFileDj(request, existingPath=existingPath)
                if model_id is not None:
                    #print("Lo elimino por aqui !!!!!!!!!!!!")
                    self.alDetenerUpload(request,model_id)
                    res = JsonResponse({UploadManager.KEY_DATA: self.mensaje_fue_mandado_a_detener
                                           , UploadManager.KEY_TERMINO_CON_ERROR: False})
                    #model_id.eliminar()
        return res
