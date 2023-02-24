from ReneDjangoApp.Utiles.Clases.Validacion.TiposDeValidacion import *
from ReneDjangoApp.Utiles.MetodosUtiles.UtilesDjango import getPost,getPostFloat,getPostBool,getPostInt
from ReneDjangoApp.Utiles.MetodosUtiles.MetodosBasicos import *
class CampoConValidacion:
    def __init__(self,valorPorDefecto=None):
        self.mensaje=""
        self.esValido=True
        self.valor=valorPorDefecto
        self.listaTiposDeValidacion=[]
        self.condicionDeEvaluacion=lambda :True
        self.nombreVariable=None


        def metodoGetNombreDefault(campo,valor):
            lista = separadorDePalabrasEnTextoUnido(self.nombreVariable)
            lista = [p.title() for p in lista]
            nombre=""
            for p in lista:
                if len(nombre)>0:
                    nombre+=" "
                nombre+=p
            return nombre

        self.__metodoGetNombre=metodoGetNombreDefault

        def metodoGetMensajeDeIdentifiacionDeCampoDefault(campo,nombre,valor):
            return 'El campo "'+self.getNombre()+'": '


        self.__metodoGetMensajeDeIdentificacionDeCampo=metodoGetMensajeDeIdentifiacionDeCampoDefault
        #self.mensajeDeIdentificacionDeCampo=None
        #self.metodoValidar=lambda v=
    def setNombre(self,nombreOMetodo):
        """
        :param nombreOMetodo: str o (campo,valor)->str
        :return:
        """
        if esString(nombreOMetodo):
            self.__metodoGetNombre=lambda campo,valor:nombreOMetodo
        else:
            self.__metodoGetNombre=nombreOMetodo
        return self
    def getNombre(self):
        return self.__metodoGetNombre(self,self.valor)

    def setMensajeDeIdentifiacionDeCampoDefault(self,mensajeOMetodo):
        """

        :param mensajeOMetodo: str o (campo,nombre,valor)->str
        :return:
        """
        if esString(mensajeOMetodo):
            self.__metodoGetMensajeDeIdentificacionDeCampo=lambda campo,nombre,valor:mensajeOMetodo
        else:
            self.__metodoGetMensajeDeIdentificacionDeCampo=mensajeOMetodo
        return self
    def getMensajeDeIdentifiacionDeCampoDefault(self):
        return self.__metodoGetMensajeDeIdentificacionDeCampo(self,self.getNombre(),self.valor)
    def comprovarValidacion(self):
        for t in self.listaTiposDeValidacion:
            if not t.esValido(self.valor):
                self.esValido =False
                self.mensaje=t.getMensaje()
                return False
        self.esValido = True
        return True
    def addTipoDeValidacion(self,*a):
        leng=len(a)
        if leng>0:
            if esFuncion(a[0]):
                if esFuncion(a[1]):
                    m=a[1]
                else:
                    m=lambda: a[1]
                t=TipoDeValidacion(a[0],m)
                self.listaTiposDeValidacion.append(t)
            else:
                for t in a:
                    self.listaTiposDeValidacion.append(t)
        return self
    def setDependeDeCB(self,campoCB):#campoCB:CampoConValidacion
        self.condicionDeEvaluacion = lambda:campoCB.valor
        return self

    def setDependeDeCB_Not(self, campoCB):#campoCB:CampoConValidacion
        self.condicionDeEvaluacion = lambda: not campoCB.valor
        return self
    def setMaxCar(self,max):
        self.addTipoDeValidacion(TipoDeValidacionMaxLength(max,lambda v:"Debe de tener como máximo "+str(v)+" caracteres "))
        return self
    def setMinCar(self,min):
        self.addTipoDeValidacion(TipoDeValidacionMinLength(min,lambda v:"Debe de tener como mínimo "+str(v)+" caracteres "))
        return self


class CampoConValidacionRequest(CampoConValidacion):
    def __init__(self,*a,valorPorDefecto=None):
        if valorPorDefecto is None:
            valorPorDefecto=""
        CampoConValidacion.__init__(self,valorPorDefecto=valorPorDefecto)
        leng=len(a)
        if leng>0:
            self.name=a[0]
        else:
            self.name =None

    def actualizarValor(self,request):
        pass
    def __str__(self):
        return self.name

