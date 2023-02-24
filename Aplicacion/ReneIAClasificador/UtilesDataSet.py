#from RenePy.Utiles import *

from Aplicacion.ReneIAClasificador.AlgoritmosDeProcesamientoDeImagenes import *
from Aplicacion.ReneIAClasificador.comprobador_v1_0 import *
from Aplicacion.ReneIAClasificador.entrenador_v2_0 import *
#from RenePy.ClasesUtiles.File import File
from ReneDjangoApp.Utiles.Utiles import *
from ReneDjangoApp.Utiles.Clases.File import File
class ArgumentosDeEventosAlProcesarYcrearDataSet:
    def __init__(self,fOriginal:File,fDestino:File):
        self.fOriginal:File=fOriginal
        self.fDestino:File=fDestino
        self.nombreImagen=self.fOriginal.getName()
        self.nombreCarpetaPadre=self.fOriginal.getParentFile().getName()
        #self.esLaPrimeraImagenDeUnaCarpeta=False
        self.indiceDeCarpeta=0
        self.indiceDeImagenEnCarpeta=0
        self.indiceImagen=0
        self.porcientoDeImagenConRespectoAlTotal=0
        self.porcientoDeImagenConRespectoAlaCarpeta = 0
        self.porcientoDeCarpeta = 0

        self.cantidadTotalDeImagenes=0
        self.cantidadTotalDeImagenesEnEstaCarpeta=0

        self.indiceDeFaseDeImagen=0
        self.cantidadTotalDeFasesDeImagen=0
        self.progresoDeFasesDeImagen=0
        self.cantidadDeCarpetas=0
