
from Aplicacion.UtilesAplicacion.UtilesApp import *
from Aplicacion.UtilesAplicacion.LogicaUpload import *
from Aplicacion.UtilesAplicacion.LogicaIA import logicaDeEntrenamiento
#from Aplicacion.UtilesAplicacion.ConstantesApp import PERMISO_ADMIN,PERMISO_INVESTIGADOR
class Formulario_ConfiguracionDeEntrenamiento(FormularioConValidacion):
    def inicializarCampos(self):
        MIN_CARACTERES = 5
        MAX_CARACTERES = 50
        self.nombre=CampoConAlfanumericos_Validacion()
        self.nombre.addTipoDeValidacion(lambda v:not bd.existeModeloNeuronal_Nombre(v) \
                                                 and (not v in logicaDeEntrenamiento.getListaDeNombresDeModeloEnProceso())
                                        ,"Ya existe un modelo neuronal con este nombre ")
        self.nombre.setMaxCar(MAX_CARACTERES).setMinCar(MIN_CARACTERES)

        self.descripcion=CampoConValidacionPost()

        # self.tipoDeFruto=CampoConAlfanumericos_Validacion()
        # self.tipoDeFruto.setMaxCar(MAX_CARACTERES).setMinCar(MIN_CARACTERES)

        self.idDataset=CampoPositivo_Validacion()
        self.idDataset.addTipoDeValidacion(lambda v:  bd.existeDataset_ID(v),
                                        "No se encuentra este Dataset en la Base de Datos ")

        self.cantidadDeEpocas=CampoRangoEnteroPositivo_Validacion(0,100,valorPorDefecto=80)
        self.usarPorcentajeParaValidacion=CampoRB_Validacion(APP_CNF.inputs.TIPO_DE_VALIDACION,valorPorDefecto=True)
        self.usarDatasetParaValidacion = CampoRB_Validacion(APP_CNF.inputs.TIPO_DE_VALIDACION)

        self.porsentajeParaValidacion=CampoRangoPositivo_Validacion(0.1,0.4,valorPorDefecto=0.2)
        self.porsentajeParaValidacion.setDependeDeCB(self.usarPorcentajeParaValidacion)

        self.idDatasetParaValidacion = CampoPositivo_Validacion()
        self.idDatasetParaValidacion.setDependeDeCB(self.usarDatasetParaValidacion)
        self.idDatasetParaValidacion.addTipoDeValidacion(lambda v: bd.existeDataset_ID(v),
                                                         "No se encuentra este Dataset en la Base de Datos ")
        self.idDatasetParaValidacion.addTipoDeValidacion(lambda v: v!=self.idDataset.valor,
                                                         "Los Dataset seleccionados tienen que ser distintos ")
        def validar_DatasetDeValidacion1(idDts):
            dtsV=bd.getDataset_id(idDts)
            claV=bd.getClaseDeClasificacion_All_Dataset(dtsV)
            dtsE=bd.getDataset_id(self.idDataset.valor)
            claE=bd.getClaseDeClasificacion_All_Dataset(dtsE)
            return len(claV)==len(claE)

        self.idDatasetParaValidacion.addTipoDeValidacion(validar_DatasetDeValidacion1,
                                                         "EL Dataset de validación debe de coincidir al menos en cantidad de clases de clasificación con respecto al Dataset de entrenamiento   ")



        self.usarLimiteDePrecision = CampoCB_Validacion(valorPorDefecto=True)
        self.limiteDePrecision = CampoRangoPositivo_Validacion(0.6, 0.99,valorPorDefecto=0.92)
        self.limiteDePrecision.setDependeDeCB(self.usarLimiteDePrecision)

        self.guardarMaximaPrecision = CampoCB_Validacion(valorPorDefecto=True)

class Formulario_AgregarDataset(FormularioConValidacion):
    def inicializarCampos(self):
        MIN_CARACTERES = 5
        MAX_CARACTERES = 50
        self.nombre=CampoConAlfanumericos_Validacion()
        self.nombre.addTipoDeValidacion(lambda v:(not bd.existeDataset_Nombre(v)) and (not v in logicaUploadDataset.getListaDeNombresDeDatasetEnProceso()),"Ya existe un dataset con este nombre ")
        self.nombre.setMaxCar(MAX_CARACTERES).setMinCar(MIN_CARACTERES)

        self.descripcion=CampoConValidacionPost()

        self.tipoDeFruto=CampoConValidacionPost()
        self.tipoDeFruto.addTipoDeValidacion(
            lambda v: bd.existeFruto_id(v)
            , "No existe este fruto")
        # self.tipoDeFruto.setMaxCar(MAX_CARACTERES).setMinCar(MIN_CARACTERES)


