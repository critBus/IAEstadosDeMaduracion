from ReneDjangoApp.Utiles.Clases.File import File
from ReneDjangoApp.Utiles.MetodosUtiles.MetodosBasicos import contiene,strg
from zipfile import ZipFile

def recorrerCarpetaYUtilizarSubCarpetas_BolContinuar(file,utilizar,esCarpetaPadre=True,profundidad=0):#,subRecorrido=None
    # utilizar (f,profundidad)
    file=File.castear(file)
    if file.existe():
        if not esCarpetaPadre:
            if not utilizar(file,profundidad):
                return False
        # else:
        #     if file.subDireccion == None:
        #         file.subDireccion = file.getName()
        #         file.subCarpeta=""
        if file.isDir():

            lf=file.listFiles()
            for f in lf:
                # i.subCarpeta="/"+file.subDireccion
                # i.subDireccion=i.subCarpeta
                # subRecorridoActual=subRecorrido+"/"+i.getName()
                if not recorrerCarpetaYUtilizarSubCarpetas_BolContinuar(f,utilizar,False,(profundidad+1)):#,subRecorridoActual
                    return False
        return True
    return False

def recorrerCarpetaYCrearSubCarpetasImagen_BoolContinuar(carpetaOriginal,carpetaSalida,utilizar):
    def accion(f: File,p:int):
        if f.isDir():
            pass
        else:
            destino = File(strg(carpetaSalida, f.getSubFile()))
            if not destino.getParentFile().existe():
                crearCarpeta(destino.getParentFile())
            if not utilizar(f,destino):
                return False
        return True

    recorrerCarpetaYUtilizarSubCarpetas_BolContinuar(carpetaOriginal, accion)


def crearCarpeta(direccion):
    File(direccion).mkdirs()

def getProfundidad(f):
    f=str(f).strip()
    p=len(f.replace("\\","/").split("/"))-1
    if f.endswith("/"):
        return p-1
    return p

    #f = File.castear(f)

def esZip(f):
    f=File.castear(f)
    return f.isFile() and f.getExtencion().lower()==".zip"
def extraerZip_BoolContinuar(urlZip,urlCarpetaSalida,metodoBool_AntesDeExtraer,metodoBool_GetProgreso):
    #metodoBool_AntesDeExtraer (nombreFile)->bool
    #metodoBool_GetProgreso (totalArchivos,indiceActual)->bool
    #f_carpeta_salida=File(urlCarpetaSalida)
    with ZipFile(urlZip, 'r') as obj_zip:
        FileNames = obj_zip.namelist()
        total=len(FileNames)
        indice=0
        for fileName in FileNames:
            if not metodoBool_AntesDeExtraer(fileName):
                return None
            #f_salida_elemento=File
            obj_zip.extract(str(fileName), str(urlCarpetaSalida))
            if not metodoBool_GetProgreso(total,indice):
                return None
            indice+=1



def getExtencion(dire):
    #print("dire=",dire)
    file = File.getFile(dire)
    #print("file=", file)
    name=file.getName()
    if contiene(name,"."):
        return name[name.rfind("."):len(name)]
    return ""


def recorrerCarpetaYUtilizarSubCarpetas_BolEntrar(file, utilizar, esCarpetaPadre=True,
                                                  profundidad=0):  # ,subRecorrido=None
    # utilizar (f,profundidad)
    file = File.castear(file)
    if file.existe():
        if not esCarpetaPadre:
            if utilizar(file, profundidad) == False:
                return None
        # else:
        #     if file.subDireccion == None:
        #         file.subDireccion = file.getName()
        #         file.subCarpeta=""
        if file.isDir():

            lf = file.listFiles()
            for f in lf:
                # i.subCarpeta="/"+file.subDireccion
                # i.subDireccion=i.subCarpeta
                # subRecorridoActual=subRecorrido+"/"+i.getName()
                recorrerCarpetaYUtilizarSubCarpetas_BolEntrar(f, utilizar, False,
                                                              (profundidad + 1))  # ,subRecorridoActual

#
# def recorrerCarpetaYUtilizarSubCarpetas_BolContinuar(file,utilizar,esCarpetaPadre=True,profundidad=0):#,subRecorrido=None
#     # utilizar (f,profundidad)
#     file=File.castear(file)
#     if file.existe():
#         if not esCarpetaPadre:
#             if not utilizar(file,profundidad):
#                 return False
#         # else:
#         #     if file.subDireccion == None:
#         #         file.subDireccion = file.getName()
#         #         file.subCarpeta=""
#         if file.isDir():
#
#             lf=file.listFiles()
#             for f in lf:
#                 # i.subCarpeta="/"+file.subDireccion
#                 # i.subDireccion=i.subCarpeta
#                 # subRecorridoActual=subRecorrido+"/"+i.getName()
#                 if not recorrerCarpetaYUtilizarSubCarpetas_BolContinuar(f,utilizar,False,(profundidad+1)):#,subRecorridoActual
#                     return False
#         return True
#     return False