class EventosAlProcesarYcrearDataSet:
    def __init__(self,listaPar_NombreCarpeta_CantidadDeImagenes
                 ,antesDeComenzarAProcesarLaImagen
                 ,antesDeAplicar_grayWorld
                 ,antesDeAplicar_boundingBox
                 ,antesDeAplicar_mresize
                 ,antesDeAplicar_cielAB
                 ,alTerminarConExito):
        self.listaPar_NombreCarpeta_CantidadDeImagenes=listaPar_NombreCarpeta_CantidadDeImagenes
        self.cantidadTotalDeImagenes=0
        self.cantidadDeCarpetas=0
        for p in self.listaPar_NombreCarpeta_CantidadDeImagenes:
            self.cantidadTotalDeImagenes+=p[1]
            self.cantidadDeCarpetas+=1
        self.cantidadDeImagenesProcesadas=0
        self.cantidadDeCarpetasProcesadas=0
        self.cantidadDeImagenesProcesadasEnEstaCarpeta=0
        self.__antesDeComenzarAProcesarLaImagen=antesDeComenzarAProcesarLaImagen
        self.__antesDeAplicar_grayWorld= antesDeAplicar_grayWorld
        self.__antesDeAplicar_boundingBox = antesDeAplicar_boundingBox
        self.__antesDeAplicar_mresize = antesDeAplicar_mresize
        self.__antesDeAplicar_cielAB = antesDeAplicar_cielAB
        self.__alTerminarConExito=alTerminarConExito

        self.nombreCarpetaAnterior=None

        self.argsActual:ArgumentosDeEventosAlProcesarYcrearDataSet=None
    def antesDeComenzarAProcesarLaImagen(self,fOriginal:File,fDestino:File):
        args=ArgumentosDeEventosAlProcesarYcrearDataSet(fOriginal,fDestino)
        if self.nombreCarpetaAnterior is None:
            #self.esLaPrimeraImagenDeUnaCarpeta = True
            self.nombreCarpetaAnterior=args.nombreCarpetaPadre
        elif self.nombreCarpetaAnterior!=args.nombreCarpetaPadre:
                self.nombreCarpetaAnterior=args.nombreCarpetaPadre
                self.cantidadDeCarpetasProcesadas+=1
                self.cantidadDeImagenesProcesadasEnEstaCarpeta = 0

        args.indiceDeCarpeta=self.cantidadDeCarpetasProcesadas
        args.indiceDeImagenEnCarpeta=self.cantidadDeImagenesProcesadasEnEstaCarpeta
        args.indiceImagen=self.cantidadDeImagenesProcesadas

        self.cantidadDeImagenesProcesadasEnEstaCarpeta+=1
        self.cantidadDeImagenesProcesadas+=1

        args.cantidadTotalDeImagenes = self.cantidadTotalDeImagenes
        args.cantidadTotalDeImagenesEnEstaCarpeta=self.listaPar_NombreCarpeta_CantidadDeImagenes[args.indiceDeCarpeta][1]
        args.porcientoDeImagenConRespectoAlTotal=(args.indiceImagen/args.cantidadTotalDeImagenes)*100
        args.porcientoDeImagenConRespectoAlaCarpeta = (args.indiceDeImagenEnCarpeta /args.cantidadTotalDeImagenesEnEstaCarpeta ) * 100
        args.porcientoDeCarpeta = (args.indiceDeCarpeta / self.cantidadDeCarpetas) * 100

        args.indiceDeFaseDeImagen = 0
        args.cantidadTotalDeFasesDeImagen = 6
        args.progresoDeFasesDeImagen = 0
        args.cantidadDeCarpetas=self.cantidadDeCarpetas
        self.argsActual=args
        return self.__antesDeComenzarAProcesarLaImagen(self.argsActual)
    def antesDeAplicar_grayWorld(self):
        self.argsActual.indiceDeFaseDeImagen = 1
        self.argsActual.progresoDeFasesDeImagen = (self.argsActual.indiceDeFaseDeImagen/self.argsActual.cantidadTotalDeFasesDeImagen)*100
        return self.__antesDeAplicar_grayWorld(self.argsActual)
    def antesDeAplicar_boundingBox(self):
        self.argsActual.indiceDeFaseDeImagen = 2
        self.argsActual.progresoDeFasesDeImagen = (self.argsActual.indiceDeFaseDeImagen / self.argsActual.cantidadTotalDeFasesDeImagen) * 100
        return self.__antesDeAplicar_boundingBox(self.argsActual)
    def antesDeAplicar_mresize(self):
        self.argsActual.indiceDeFaseDeImagen = 3
        self.argsActual.progresoDeFasesDeImagen = (self.argsActual.indiceDeFaseDeImagen / self.argsActual.cantidadTotalDeFasesDeImagen) * 100

        return self.__antesDeAplicar_mresize(self.argsActual)
    def antesDeAplicar_cielAB(self):
        self.argsActual.indiceDeFaseDeImagen = 4
        self.argsActual.progresoDeFasesDeImagen = (self.argsActual.indiceDeFaseDeImagen / self.argsActual.cantidadTotalDeFasesDeImagen) * 100

        return self.__antesDeAplicar_cielAB(self.argsActual)
    def alTerminarConExito(self):
        self.argsActual.indiceDeFaseDeImagen = 5
        self.argsActual.progresoDeFasesDeImagen = (self.argsActual.indiceDeFaseDeImagen / self.argsActual.cantidadTotalDeFasesDeImagen) * 100

        return self.__alTerminarConExito(self.argsActual)



def procesarYcrearDataSet_BoolSiContinuar(carpetaImagenesOriginales,carpetaSalidaDataSet,eventos:EventosAlProcesarYcrearDataSet):
    def accion(fOriginal:File,fDestino:File):
        if UtilesImg.esImagen(fOriginal):
            if not eventos.antesDeComenzarAProcesarLaImagen(fOriginal,fDestino):
                return False
            urlImagenEntrada=str(fOriginal)

            urlSalida=str(fDestino)
            if not eventos.antesDeAplicar_grayWorld():
                return False
            grayWorld(urlImagenEntrada, urlSalida)
            if not eventos.antesDeAplicar_boundingBox():
                return False
            boundingBox(urlSalida, urlSalida)
            if not eventos.antesDeAplicar_mresize():
                return False
            mresize(urlSalida, urlSalida)
            if not eventos.antesDeAplicar_cielAB():
                return False
            cielAB(urlSalida, urlSalida)
            if not eventos.alTerminarConExito():
                return False
            return True
        else:
            return False
    Archivo.recorrerCarpetaYCrearSubCarpetasImagen_BoolContinuar(carpetaImagenesOriginales,carpetaSalidaDataSet,accion)