class Formulario_AgregarUsuario(FormularioConValidacion):
    def inicializarCampos(self):
        MIN_CARACTERES = 5
        MIN_CARACTERES_NOMBRE = 4
        MAX_CARACTERES = 50
        MIN_CARACTERES_CORREO = 10
        MAX_CARACTERES_CORREO = 100
        self.usuario = CampoConAlfanumericos_Validacion()
        def comprobarSiExisteUsuario(username):
            existeUsuario=bd.existeUsuario(str(username).strip())
            #print("dentro de validacion existe usuario=",existeUsuario)
            #print("respuesta esValido:",not existeUsuario)
            return not existeUsuario
        self.usuario.addTipoDeValidacion(comprobarSiExisteUsuario ,
                                        "Ya existe un usuario con este username ")
        self.usuario.setMaxCar(MAX_CARACTERES).setMinCar(MIN_CARACTERES)

        self.nombre=CampoSoloLetras_Validacion()
        self.nombre.setMaxCar(MAX_CARACTERES).setMinCar(MIN_CARACTERES_NOMBRE)

        self.apellidos = CampoSoloLetras_Validacion()
        self.apellidos.setMaxCar(MAX_CARACTERES).setMinCar(MIN_CARACTERES)

        self.contraseña=CampoSeguridadMinimaContraseña_Validacion().setMaxCar(200)

        self.confirmarContraseña = CampoCoincidenteContraseña_Validacion(self.contraseña).setMaxCar(200)

        self.correo=CampoCorreo_Validacion()
        self.correo.setMaxCar(MAX_CARACTERES_CORREO).setMinCar(MIN_CARACTERES_CORREO)

        self.permisosDeUsuario=CampoSelecionar_Validacion(["1","2","3"])

class Formulario_CambiarContraseñaUsuario(FormularioConValidacion):
    def inicializarCampos(self):
        self.usuario = CampoConAlfanumericos_Validacion()
        self.usuario.addTipoDeValidacion(lambda username:bd.existeUsuario(str(username).strip()),
                                         "No existe un usuario con este username ")
        self.contraseña = CampoSeguridadMinimaContraseña_Validacion().setMaxCar(200)

        self.confirmarContraseña = CampoCoincidenteContraseña_Validacion(self.contraseña).setMaxCar(200)

class Formulario_EditarUsuario(FormularioConValidacion):
    def inicializarCampos(self):
        MIN_CARACTERES = 5
        MIN_CARACTERES_NOMBRE = 4
        MAX_CARACTERES = 50
        MIN_CARACTERES_CORREO = 10
        MAX_CARACTERES_CORREO = 100

        self.id = CampoConValidacionPost()
        self.id.addTipoDeValidacion(lambda id: bd.existeUsuario_id(id),
                                         "No existe este usuario ")
        self.nombre=CampoSoloLetras_Validacion()
        self.nombre.setMaxCar(MAX_CARACTERES).setMinCar(MIN_CARACTERES_NOMBRE)

        self.apellidos = CampoSoloLetras_Validacion()
        self.apellidos.setMaxCar(MAX_CARACTERES).setMinCar(MIN_CARACTERES)



        self.correo=CampoCorreo_Validacion()
        self.correo.setMaxCar(MAX_CARACTERES_CORREO).setMinCar(MIN_CARACTERES_CORREO)

        self.permisosDeUsuario=CampoSelecionar_Validacion(["1","2","3"])

        self.activo=CampoCB_Validacion()

# class Formulario_EnFaseTerminadoEntrenamiento(FormularioConValidacion):
#     def inicializarCampos(self):
#         se


class Formulario_EditarDataset(FormularioConValidacion):
    # def __init__(self,idDataset):
    #     self.idDataset=idDataset
    #     FormularioConValidacion.__init__(self)
    def inicializarCampos(self):
        MIN_CARACTERES = 5
        MAX_CARACTERES = 50

        self.id = CampoConValidacionPost()
        self.id.addTipoDeValidacion(lambda id: bd.existeDataset_ID(id),
                                    "No existe este dataset ")

        def validarNombre(nombre):
            #dataset=bd.getDataset_id(self.idDataset)
            dataset = bd.getDataset_id(self.id.valor)
            if nombre==dataset.Nombre:
                return True
            return (not bd.existeDataset_Nombre(nombre)) and (not nombre in logicaUploadDataset.getListaDeNombresDeDatasetEnProceso())

        self.nombre=CampoConAlfanumericos_Validacion()
        #self.nombre.addTipoDeValidacion(lambda v:(not bd.existeDataset_Nombre(v)) and (not v in logicaUploadDataset.getListaDeNombresDeDatasetEnProceso()),"Ya existe un dataset con este nombre ")
        self.nombre.addTipoDeValidacion(validarNombre,
                                        "Ya existe un dataset con este nombre ")
        self.nombre.setMaxCar(MAX_CARACTERES).setMinCar(MIN_CARACTERES)

        self.descripcion=CampoConValidacionPost()

        self.tipoDeFruto=CampoConValidacionPost()
        self.tipoDeFruto.addTipoDeValidacion(
            lambda v: bd.existeFruto_id(v)
            , "No existe este fruto")
        # self.tipoDeFruto.setMaxCar(MAX_CARACTERES).setMinCar(MIN_CARACTERES)


