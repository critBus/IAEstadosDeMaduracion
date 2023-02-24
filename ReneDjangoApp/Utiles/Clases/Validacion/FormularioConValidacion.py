from ReneDjangoApp.Utiles.Clases.Validacion.CamposConValidacion import CampoConValidacion,CampoConValidacionRequest
from ReneDjangoApp.Utiles.Clases.ClasesDeConstantes import Nombre_Input_Constants
from ReneDjangoApp.Utiles.MetodosUtiles.MetodosBasicos import *
class FormularioConValidacion:
    def __init__(self):
        self.submit=self.__class__.__name__
        self.valido=True
        self.validado=False
        self.inicializarCampos()
        self.inicializarNames()

        self.mensajeNoValido=""
    def inicializarCampos(self):
        pass
    def __str__(self):
        return self.submit
    def inicializarNames(self):
        d = vars(self)
        for n in d:
            c=d[n]
            if isinstance(c, CampoConValidacionRequest):
                c.name=self.__class__.__name__+"_"+n
                c.nombreVariable=n
                # print("c.name=",c.name)
    def getCamposConValidacion(self):
        d = vars(self)
        return [d[n] for n in d if isinstance(d[n], CampoConValidacionRequest)]
    def actualizarValoresPost(self,request):
        #print(request.POST)
        lista = self.getCamposConValidacion()
        for e in lista:
            if e.condicionDeEvaluacion():
                e.actualizarValor(request)
    def comprobarValidacion(self,request):
        self.actualizarValoresPost(request)
        return self.esValido()
    def esValido(self):

        self.validado =True
        lista=self.getCamposConValidacion()
        for e in lista:
            if e.condicionDeEvaluacion() and not e.comprovarValidacion():
                self.valido = False
                self.mensajeNoValido =e.getMensajeDeIdentifiacionDeCampoDefault()+ e.mensaje
                return False
        self.valido = True
        return True
    def verValoresDeCampos(self):
        for c in self.getCamposConValidacion():
            print(c,": ",c.valor)

    # def getMensajeNoValido(self):
    #     lista = self.getCamposConValidacion()
    #     for e in lista:
    #         if e.condicionDeEvaluacion():

    def htmlHidden(self):
        return '<input type="hidden" name="'+Nombre_Input_Constants.UBICACION_POST+'" value="'+self.submit+'">'