def procesarYcrearDataSet(carpetaImagenesOriginales,carpetaSalidaDataSet,accionAlCrearUnaImagen=None):
    def accion(fOriginal:File,fDestino:File):
        if UtilesImg.esImagen(fOriginal):
            urlImagenEntrada=str(fOriginal)
            urlSalida=str(fDestino)
            grayWorld(urlImagenEntrada, urlSalida)
            boundingBox(urlSalida, urlSalida)
            mresize(urlSalida, urlSalida)
            cielAB(urlSalida, urlSalida)
            if accionAlCrearUnaImagen!=None:
                accionAlCrearUnaImagen(fOriginal,fDestino)
    Archivo.recorrerCarpetaYCrearSubCarpetasImagen(carpetaImagenesOriginales,carpetaSalidaDataSet,accion)



# def prueba():
#     entrada=File(r"F:\_BORRAR\Nueva carpeta\Entrada\ds1")
#     salida=File(r"F:\_BORRAR\Nueva carpeta\Salida\fb2")
#
#     def printProgres(args:ArgumentosDeEventosAlProcesarYcrearDataSet,nombrePaso,porcientoPaso):
#         print(args.nombreCarpetaPadre," img: ", args.nombreImagen
#               , " ", args.indiceImagen, "/", args.cantidadTotalDeImagenes, "(",args.porcientoDeImagenConRespectoAlTotal,"%", ")"
#               ," ",args.indiceDeImagenEnCarpeta,"/",args.cantidadTotalDeImagenesEnEstaCarpeta,"(",args.porcientoDeImagenConRespectoAlaCarpeta,"%",")"
#               ," ",nombrePaso," ",porcientoPaso,"%"
#               )
#         return True
#
#     def antesDeComenzarAProcesarLaImagen(args:ArgumentosDeEventosAlProcesarYcrearDataSet):
#         printProgres(args,"comenzando...",0)
#         return True
#
#     def antesDeAplicar_grayWorld(args:ArgumentosDeEventosAlProcesarYcrearDataSet):
#         printProgres(args,"grayWorld",20)
#         return True
#     def antesDeAplicar_boundingBox(args:ArgumentosDeEventosAlProcesarYcrearDataSet):
#         printProgres(args,"boundingBox",40)
#         return True
#     def antesDeAplicar_mresize(args:ArgumentosDeEventosAlProcesarYcrearDataSet):
#         printProgres(args,"mresize",60)
#         return True
#
#     def antesDeAplicar_cielAB(args: ArgumentosDeEventosAlProcesarYcrearDataSet):
#         printProgres(args, "cielAB", 80)
#         return True
#     def alTerminarConExito(args:ArgumentosDeEventosAlProcesarYcrearDataSet):
#         printProgres(args,"exito",100)
#         return True
#
#     listaPar_NombreCarpeta_CantidadDeImagenes=[
#         ["1 VERDE HECHO",20]
#         ,["2 VERDE", 20]
#         , ["3 RAYONA", 20]
#         , ["4 MADURA", 20]
#     ]
#     eventos=EventosAlProcesarYcrearDataSet(
#         listaPar_NombreCarpeta_CantidadDeImagenes=listaPar_NombreCarpeta_CantidadDeImagenes
#         ,antesDeComenzarAProcesarLaImagen=antesDeComenzarAProcesarLaImagen
#         ,antesDeAplicar_grayWorld=antesDeAplicar_grayWorld
#         , antesDeAplicar_boundingBox=antesDeAplicar_boundingBox
#         , antesDeAplicar_mresize=antesDeAplicar_mresize
#         ,antesDeAplicar_cielAB=antesDeAplicar_cielAB
#         , alTerminarConExito=alTerminarConExito
#     )
#     procesarYcrearDataSet_BoolSiContinuar(
#         carpetaImagenesOriginales=entrada
#         ,carpetaSalidaDataSet=salida
#         ,eventos=eventos
#     )
#
# prueba()