class Formulario_EditarModeloNeuronal(FormularioConValidacion):
    def inicializarCampos(self):
        MIN_CARACTERES = 5
        MAX_CARACTERES = 50

        self.id = CampoConValidacionPost()
        self.id.addTipoDeValidacion(lambda id: bd.existeModeloNeuronal_ID(id),
                                    "No existe este modelo ")

        def validarNombre(nombre):
            modelo = bd.getModeloNeuronal_id(self.id.valor)
            if nombre==modelo.Nombre:
                return True
            return (not bd.existeModeloNeuronal_Nombre(nombre)) and (not nombre in logicaDeEntrenamiento.getListaDeNombresDeModeloEnProceso())

        self.nombre = CampoConAlfanumericos_Validacion()

        self.nombre.addTipoDeValidacion(validarNombre,
                                        "Ya existe un modelo neuronal con este nombre ")
        self.nombre.setMaxCar(MAX_CARACTERES).setMinCar(MIN_CARACTERES)

        self.descripcion=CampoConValidacionPost()

        # self.tipoDeFruto=CampoConAlfanumericos_Validacion()
        # self.tipoDeFruto.setMaxCar(MAX_CARACTERES).setMinCar(MIN_CARACTERES)


class Formulario_AgregarTipoDeFruto(FormularioConValidacion):
    def inicializarCampos(self):
        MIN_CARACTERES = 4
        MAX_CARACTERES = 50
        self.nombre = CampoConAlfanumericos_Validacion()

        self.nombre.setMaxCar(MAX_CARACTERES).setMinCar(MIN_CARACTERES)

        self.variedad = CampoConAlfanumericos_Validacion()
        self.variedad.addTipoDeValidacion(lambda v: not bd.existeFruto_Nombre_Variedad(nombre=self.nombre.valor
                                                                                       ,variedad=v)
                                        , "Ya existe un fruto de esta variedad ")

        self.nombreCientifico = CampoConAlfanumericos_Validacion().setNombre("Nombre Científico")
        self.nombreCientifico.addTipoDeValidacion(
            lambda v: not bd.existeFruto_NombreCientifico(nombreCientifico=v)
                                          , "Ya existe un fruto con este nombre ")

        self.descripcion = CampoConValidacionPost()

        self.nombreImagen=CampoDireccionImagen_JPG_JPEG_PNG_Validacion()

        self.ArchivoImagen=CampoConValidacionImagenJPG_JPEG_PNG()


class Formulario_EditarTipoDeFruto(FormularioConValidacion):
    def inicializarCampos(self):
        MIN_CARACTERES = 4
        MAX_CARACTERES = 50

        self.id = CampoConValidacionPost()
        self.id.addTipoDeValidacion(lambda id: bd.existeFruto_id(id),
                                    "No existe este fruto ")

        self.nombre = CampoConAlfanumericos_Validacion()

        self.nombre.setMaxCar(MAX_CARACTERES).setMinCar(MIN_CARACTERES)

        self.variedad = CampoConAlfanumericos_Validacion()
        def validarVariedad(v):
            fruto=bd.getFruto_id(self.id.valor)
            if self.nombre.valor==fruto.Nombre and v==fruto.Variedad:
                return True
            return not bd.existeFruto_Nombre_Variedad(nombre=self.nombre.valor,variedad=v)
        self.variedad.addTipoDeValidacion(validarVariedad
                                        , "Ya existe un fruto de esta variedad ")

        self.nombreCientifico = CampoConAlfanumericos_Validacion().setNombre("Nombre Científico")
        def validarNombreCientifico(nombreCientifico):
            fruto = bd.getFruto_id(self.id.valor)
            if nombreCientifico == fruto.NombreCientifico:
                return True
            return not bd.existeFruto_NombreCientifico(nombreCientifico=nombreCientifico)
        self.nombreCientifico.addTipoDeValidacion(
            validarNombreCientifico
            , "Ya existe un fruto con este nombre ")

        self.descripcion = CampoConValidacionPost()

        self.agregoUnaNuevaImagen=CampoCB_Validacion()

        self.nombreImagen=CampoDireccionImagen_JPG_JPEG_PNG_Validacion().setDependeDeCB(self.agregoUnaNuevaImagen)

        self.ArchivoImagen=CampoConValidacionImagenJPG_JPEG_PNG().setDependeDeCB(self.agregoUnaNuevaImagen)




