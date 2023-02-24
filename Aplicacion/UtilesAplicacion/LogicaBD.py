from operator import attrgetter,itemgetter
from typing import TYPE_CHECKING, Dict, List, NoReturn, Optional, Union, Tuple, cast, ClassVar
from django.contrib.auth.models import User,Group
from Aplicacion.models import * #,Fruto
from Aplicacion.UtilesAplicacion.ClasesLogica import *
#from Aplicacion.UtilesAplicacion.ConstantesApp import APP_CNF.consts.PERMISO_ADMIN,APP_CNF.consts.PERMISO_INVESTIGADOR

from ReneDjangoApp.Utiles.Utiles import *
import os
from datetime import datetime

from ipware.ip import get_client_ip


# class DatosDeDataset:
#     def __init__(self):
#         self

# class DatasetsYClasificaciones:
#     def __init__(self):
#         self.matrizPar_Datasets_Clasificaciones=[]
#     def add(self,dataset,clasificaciones):
#         self.matrizPar_Datasets_Clasificaciones.append([dataset,clasificaciones])

class FrutoYModelos:
    def __init__(self):
        self.fruto=None
        self.listaDeModelos=None

def isEmptyVariable(a):
    return len(str(a))==0
def ErrorMensaje(mensaje):
    return Exception("El nombre no puede estar vacío")