class CampoConValidacionPost(CampoConValidacionRequest):
    def __init__(self,*a,valorPorDefecto=None):
        CampoConValidacionRequest.__init__(self,valorPorDefecto=valorPorDefecto)
    def actualizarValor(self,request):
        self.valor=getPost(request,self.name)


class CampoCB_Validacion(CampoConValidacionPost):
    def __init__(self,*a,valorPorDefecto=None):
        if valorPorDefecto is None:
            valorPorDefecto=False
        CampoConValidacionPost.__init__(self,*a,valorPorDefecto=valorPorDefecto)

    def actualizarValor(self,request):
        self.valor=getPostBool(request,self.name)



class CampoRB_Validacion(CampoConValidacionPost):
    def __init__(self,nameRadio,*a,valorPorDefecto=None):
        if valorPorDefecto is None:
            valorPorDefecto=False
        CampoConValidacionPost.__init__(self,*a,valorPorDefecto=valorPorDefecto)
        #self.valorPropio=valorPropio valorPropio
        self.nameRadio=nameRadio
    def actualizarValor(self,request):
        self.valor=getPost(request,self.nameRadio)==self.name


class CampoConAlfanumericos_Validacion(CampoConValidacionPost):
    def __init__(self,*a,valorPorDefecto=None):
        CampoConValidacionPost.__init__(self,*a,valorPorDefecto=valorPorDefecto)
        self.addTipoDeValidacion(TipoDeValidacion.STR_CON_ALFANUMERICOS)

class CampoNoEmpty_Validacion(CampoConValidacionPost):
    def __init__(self,*a,valorPorDefecto=None):
        CampoConValidacionPost.__init__(self,*a,valorPorDefecto=valorPorDefecto)
        self.addTipoDeValidacion(TipoDeValidacion.STR_NO_EMPTY)
class CampoPositivo_Validacion(CampoConValidacionPost):
    def __init__(self, *a,valorPorDefecto=None):
        if valorPorDefecto is None:
            valorPorDefecto=0
        CampoConValidacionPost.__init__(self,*a,valorPorDefecto=valorPorDefecto)
        self.addTipoDeValidacion(TipoDeValidacion.SOLO_INT_POSITIVO_STR)
    def actualizarValor(self,request):
        self.valor=getPostInt(request,self.name)
class CampoRangoPositivo_Validacion(CampoConValidacionPost):
    def __init__(self,min,max,*a,valorPorDefecto=None):
        if valorPorDefecto is None:
            valorPorDefecto=min
        CampoConValidacionPost.__init__(self,*a,valorPorDefecto=valorPorDefecto)
        self.addTipoDeValidacion(#TipoDeValidacion.SOLO_INT_POSITIVO_STR,
        TipoDeValidacionRangoPositivo(min,max,lambda vmin,vmax:"El numero debe de estar en el rango de "+str(vmin)+" a "+str(vmax)+" y debe ser un numero positivo cuyo indicador decimal sea un ‘.’"))
    def actualizarValor(self,request):
        # print("self.name=",self.name)
        # print("request.POST=",request.POST)
        self.valor=getPostFloat(request,self.name)


class CampoRangoEnteroPositivo_Validacion(CampoConValidacionPost):
    def __init__(self,min,max,*a,valorPorDefecto=None):
        if valorPorDefecto is None:
            valorPorDefecto=min
        CampoConValidacionPost.__init__(self,*a,valorPorDefecto=valorPorDefecto)
        self.addTipoDeValidacion(TipoDeValidacion.SOLO_INT_POSITIVO_STR
        ,TipoDeValidacionRangoEnteroPositivo(min,max,lambda vmin,vmax:"El numero debe de estar en el rango de "+str(vmin)+" a "+str(vmax)+" y debe ser un numero entero positivo "))
    def actualizarValor(self,request):
        self.valor=getPostInt(request,self.name)


class CampoCorreo_Validacion(CampoConValidacionPost):
    def __init__(self,*a,valorPorDefecto=None):
        CampoConValidacionPost.__init__(self,*a,valorPorDefecto=valorPorDefecto)
        self.addTipoDeValidacion(TipoDeValidacion.STR_CORREO)

class CampoSoloLetras_Validacion(CampoConValidacionPost):
    def __init__(self,*a,valorPorDefecto=None):
        CampoConValidacionPost.__init__(self,*a,valorPorDefecto=valorPorDefecto)
        self.addTipoDeValidacion(TipoDeValidacion.STR_SOLO_LETRAS)

