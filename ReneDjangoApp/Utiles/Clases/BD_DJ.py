from ReneDjangoApp.Utiles.MetodosUtiles.UtilesDjangoUser import *
#username
#password
#email
#first_name
#last_name
class BD_DJ:
    def getModelUser(self):
        return getModelUserDJ()

    def editarUser(self, usuario):
        return editarUserDJ(usuario)

    def saveUser(self, username, password, nombre, apellido, correo,es_de_los_adminstradores=False):
        return saveUserDJ(username, password, nombre, apellido, correo,es_de_los_adminstradores)

    def getUser_id(self, id):
        return getUserDJ_id(id)

    def getUser_username(self, username):
        return getUserDJ_username(username)

    def getUser_All(self):
        return getUserDJ_All()

    def deleteUser(self, usuario):
        deleteUserDJ(usuario)

    def existeUsuario(self, username):
        return existeUsuarioDJ(username)
    def existeUsuario_id(self, id):
        return self.getUser_id(id) is not None

    def cambiarContraseñaUsuario(self,usuario: User, contraseña):
        return cambiarContraseñaUsuarioDJ(usuario,contraseña)