class BD(BD_DJ):
    def getDatosDeModelos_ParaCalsificar(self):
        l=self.getListaParNombresFrutosYIdModeloNeuronal()
        return [DatosModeloNeuronal(self.getModeloNeuronal_id(idModelo),self)  for nombreFrutoCienti,idModelo in l]

    def getListaParNombresFrutosYIdModeloNeuronal(self):
        lm=self.getModelosNeuronalesAll()
        dic={}
        for m in lm:
            dataset:Dataset=self.getDataset_ModeloNeuronal(m)
            fr=dataset.Fruto.NombreCientifico
            if fr in dic:
                if dic[fr].Precision < m.Precision:
                    dic[fr]=m
            else:
                dic[fr] = m
        return [[k,dic[k].id] for k in dic]

    def agregarTipoDeFruto(self,nombreCientifi,variedad,descripcion):
        if isEmptyVariable(nombreCientifi):
            raise ErrorMensaje("El nombre no puede estar vacío")
        if isEmptyVariable(variedad):
            raise ErrorMensaje("El tipo no puede estar vacío")
        if self.existeFrutoConNombre(nombre=nombreCientifi):
            raise ErrorMensaje("Ya existe un fruto con este nombre ")
        self.saveFrutoNuevo(nombreCientifi,variedad,descripcion)
    def saveFrutoNuevo(self,nombre,variedad,descripcion):
        return self.saveFruto(nombre,nombre,variedad,descripcion,"")
    def existeFrutoConNombre(self,nombre):
        return Fruto.objects.filter(NombreCientifico=nombre).exists()


    def editarFruto(self,id,nombre
                          ,nombreCientifico
                          ,variedad
                  , descripcion
                    , direccionImagen
                  ):
        nombre = nombre.strip()
        nombreCientifico = nombreCientifico.strip()
        variedad = variedad.strip()
        fruto:Fruto=self.getFruto_id(id)
        if fruto.Nombre!=nombre \
            or fruto.NombreCientifico !=nombreCientifico\
            or fruto.Variedad!= variedad\
            or fruto.Descripcion!=descripcion\
                or direccionImagen is not None:
            fruto.Nombre=nombre
            fruto.NombreCientifico =nombreCientifico
            fruto.Variedad = variedad
            fruto.Descripcion = descripcion
            if direccionImagen is not None:
                fruto.DireccionImagen = direccionImagen
            fruto.save()
        return fruto


    def getDatasetAll_Fruto(self,fruto:Fruto)->List[Dataset]:
        return Dataset.objects.filter(Fruto=fruto)
    def deleteFruto_id_Cascada(self,id):
        fruto: Fruto = self.getFruto_id(id)
        ld=self.getDatasetAll_Fruto(fruto)
        for d in ld:
            self.deleteDataset_Cascada_id(d.id)

        fruto.delete()
    def existeFruto_NombreCientifico(self,nombreCientifico):
        return Fruto.objects.filter(NombreCientifico=nombreCientifico).exists()
    def existeFruto_Nombre_Variedad(self,nombre,variedad):
        return Fruto.objects.filter(Nombre=nombre,Variedad=variedad).exists()
    def existeFruto_id(self,id):
        return Fruto.objects.filter(id=int(id)).exists()
    def existeClasificacion_id(self,id):
        return Clasificacion.objects.filter(id=int(id)).exists()
    def getFrutosAll(self):
        return Fruto.objects.all()
    def getFruto_id(self, id):
        return Fruto.objects.get(id=int(id))

    def getFruto_nombre_variedad(self, nombre,variedad):
        return Fruto.objects.get(Nombre=nombre,Variedad=variedad)
    def saveFruto(self
                          ,nombre
                          ,nombreCientifico
                          ,variedad
                  , descripcion
                  , direccionImagen

                  ):
        nombre=nombre.strip()
        nombreCientifico = nombreCientifico.strip()
        variedad = variedad.strip()
        dato = Fruto.objects.create(
            Nombre=nombre
            , NombreCientifico=nombreCientifico
            , Variedad=variedad
            , Descripcion=descripcion
            , DireccionImagen=direccionImagen


        )
        dato.save()
        return dato


    def getModeloNeuronal_All_Dataset(self,dataset)->List[ModeloNeuronal]:
        le:List[Entrenamiento]=self.getEntrenamiento_All_Dataset(dataset)
        return [e.ModeloNeuronal for e in le if e.Dataset.id==dataset.id]
        #return ModeloNeuronal.objects.filter(Dataset=dataset)

    def getClaseDeClasificacion_SortVisual_All_ModeloNeuronal(self,modeloNeuronal:ModeloNeuronal)->List[ClaseDeClasificacion]:
        # entrenamiento:Entrenamiento=self.getEntrenamiento_ModeloNeuronal(modeloNeuronal)
        # return self.getClaseDeClasificacion_All_Dataset(entrenamiento.Dataset)
        return self.getClaseDeClasificacion_SortVisual_All_Dataset(self.getDataset_ModeloNeuronal(modeloNeuronal))

    def getClaseDeClasificacion_SortVisual_All_Dataset(self,dataset)->List[ClaseDeClasificacion]:
        # l=self.getRelacionClasesDeClasificacionYDataset_All_Dataset(dataset)
        # return [e.ClaseDeClasificacion for e in l]
        clasificaciones:List[ClaseDeClasificacion]=ClaseDeClasificacion.objects.filter(Dataset=dataset)
        clasificaciones_en_orden_para_entrenamiento:List[ClaseDeClasificacion]=[cla for cla in clasificaciones]
        for cla in clasificaciones:
            clasificaciones_en_orden_para_entrenamiento[cla.Indice]=cla
        return clasificaciones_en_orden_para_entrenamiento

    def editarModeloNeuronal(self,id,nombre
                             #,fruto
                             ,descripcion):
        dts:ModeloNeuronal=self.getModeloNeuronal_id(id)
        dts.Nombre=nombre
        #dts.Fruto=fruto
        dts.Descripcion=descripcion
        dts.save()
        return dts
    def editarDataset(self,id,nombre,fruto,descripcion,matrisDeNombreDeClasificaciones):
        dts:Dataset=self.getDataset_id(id)
        dts.Nombre=nombre
        dts.Fruto=fruto
        dts.Descripcion=descripcion

        lcla=self.getClaseDeClasificacion_All_Dataset(dts)
        for cla in lcla:
            for i,datos in enumerate(matrisDeNombreDeClasificaciones):
                nombreClasi = datos[0]
                nombreCarpeta=datos[1]
                descripcion=datos[2]
                if cla.NombreCarpetaCorrespondiente==nombreCarpeta:
                    if cla.Nombre!=nombreClasi \
                            or cla.Indice!=i \
                        or cla.Descripcion!=descripcion:
                        cla.Nombre=nombreClasi
                        cla.Descripcion=descripcion
                        cla.Indice=i
                        cla.save()
                    break

        dts.save()
        return dts
    def editarUsuario(self,id,nombre, apellido, correo,esInvestigador,esAdmin,activo):
        nombre=nombre.strip()
        apellido = apellido.strip()
        correo = correo.strip()


        user:User=self.getUser_id(id)
        if user.first_name!=nombre or user.last_name!=apellido \
                or user.email!=correo or user.is_active!=activo\
                or user.is_staff!= (esAdmin and user.is_active):
            user.first_name=nombre
            user.last_name=apellido
            user.email = correo
            user.is_active=activo

            user.is_staff = esAdmin and user.is_active

            user=self.editarUser(user)



        def agregarGrupo(nombre):
            group=Group.objects.get(name=nombre)
            user.groups.add(group)
        def removeGrupo(nombre):
            if user.groups.filter(name=nombre).exists():
                group = user.groups.get(name=nombre)
                user.groups.remove(group)

        def editarGrupoDeSerNecesario(loQueEra,loQueTieneQueSer,nombreGrupo):
            if loQueEra:
                if not loQueTieneQueSer:
                    removeGrupo(nombreGrupo)
            else:
                if loQueTieneQueSer:
                    agregarGrupo(nombreGrupo)


        perteneceALosInvestigadores=user.groups.filter(name=APP_CNF.consts.PERMISO_INVESTIGADOR).exists()
        perteneceALosAdmin = user.groups.filter(name=APP_CNF.consts.PERMISO_ADMIN).exists()

        editarGrupoDeSerNecesario(perteneceALosInvestigadores,esInvestigador,APP_CNF.consts.PERMISO_INVESTIGADOR)
        editarGrupoDeSerNecesario(perteneceALosAdmin, esAdmin, APP_CNF.consts.PERMISO_ADMIN)
        return user




    def deleteUsuario_id_Cascada(self, id):
        self.deleteUsuario_Cascada(self.getUser_id(id))
    def deleteUsuario_Cascada(self,usuario:User):
        cla=self.getClasificacion_All_username(usuario.username)
        for c in cla:
            self.deleteClasificacion_YProcesamiento_idClasificacion_(c.id)
        dt=self.getDatasetAll_Usuario(usuario)
        for d in dt:
            self.deleteDataset_Cascada_id(d.id)
        lm=self.getModelosNeuronalesAll_Usuario(usuario)
        for m in lm:
            self.deleteModeloNeuronal_Cascada_id(m.id)
        self.deleteUser(usuario)


    def esInvestigador(self,usuario:User):
        return usuario.groups.filter(name__in=[APP_CNF.consts.PERMISO_ADMIN,APP_CNF.consts.PERMISO_INVESTIGADOR]).exists()


    def esAdmin(self,usuario:User):
        return usuario.groups.filter(name=APP_CNF.consts.PERMISO_ADMIN).exists()

    def createPermiosDefault(self):
        def crearGrupoSiNoExiste(nombre):
            if not Group.objects.filter(name=nombre).exists():
                group = Group(name=nombre)
                group.save()

        crearGrupoSiNoExiste(APP_CNF.consts.PERMISO_ADMIN)
        crearGrupoSiNoExiste(APP_CNF.consts.PERMISO_INVESTIGADOR)
    def crearUsuario(self,username, password, nombre, apellido, correo,esInvestigador,esAdmin):
        user:User=self.saveUser(username, password, nombre, apellido, correo,es_de_los_adminstradores=esAdmin)
        #self.createPermiosDefault()
        def agregarGrupo(nombre):
            group=Group.objects.filter(name=nombre)[0]
            user.groups.add(group)
        if esInvestigador:
            agregarGrupo(APP_CNF.consts.PERMISO_INVESTIGADOR)
        if esAdmin:
            agregarGrupo(APP_CNF.consts.PERMISO_ADMIN)
            # user.is_staff=True
            # user.save()





    def __parseRepresentacionDeUsuario(self,usuario:User)->RepresentacionDeUsuario:
        ru = RepresentacionDeUsuario()
        ru.username=usuario.username
        ru.nombre =usuario.first_name
        ru.apellidos = usuario.last_name
        ru.correo = usuario.email
        ru.id=usuario.id
        ru.enable=usuario.is_active

        ru.fechaDeCreacion=usuario.date_joined
        if self.esAdmin(usuario):
            ru.permiso=APP_CNF.consts.PERMISO_ADMIN#"administrador"
        elif self.esInvestigador(usuario):
            ru.permiso =APP_CNF.consts.PERMISO_INVESTIGADOR #"investigador"
        else:
            ru.permiso =APP_CNF.consts.PERMISO_USUARIO#"usuario"
        return ru


    def getRepresentacionDeUsuario_All(self)->List[RepresentacionDeUsuario]:
        lu=self.getUser_All()
        return [self.__parseRepresentacionDeUsuario(u) for u in lu]

    def getRepresentacionDeUsuario_id(self,id)->RepresentacionDeUsuario:

        return self.__parseRepresentacionDeUsuario(self.getUser_id(id))



    def getRepresentacionesDeEpoca(self,entrenamiento:Entrenamiento)->List[RepresentacionDeEpoca]:
        mr=[]
        epocas=bd.getEpoca_All_Entrenamiento(entrenamiento)
        cantidadDeEpocas=len(epocas)
        for e in epocas:
            datos=bd.getDatoEnHistorialDeEntrenamiento_All_Epoca(e)
            cantidadDeLotes=len(datos)

            re:RepresentacionDeEpoca=RepresentacionDeEpoca()
            re.epoca=e.Numero_De_Epoca
            re.precision_Epoca=e.Precision
            re.perdida_Epoca = e.Perdida
            lr=[]

            for d in datos:
                r=RepresentacionDeDatoDeLoteEnHistorialDeEntrenamiento()

                r.epoca=e.Numero_De_Epoca
                r.lote=d.Lote
                r.cantidadDeLotes=cantidadDeLotes
                r.cantidadDeEpocas=cantidadDeEpocas
                r.precision_Lote=d.Precision
                r.perdida_Lote=d.Perdida
                r.precision_Epoca = e.Perdida
                r.perdida_Epoca = e.Precision

                lr.append(r)
            lr=sorted(lr, key=attrgetter('lote'))
            #sorted(lr, key=attrgetter('lote'))
            re.listaDeLotes=lr
            mr.append(re)
        mr=sorted(mr, key=attrgetter('epoca'))
        #sorted(mr, key=attrgetter('epoca'))
        return mr



                

    def deleteModeloNeuronal_Cascada_id(self, id):
        m = self.getModeloNeuronal_id(id)
        lc=self.getClasificacion_All_ModeloNeuronal(m)
        for cla in lc:
            self.deleteClasificacion_YProcesamiento_idClasificacion_(cla.id)

        self.deleteValidacion_Cascada(self.getValidacion_ModeloNeuronal(m))
        self.deleteEntrenamiento_Cascada(self.getEntrenamiento_ModeloNeuronal(m))
        self.deleteModeloNeuronal(m)

    def getValidacion_ModeloNeuronal(self,modelo:ModeloNeuronal)->Validacion:
        #return Validacion.objects.get(ModeloNeuronal=modelo)
        validaciones=Validacion.objects.filter(ModeloNeuronal=modelo)
        if len(validaciones)>0:
            return validaciones[0]
        return None

    def getValidacion_All_Dataset(self,dts:Dataset)->List[Validacion]:
        return Validacion.objects.filter(Dataset=dts)


    def deleteValidacion_Cascada(self,dato):
        le=self.getDatoEnMatrizDeConfusion_All_Validacion(dato)
        for e in le:
            self.deleteDatoEnMatrizDeConfusion(e)
        self.deleteValidacion(dato)
    def deleteValidacion(self,dato):
        dato.delete()
    def getDatoEnMatrizDeConfusion_All_Validacion(self,validacion):
        return DatoEnMatrizDeConfusion.objects.filter(Validacion=validacion)
    def deleteDatoEnMatrizDeConfusion(self,dato):
        dato.delete()
    def deleteEntrenamiento_Cascada(self,dato):
        le=self.getEpoca_All_Entrenamiento(dato)
        for e in le:
            self.deleteEpoca_Cascada(e)
        self.deleteEntrenamiento(dato)
    def deleteEntrenamiento(self,dato):
        dato.delete()
    def getEpoca_All_Entrenamiento(self,entrenamiento):
        return Epoca.objects.filter(Entrenamiento=entrenamiento)
    def deleteEpoca_Cascada(self, dato):
        ld=self.getDatoEnHistorialDeEntrenamiento_All_Epoca(dato)
        for d in ld:
            self.deleteDatoEnHistorialDeEntrenamiento(d)
        self.deleteEpoca(dato)
    def deleteEpoca(self,dato):
        dato.delete()
    def getDatoEnHistorialDeEntrenamiento_All_Epoca(self,epoca):
        return DatoEnHistorialDeEntrenamiento.objects.filter(Epoca=epoca)
    def deleteDatoEnHistorialDeEntrenamiento(self,dato):
        dato.delete()

    def getEntrenamiento_ModeloNeuronal(self,modelo:ModeloNeuronal)->Entrenamiento:
        #return Entrenamiento.objects.get(ModeloNeuronal=modelo)
        entrenamientos=Entrenamiento.objects.filter(ModeloNeuronal=modelo)
        if len(entrenamientos)>0:
            return entrenamientos[0]
        return None #get

    def getEntrenamiento_All_Dataset(self,dts:Dataset)->List[Entrenamiento]:
        return Entrenamiento.objects.filter(Dataset=dts)

    # def getEntrenamiento_Dataset(self,dts:Dataset)->Entrenamiento:
    #     #return Entrenamiento.objects.get(ModeloNeuronal=modelo)
    #     entrenamientos=Entrenamiento.objects.filter(Dataset=dts)
    #     if len(entrenamientos)>0:
    #         return entrenamientos[0]
    #     return None #get

    def getDataset_ModeloNeuronal(self, modeloNeuronal:ModeloNeuronal)->Dataset:
        entrenamiento: Entrenamiento = self.getEntrenamiento_ModeloNeuronal(modeloNeuronal)
        return entrenamiento.Dataset

    def getClaseDeClasificacion_All_ModeloNeuronal(self,modeloNeuronal:ModeloNeuronal)->List[ClaseDeClasificacion]:
        # entrenamiento:Entrenamiento=self.getEntrenamiento_ModeloNeuronal(modeloNeuronal)
        # return self.getClaseDeClasificacion_All_Dataset(entrenamiento.Dataset)
        return self.getClaseDeClasificacion_All_Dataset(self.getDataset_ModeloNeuronal(modeloNeuronal))

    def getClaseDeClasificacion_All_Dataset(self,dataset)->List[ClaseDeClasificacion]:
        # l=self.getRelacionClasesDeClasificacionYDataset_All_Dataset(dataset)
        # return [e.ClaseDeClasificacion for e in l]
        clasificaciones:List[ClaseDeClasificacion]=ClaseDeClasificacion.objects.filter(Dataset=dataset)
        clasificaciones_en_orden_para_entrenamiento:List[ClaseDeClasificacion]=[cla for cla in clasificaciones]
        for cla in clasificaciones:
            clasificaciones_en_orden_para_entrenamiento[cla.Indice_De_Carpeta]=cla
        return clasificaciones_en_orden_para_entrenamiento
    def saveEntrenamiento(self
                          ,total_De_Epocas
                          ,modeloNeuronal
                          ,dataset):
        dato = Entrenamiento.objects.create(
            Total_De_Epocas=total_De_Epocas
            , ModeloNeuronal=modeloNeuronal
            , Dataset=dataset

        )
        dato.save()
        return dato
    def saveEpoca(self, numero_De_Epoca
                                           , total_De_Lotes
                                           , precision
                                           , perdida

                                           , entrenamiento):

        dato = Epoca.objects.create(
            Numero_De_Epoca=numero_De_Epoca
            , Total_De_Lotes=total_De_Lotes
            , Precision=precision
            , Perdida=perdida
            , Entrenamiento=entrenamiento

        )
        dato.save()
        return dato
    def saveDatoEnHistorialDeEntrenamiento(self, epoca
                                           , lote
                                           , precision
                                           , perdida
                                           ):

        dato = DatoEnHistorialDeEntrenamiento.objects.create(
            Epoca=epoca
            , Lote=lote
            , Precision=precision
            , Perdida=perdida


        )
        dato.save()
        return dato

    def saveValidacion(self
                          , precision
                       ,porcentaje_Utilizado_Del_Dataset
                          , modeloNeuronal
                          , dataset):
        dato = Validacion.objects.create(
            Precision=precision
            ,Porcentaje_Utilizado_Del_Dataset=porcentaje_Utilizado_Del_Dataset
            , ModeloNeuronal=modeloNeuronal
            , Dataset=dataset

        )
        dato.save()
        return dato
    def saveDatoEnMatrizDeConfusion(self, clasificacion_predicha
                                           , clasificacion_real
                                           , indice_columna
                                           , indice_fila
                                           , cantidad
                                           , validacion):

        dato = DatoEnMatrizDeConfusion.objects.create(
            Clasificacion_predicha=clasificacion_predicha
            , Clasificacion_real=clasificacion_real
            , Indice_columna=indice_columna
            , Indice_fila=indice_fila
            , Cantidad=cantidad
            , Validacion=validacion

        )
        dato.save()
        return dato

    def getNombreCarpeta_deClasificacion(self,dataset,clasificacion):
        clasesClasificaciones=self.getClaseDeClasificacion_All_Dataset(dataset)
        for cl in clasesClasificaciones:
            if cl.Nombre==clasificacion:
                return cl.NombreCarpetaCorrespondiente
        return None
    def getClaseDeClasificacion_id(self,id)->ClaseDeClasificacion:
        return ClaseDeClasificacion.objects.get(id=int(id))
    def deleteClaseDeClasificacion(self,m):
        m.delete()
    def deleteClaseDeClasificacion_id(self,id):
        m=self.getClaseDeClasificacion_id(id)
        self.deleteClaseDeClasificacion(m)


    def getClasificacion_All_ModeloNeuronal(self,modeloNeuronal):
        return Clasificacion.objects.filter(ModeloNeuronal=modeloNeuronal)

    def deleteModeloNeuronal(self,m):
        m.delete()
    def deleteModeloNeuronal_id(self,id):
        m=self.getModeloNeuronal_id(id)
        self.deleteModeloNeuronal(m)
    def deleteDataset_Cascada_id(self,id):
        dat=self.getDataset_id(id)



        lm = self.getModeloNeuronal_All_Dataset(dat)
        for m in lm:
            self.deleteModeloNeuronal_Cascada_id(m.id)

        le = self.getEntrenamiento_All_Dataset(dat)
        for e in le:
            self.deleteModeloNeuronal_Cascada_id(e.ModeloNeuronal.id)

        lv=self.getValidacion_All_Dataset(dat)
        for v in lv:
            self.deleteModeloNeuronal_Cascada_id(v.ModeloNeuronal.id)


        lc=self.getClaseDeClasificacion_All_Dataset(dat)
        for c in lc:
            self.deleteClaseDeClasificacion_id(c.id)
        self.deleteDataset(dat)
    def deleteDataset_ID(self,id):
        dat=self.getDataset_id(id)
        self.deleteDataset(dat)
    def deleteDataset(self,dat):
        dat.delete()


    def saveDataset(self
                   ,Direccion_Imagenes_Procesadas
                   ,Direccion_Imagenes_Originales
                   ,Nombre
                   ,Descripcion
                   ,CantidadDeImagenes
                   ,Fruto
                   ,usuario
                   ,matris_Clasificacion_NombreCarpeta_CantidadDeImagenes):

        Nombre=str(Nombre).strip()
        Direccion_Imagenes_Procesadas = str(Direccion_Imagenes_Procesadas).strip()
        Direccion_Imagenes_Originales = str(Direccion_Imagenes_Originales).strip()

        dataset= Dataset.objects.create(
         Direccion_Imagenes_Procesadas = Direccion_Imagenes_Procesadas
        , Direccion_Imagenes_Originales = Direccion_Imagenes_Originales
        , Nombre = Nombre
        , Descripcion = Descripcion
        , CantidadDeImagenes = CantidadDeImagenes
        , Fruto = Fruto
            ,User=usuario
        )
        indice=0
        for clasificacion,nombreCarpeta,cantidadDeImagenes,descripcionClase,indice_carpeta in matris_Clasificacion_NombreCarpeta_CantidadDeImagenes:
            ClaseDeClasificacion.objects.create(
                Nombre=clasificacion
                ,NombreCarpetaCorrespondiente=nombreCarpeta
                ,Indice=indice
                ,Indice_De_Carpeta=indice_carpeta
                ,CantidadDeImagenes=cantidadDeImagenes
                ,Descripcion=descripcionClase
                ,Dataset=dataset
            )
            indice+=1

    def existeDataset_Nombre(self,nombre):
        #return self.getDataset(nombre) is not None
        return Dataset.objects.filter(Nombre=nombre).exists()
    def getDataset(self,nombre):
        #return Dataset.objects.get(Nombre=nombre)
        dts = Dataset.objects.filter(Nombre=nombre)
        if len(dts) > 0:
            return dts[0]
        return None  # get

    def existeDataset_ID(self,id):
        #return self.getDataset_id(id) is not None
        return Dataset.objects.filter(id=id).exists()
    def existeModeloNeuronal_Nombre(self,nombre):
        #return self.getModelo(nombre) is not None
        return ModeloNeuronal.objects.filter(Nombre=nombre).exists()
    def existeModeloNeuronal_ID(self,id):
        #return self.getModeloNeuronal_id(id) is not None
        return ModeloNeuronal.objects.filter(id=id).exists()



    def getDatasetAll(self):
        return Dataset.objects.all()
    def getDatasetAll_Usuario(self,usuario:User)->List[Dataset]:
        return Dataset.objects.filter(User=usuario)
    def getDataset_id(self,id)->Dataset:
        return Dataset.objects.get(id=int(id))

    def getModelosNeuronalesAll(self):
        return ModeloNeuronal.objects.all()
    def getModelosNeuronalesAll_Usuario(self,usuario:User):
        return ModeloNeuronal.objects.filter(User=usuario)

    def getModeloNeuronal_id(self,id)->ModeloNeuronal:
        return ModeloNeuronal.objects.get(id=int(id))


    def getModelo(self,nombre):
        return ModeloNeuronal.objects.get(Nombre=nombre)



    def saveModeloNeuronal(self,direccion,nombre
                           #,fruto
                           ,user,fechaDeCreacion,descripcion
                           ,precision,perdida,cantidadDeEpocas):
        # print("precision=",precision) ,dataset
        # print("perdida=",perdida)
        nombre = str(nombre).strip()
        direccion = str(direccion).strip()

        m = ModeloNeuronal.objects.create(Direccion=direccion
                                          ,Nombre=nombre
                                          #,Fruto=fruto
                                          ,User=user
                                          #,Dataset=dataset
                                          ,FechaDeCreacion=fechaDeCreacion
                                          ,Descripcion=descripcion
                                          ,Precision=precision
                                          ,Perdida=perdida
                                          ,CantidadDeEpocas=cantidadDeEpocas)
        m.save()
        return m



    def saveProcesamientoImagen(self,imagen):#, user
        pro = ProcesamientoDeImagen.objects.create(ImagenOriginal=imagen)#, User=user
        pro.save()
        return pro

    def saveImagenProcesada(self,imagen, procesamiento, tipo, algoritmo):
        imgp = ImagenProcesada.objects.create(ImagenResultante=imagen
                                              , ProcesamientoDeImagen=procesamiento
                                              , Tipo=tipo
                                              , AlgoritmoUtilizado=algoritmo)
        imgp.save()
        return imgp



    def saveClasificacion(self,procesamiento,imagen, resultado, username,ip, modelo):
        if ip is None:
            ip=APP_CNF.consts.NOMBRE_IP_ANONIMO
        cla = Clasificacion.objects.create(
            Procesamiento=procesamiento
            ,ImagenProcesada=imagen
            , Resultado=resultado
            , Username=username
            ,IP_Usuario=ip
            , ModeloNeuronal=modelo)
        cla.save()
        return cla



    def getClasificacion_All(self):
        return Clasificacion.objects.all().order_by('-Fecha')
    def getClasificacion_All_username(self,username):
        if isinstance(username,User):
            username=username.username
        return Clasificacion.objects.filter(Username=username).order_by('-Fecha')
    def getClasificacion_All_username_ip(self,username,ip):
        if isinstance(username,User):
            username=username.username
        return Clasificacion.objects.filter(Username=username,IP_Usuario=ip).order_by('-Fecha')
    def getClasificacion_All_usuario_contains(self, username,ip,nombreFruto=None,resultado=None,nombreModelo=None,fecha=None):
        esAnonimo=username==APP_CNF.consts.NOMBRE_USUARIO_ANONIMO

        if isNoneAll(nombreFruto,nombreModelo,fecha) and resultado is not None:
            if esAnonimo:
                return Clasificacion.objects.filter(Username=username,IP_Usuario=ip, Resultado__icontains=resultado)
            return Clasificacion.objects.filter(Username=username,Resultado__icontains=resultado)

        def getClasificacion_All_usuario():
            if esAnonimo:
                return self.getClasificacion_All_username_ip(username,ip)
            return self.getClasificacion_All_username(username)

        if isNoneAll(nombreFruto,nombreModelo,resultado) and fecha is not None:
            res = []
            l = getClasificacion_All_usuario()
            for cla in l:
                if contiene(str(getStrDate(cla.Fecha)), fecha,True):
                    res.append(cla)
            return res

        if isNoneAll(nombreFruto, fecha, resultado) and nombreModelo is not None:
            res=[]
            l=getClasificacion_All_usuario()
            for cla in l:
                if contiene(str(cla.ModeloNeuronal.Nombre),nombreModelo,True):
                    res.append(cla)
            return res

        def contieneAFruto(fruto,valor):
            return contiene(str(fruto.NombreCientifico), valor, True)
            # return contiene(str(fruto.Nombre), valor, True)\
            #             or contiene(str(fruto.Variedad), valor, True)\
            #             or contiene(str(fruto.NombreCientifico), valor, True)

        if isNoneAll(nombreModelo, fecha, resultado) and nombreFruto is not None:
            #print("filtro ya")
            res=[]
            l=getClasificacion_All_usuario()
            for cla in l:
                fruto:Fruto=self.getDataset_ModeloNeuronal(cla.ModeloNeuronal).Fruto
                if contieneAFruto(fruto,nombreFruto):
                #if contiene(str(cla.ModeloNeuronal.Fruto), nombreFruto,True):
                    res.append(cla)
            return res
        if not isNoneAll(nombreModelo, fecha, resultado,nombreFruto):
            res = []
            l = getClasificacion_All_usuario()
            for cla in l:
                fruto: Fruto = self.getDataset_ModeloNeuronal(cla.ModeloNeuronal).Fruto
                if contiene(str(cla.Resultado),resultado,True) or\
                        contiene(str(cla.Fecha),fecha,True) or\
                        contiene(str(cla.ModeloNeuronal.Nombre), nombreModelo,True) or \
                        contieneAFruto(fruto, nombreFruto):
                        #contiene(str(cla.ModeloNeuronal.Fruto), nombreFruto,True):
                        #contiene(str(cla.ModeloNeuronal.Fruto.Nombre), nombreFruto):
                    res.append(cla)


            return res
        return []






    def getClasificacion_id(self,id)->Clasificacion:
        return Clasificacion.objects.get(id=int(id))

    def getClasificacion_Procesamiento(self,procesamiento:ProcesamientoDeImagen)->Clasificacion:
        return Clasificacion.objects.get(Procesamiento=procesamiento)
    def deleteClasificacion_id(self,id):
        cla=self.getClasificacion_id(id)
        self.deleteClasificacion(cla)
    def deleteClasificacion(self,cla):
        cla.delete()

    def deleteClasificacion_YProcesamiento_idClasificacion_(self, idClasificacion):
        cla=self.getClasificacion_id(idClasificacion)
        pro=self.getProcesamientoDeImagen_Clasificacion(cla)
        limgp=self.getImagenProcesada_All_deProcesamiento(pro)
        # print("limgp=",limgp)
        # print("tipe=",type(limgp))
        self.deleteClasificacion(cla)
        for imgp in limgp:
            self.deleteImagenProcesada(imgp)
        self.deleteProcesamientoDeImagen(pro)



    def getProcesamientoDeImagen_id(self,id)->ProcesamientoDeImagen:
        return ProcesamientoDeImagen.objects.get(id=id)
    def getImagenProcesada(self,procesamiento,algoritmo)->ImagenProcesada:
        return ImagenProcesada.objects.get(ProcesamientoDeImagen=procesamiento,AlgoritmoUtilizado=algoritmo)

    def getImagenProcesada_All(self):
        return ImagenProcesada.objects.all()
    def getImagenProcesada_All_deProcesamiento(self,procesamiento)->List[ImagenProcesada]:
        return ImagenProcesada.objects.filter(ProcesamientoDeImagen=procesamiento)
    def deleteImagenProcesada(self,imgp:ImagenProcesada):

        APP_CNF.deleteCampoImg(imgp.ImagenResultante)
        imgp.delete()
    def getProcesamientoDeImagenes_All_usuario(self,user):
        return ProcesamientoDeImagen.objects.filter(User=user)
    def getProcesamientoDeImagen_Clasificacion(self,clasificacion:Clasificacion)->ProcesamientoDeImagen:
        return clasificacion.Procesamiento
    def deleteProcesamientoDeImagen(self,pro:ProcesamientoDeImagen):
        APP_CNF.deleteCampoImg(pro.ImagenOriginal)
        pro.delete()

    def getConjuntoProcesamientoDeImagenesDeUsuario(self,user)->List[ConjuntoProcesamientoYClasificacion]:
        l=[]

        lp=self.getProcesamientoDeImagenes_All_usuario(user)
        for pro in lp:
            c=ConjuntoProcesamientoYClasificacion()
            cla=self.getClasificacion_Procesamiento(pro)
            c.imagen=pro.ImagenOriginal
            c.procesamiento=pro
            c.clasificaion=cla
            l.append(c)
        return l


    def getConjuntoProcesamientoDeImagenesYAlgoritmosDeUsuario(self,user)->List[ConjuntoProcesamiento_Clasificacion_Algoritmos]:
        l=[]

        lp=self.getProcesamientoDeImagenes_All_usuario(user)
        for pro in lp:
            c=ConjuntoProcesamiento_Clasificacion_Algoritmos()
            cla=self.getClasificacion_Procesamiento(pro)
            limp=self.getImagenProcesada_All_deProcesamiento(pro)
            for imgp in limp:
                cai=ConjuntoAlgoritoYImagen()
                cai.imagen=imgp.ImagenResultante
                cai.imagenProcesada=imgp
                c.listaDeConjuntoAlgoritoYImagen.append(cai)


            c.imagen=pro.ImagenOriginal
            c.procesamiento=pro
            c.clasificaion=cla
            l.append(c)
        return l



bd=BD()


