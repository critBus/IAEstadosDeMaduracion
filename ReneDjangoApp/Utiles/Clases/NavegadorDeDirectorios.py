from ReneDjangoApp.Utiles.Clases.File import File
class NavegadorDeDirectorios:
    def __init__(self,carpetaPadreInicial:File):
        self.carpetaPadreInicial:File=carpetaPadreInicial
        self.__condicionDeExpancion=lambda f:f.isDir()
        self.carpetaActual:File=self.carpetaPadreInicial
        self.listaCarpetasActuales=[]
        self.__expandir(self.carpetaActual)
    def puedeRetroceder(self):
        return str(self.carpetaPadreInicial)!=str(self.carpetaActual) and self.carpetaActual.getParent() is not None
    def __expandir(self,f:File):
        contenido=f.listFiles()
        self.listaCarpetasActuales=[fileInterno for fileInterno in contenido if fileInterno.isDir()]
    def intentarExpandir(self):
        if self.__condicionDeExpancion(self.carpetaActual):
            self.__expandir(self.carpetaActual)
    def puedeExpandirse(self,indice):
        if indice<len(self.listaCarpetasActuales) and indice>=0:
            return self.__condicionDeExpancion(self.listaCarpetasActuales[indice])
        return False