class CampoSoloLetrasYNumeros_Validacion(CampoConValidacionPost):
    def __init__(self,*a,valorPorDefecto=None):
        CampoConValidacionPost.__init__(self,*a,valorPorDefecto=valorPorDefecto)
        self.addTipoDeValidacion(TipoDeValidacion.STR_SOLO_LETRAS_Y_NUMEROS)

class CampoSeguridadMinimaContraseña_Validacion(CampoConValidacionPost):
    def __init__(self,*a,valorPorDefecto=None):
        CampoConValidacionPost.__init__(self,*a,valorPorDefecto=valorPorDefecto)
        self.addTipoDeValidacion(TipoDeValidacion.STR_SEGURIDAD_MINIMA_CONTRASEÑA)


class CampoCoincidenteContraseña_Validacion(CampoConValidacionPost):
    def __init__(self,campoOriginal:CampoConValidacionPost,*a,valorPorDefecto=None):
        CampoConValidacionPost.__init__(self,*a,valorPorDefecto=valorPorDefecto)
        self.addTipoDeValidacion(TipoDeValidacion(lambda v:campoOriginal.valor==v
                                            ,lambda :"Tiene que coincidir con la contraseña"))


class CampoSelecionar_Validacion(CampoConValidacionPost):
    def __init__(self,listaValoresEntreLosQueSeleccionar,*a,valorPorDefecto=None):
        CampoConValidacionPost.__init__(self,*a,valorPorDefecto=valorPorDefecto)
        self.addTipoDeValidacion(TipoDeValidacion(lambda v: str(v) in listaValoresEntreLosQueSeleccionar
                                            ,lambda :"Tiene que coincidir con los valores de "+strLista(listaValoresEntreLosQueSeleccionar)))



class CampoDireccionImagen_Validacion(CampoConValidacionPost):
    def __init__(self,*a,valorPorDefecto=None):
        CampoConValidacionPost.__init__(self,*a,valorPorDefecto=valorPorDefecto)
        self.addTipoDeValidacion(TipoDeValidacion.STR_ES_DIRECCION_FORMATO_IMAGEN)

class CampoDireccionImagen_JPG_JPEG_PNG_Validacion(CampoConValidacionPost):
    def __init__(self,*a,valorPorDefecto=None):
        CampoConValidacionPost.__init__(self,*a,valorPorDefecto=valorPorDefecto)
        self.addTipoDeValidacion(TipoDeValidacion.STR_ES_DIRECCION_FORMATO_IMAGEN
                                 ,TipoDeValidacion.STR_ES_DIRECCION_FORMATO_IMAGEN_JPG_JPEG_PNG)



class ValorEnFile:
    VALIDACION_NO_EMPTY=TipoDeValidacion(lambda v: not v.isEmpty(),"El archivo no debe estar vacio")

    def __init__(self,key,byts,size):
        self.key=key
        self.byts=byts
        self.size=size
    def isEmpty(self):
        return self.size is None or self.size==0
    def getMgb(self):
        return (self.size/1024)/1024 if not self.isEmpty() else None
    def __str__(self):
        return self.key+" - size: "+str(+self.size)

class TipoDeValidacion_MenorQueCantidadDeMegas(TipoDeValidacion):
    def __init__(self,cantidadDeMegasMaximo):
        TipoDeValidacion.__init__(self,lambda v:v.getMgb()<cantidadDeMegasMaximo
                                  ,"El archivo debe de tener un tamaño inferior a los "
                                  +str(cantidadDeMegasMaximo)+" megas")

class CampoConValidacionFile(CampoConValidacionRequest):
    def __init__(self,*a,valorPorDefecto=None):
        if valorPorDefecto is None:
            valorPorDefecto=""
        CampoConValidacion.__init__(self,valorPorDefecto=valorPorDefecto)
        leng=len(a)
        if leng>0:
            self.name=a[0]
        else:
            self.name =None

    def actualizarValor(self,request):
        byts=request.FILES[self.name]
        self.valor=ValorEnFile(key=self.name
                               ,byts=byts
                               ,size=byts.size)
    def __str__(self):
        return self.name

class CampoConValidacionImagenJPG_JPEG_PNG(CampoConValidacionFile):
    def __init__(self,*a,valorPorDefecto=None):
        CampoConValidacion.__init__(self,valorPorDefecto=valorPorDefecto)
        self.addTipoDeValidacion(ValorEnFile.VALIDACION_NO_EMPTY
                                 , TipoDeValidacion_MenorQueCantidadDeMegas(10))
