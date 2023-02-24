from ReneDjangoApp.Utiles.Clases.URL_Constants import URL_Constants

class DatosFormularioLoguin:
    def __init__(self):
        self.nombre_form_loguin="formulario_loguin"
        self.nombre_campo_username="username_campo"
        self.nombre_campo_password = "password_campo"
        self.hay_errores=False
        self.mensaje_de_error="Usuario o contraseña incorrectos"
        self.url_loguin=URL_Constants.URL_VISTA_LOGUIN




    def setFalloDeLoguin(self):
        self.hay_errores=True
    # def getDic(self):
    #     return {'formulario_loguin':self.nombre_form_loguin
    #             ,'username_campo':self.nombre_campo_username
    #             ,''}