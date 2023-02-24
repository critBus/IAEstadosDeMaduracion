from ReneDjangoApp.Utiles.MetodosUtiles.MetodosBasicos import *
from io import open
import os
import tempfile
import shutil

#from Utiles.MetodosUtiles import Archivo
class File():
    SEPARATOR = os.path.altsep
    def __init__(self,direccion="",subFile=None):
        if File.esFile(direccion):
            direccion=str(direccion)
        self.__direccion=direccion.replace("\\","/")
        if contiene(self.__direccion,"../"):
            self.__direccion=self.getAbsolutePath()


        self.__subFile=subFile
        #self.subCarpeta=subCarpeta
        #self._esFile=os.path.isfile(direccion)
    def getSubFile(self):
        if self.__subFile==None:
            self.__subFile=File()
        return self.__subFile
    def existe(self):
        return os.path.exists(self.__direccion)
    def getLenght(self):
        if self.isFile():
            return os.path.getsize(self.__direccion)
            #len(open(self.__direccion).read())
        return -1
    def getLenghtKB(self):
        leng=self.getLenght()
        return leng/1024
    def getLenghtMB(self):
        leng=self.getLenghtKB()
        return leng/1024
    def getLenghtGB(self):
        leng=self.getLenghtMB()
        return leng/1024
    def isFile(self):
        return os.path.isfile(self.__direccion)
    def isDir(self):
        return os.path.isdir(self.__direccion)
    def getAbsolutePath(self):
        return os.path.abspath(self.__direccion)

    def getName(self):
        return os.path.basename(self.__direccion)
    def getParent(self):
        return os.path.dirname(self.__direccion)
    def getParentFile(self):
        return File(self.getParent())
    def esAbsuluteDireccion(self):
        return os.path.isabs(self.__direccion)
    def esLinck(self):
        return os.path.islink(self.__direccion)
    def delete(self):
        if self.isDir():
            def eliminar(fil):
                print("delete: ", fil)
                if fil.isFile():
                    os.remove(str(fil))
                else:
                    os.rmdir(str(fil))

            _recorrerCarpetaYUtilizarSubCarpetas(self, eliminar)
            print("delete final: ", self)
            os.rmdir(str(self))
        # os.removedirs(str(file))
        else:
            os.remove(str(self))
    def rename(self,nuevoNombre=""):
        nuevoNombreReal=nuevoNombre
        padre=self.getParent()
        if not nuevoNombre.startswith(padre) and not contieneOR(nuevoNombre,"\\","/"):
            nuevoNombreReal=self.getParentFile().getAbsolutePath()+self.SEPARATOR+nuevoNombre
        os.rename(self.__direccion,nuevoNombreReal)
        self.__direccion=nuevoNombreReal
    def mkdirs(self):
        if not self.existe():
            os.makedirs(self.__direccion)
        return self
    def crear(self):
        if self.isDir():
            self.mkdirs()
        elif not isEmpty(self.__direccion):
            fil=open(self.__direccion,"w")
            fil.close()
        return self
    def list(self):
        return os.listdir(self.__direccion)
    def listFiles(self):
        ld=self.list()
        lf=[]
        for i in ld:
            lf.append(self.getAppendFile(i))
        return lf
    def append(self,direccion):
        if File.esFile(direccion):
            direccion=str(direccion)
        if not starWithOR(direccion,self.SEPARATOR,"\\","/"):
            direccion=self.SEPARATOR+direccion
        self.__direccion+=direccion
        self.__subFile=File(str(self.getSubFile())+direccion)
        return self
    def getAppendFile(self,direccion):
        return File(direccion=self.__direccion
                    ,subFile=File(str(self.getSubFile()))
                    ).append(direccion)
    def getNameClear(self):
        #if self.isFile():
        ext=self.getExtencion()
        #println("ext=",ext)
        return self.getName()[:-len(ext)]

    def move(self,carpetaDestino):
        """
        la carpeta destino debe de existir y ser oviamente un directorio
        :param carpetaDestino:
        :return:
        """
        if self.existe():
            carpetaDestino = File.castear(carpetaDestino)
            if carpetaDestino.isDir() and carpetaDestino.existe():
                print("moviendo...")
                print("De: ", self)
                print("A dentro de la carpeta: ", carpetaDestino)
                urlNueva = shutil.move(str(self), str(carpetaDestino))
                return File(urlNueva)
            print("esCarpeta: ", carpetaDestino.isDir(), " existe: ", carpetaDestino.existe(), " ", carpetaDestino)
        else:
            print("no existe ", self)
        return None

    def __str__(self):
        return self.__direccion
    def getExtencion(self):
        return File._getExtencion(self.__direccion)
    @staticmethod
    def esFile(file):
        return isinstance(file, File)
    @staticmethod
    def castear(file):

        if not File.esFile(file) and esString(file):
            file = File(file)
        return file

    @staticmethod
    def getFile(direccion):
            # print(type(direccion))
            # print(isinstance(direccion, File))
            if File.esFile(direccion):
                return direccion
            if esString(direccion):
                return File(direccion)

    @staticmethod
    def getStr(a):
        if esString(a):
            return a
        if File.esFile(a):
            return str(a)
        return a

    @staticmethod
    def _getExtencion(dire):
        file = File.getFile(dire)
        name = file.getName()
        if contiene(name, "."):
            return name[name.rfind("."):len(name)]
        return ""



def _recorrerCarpetaYUtilizarSubCarpetas(file,utilizar,esCarpetaPadre=True):
    file=File.castear(file)
    if file.existe():
        if file.isDir():
            lf=file.listFiles()
            for i in lf:
                _recorrerCarpetaYUtilizarSubCarpetas(i,utilizar,False)
        if not esCarpetaPadre:
            utilizar(file)


class FileTemp(File):
    def __init__(self, direccion=""):
        direTemp=tempfile.gettempdir()
        if isEmpty(direccion) or starWithOR(direccion,self.SEPARATOR,"\\","/"):
            sep=""
        else:
            sep=self.SEPARATOR
        if not File(direccion).esAbsuluteDireccion():
            direccion=direTemp+sep+direccion
        super().__init__(direccion+sep)

    @staticmethod
    def esFileTemp(file):
        return isinstance(file,FileTemp)

#print(File("Alerts.html").getNameClear())