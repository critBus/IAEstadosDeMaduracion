from ReneDjangoApp.Utiles.MetodosUtiles.UtilesDjango import getUsernameRequest
class DatosEnMemoria:
    def __init__(self):
        self.__memoria={}
    def __getDicUser(self,request):
        username=getUsernameRequest(request)
        if not username in self.__memoria:
            self.__memoria[username]={}
        return self.__memoria[username]


    def get(self,request,key,porDefecto=None):
        dic=self.__getDicUser(request)
        if not key in dic:
            dic[key]=porDefecto
            return porDefecto
        return dic[key]
    def put(self,request,key,value):
        dic = self.__getDicUser(request)
        dic[key]=value