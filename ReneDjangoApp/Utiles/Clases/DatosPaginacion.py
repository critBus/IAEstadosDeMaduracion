from ReneDjangoApp.Utiles.MetodosUtiles.UtilesDjango import *
class DatosDeIndiceDePaginacion:
    def __init__(self,indice):
        self.indice=indice
        self.enable=True

class DatosPaginacion:

    def __init__(self,indiceActual=1,listaParaPaginar=None,tamañoDeSalto=None):
        """

        :param indiceActual: 1-... comienza en 1
        :param cantidadDeIndices:
        """
        cantidadDeIndices = 1
        if listaParaPaginar is not None and tamañoDeSalto is not None:
            cantidad=len(listaParaPaginar)
            cantidadDeIndices = int(cantidad / tamañoDeSalto)
            if cantidad % tamañoDeSalto != 0:
                cantidadDeIndices += 1


        self.indiceActual=indiceActual
        self.listaDeIndices=[]
        for i in range(cantidadDeIndices):
            d=DatosDeIndiceDePaginacion(i+1)
            self.listaDeIndices.append(d)
            if d.indice==indiceActual:
                d.enable=False
        self.siguiente=cantidadDeIndices>1 and indiceActual<cantidadDeIndices
        self.anterior=indiceActual>1

class ListaDePaginacion:
    def __init__(self):
        self.listaCompleta=None
        self.listaEnPaginacion=None
    def clear(self):
        self.listaCompleta = []
        self.listaEnPaginacion = []



class PaginacionDeSession:
    NOMBRE_FORM_PAGINACION = 'nombre_formulario_paginacion'
    KEY_INDICE_PAGINACION = "paginacionKey"
    VALOR_PAGINACION_ANTERIOR = 'anterior'
    VALOR_PAGINACION_SIGUIENTE = 'siguiente'

    def __init__(self,app_config,cantidadMaximaAMostrar,crearListaCompleta):#,accionSiHayIndice,accionAntesDeRealizarPostPaginacion=None
        self.app_config=app_config
        self.crearListaCompleta=crearListaCompleta# request->lista
        #self.accionSiNoHayIndice=accionSiNoHayIndice# (request)->lista
        #self.accionSiHayIndice=accionSiHayIndice# (request)->lista
        self.cantidadMaximaAMostrar=cantidadMaximaAMostrar
        self.datosPaginacion = None
        self.__lista:ListaDePaginacion=ListaDePaginacion()
        self.indiceDefault=1
        #self.accionAntesDeRealizarPostPaginacion=accionAntesDeRealizarPostPaginacion# (request,lista)->lista
    def __getPorcionListaDefault(self,lista):
        lista = lista[:self.cantidadMaximaAMostrar]
        return lista

    def getLista(self,request):
        if self.__lista.listaCompleta is None:
            self.__lista.listaCompleta=self.crearListaCompleta(request)
            self.__lista.listaEnPaginacion=self.__getPorcionListaDefault(self.__lista.listaCompleta)
        return self.__lista

    def getListaPaginada(self,request):
        return self.getLista(request).listaEnPaginacion
    def getDatosPaginacion(self,request):
        if self.datosPaginacion is None:

            self.datosPaginacion=DatosPaginacion(self.indiceDefault, self.getLista(request).listaCompleta, self.cantidadMaximaAMostrar)
        return self.datosPaginacion
    def putSessionIndicePaginacionDefault(self,request):
        self.putSessionIndicePaginacion(request, self.indiceDefault)
    def getSessionIndicePaginacion(self,request):
        try:
            indicePaginacion=getSesInt(request,self.KEY_INDICE_PAGINACION)
            return indicePaginacion
        except:
            self.putSessionIndicePaginacionDefault(request)
            return self.indiceDefault
    def putSessionIndicePaginacion(self,request,indice):
        putSes(request, self.KEY_INDICE_PAGINACION, indice)

    def realizarPagincacionDeSerNecesario(self,request):
        indicePaginacion = self.getSessionIndicePaginacion(request)
        #l =self.crearListaCompleta(request)
        l=self.getLista(request).listaCompleta
        if indicePaginacion > self.indiceDefault:
            if (len(l) + 1) < (indicePaginacion * self.cantidadMaximaAMostrar - 1):
                # print("no crear paginacion !!!!!!!!!!!!!!!!!!!!!!!!!!!")
                l = []
                self.putSessionIndicePaginacionDefault(request)
            else:
                # print("realizar recorte paginacion !!!!!!!!!!!!!!!!!!!!")
                self.datosPaginacion = DatosPaginacion(indicePaginacion, l, self.cantidadMaximaAMostrar)
                l = l[(indicePaginacion - 1) * self.cantidadMaximaAMostrar:(indicePaginacion) * self.cantidadMaximaAMostrar]

        else:
            # print("porcion default !!!!!!!!!!!!!!!")
            l =self.__getPorcionListaDefault(l)
        self.getLista(request).listaEnPaginacion = l
        return l
    def getListaConPaginacionDefault(self,request):
        self.putSessionIndicePaginacionDefault(request)
        # l = self.crearListaCompleta(request)
        # l = self.__getPorcionListaDefault(l)
        # self.lista=l
        return self.getListaPaginada(request)

    def isPostPaginacion(self,request):
        if self.app_config.isPost(request,self.NOMBRE_FORM_PAGINACION):
            postPaginicacion = getPost(request, self.KEY_INDICE_PAGINACION)

            if postPaginicacion==self.VALOR_PAGINACION_ANTERIOR:
                indicePaginacion = self.getSessionIndicePaginacion(request)
                if indicePaginacion>self.indiceDefault:
                    indicePaginacion-=1
            elif postPaginicacion==self.VALOR_PAGINACION_SIGUIENTE:
                #print("fue siguiente !!!!!!!!!!!!!!!1")
                indicePaginacion = self.getSessionIndicePaginacion(request)
                indicePaginacion+=1
            else:
                indicePaginacion = int(postPaginicacion)
            #print("indicePaginacion =",indicePaginacion," !!!!!!!!!!!!!")
            self.putSessionIndicePaginacion(request, indicePaginacion)
            self.realizarPagincacionDeSerNecesario(request)
            return True
        return False



class PaginacionSimple:
    def __init__(self,indiceActual,cantidadDeElementos,step,cantidadDeIndicesAMostrarMaximo):
        """
        va intentar poner el indice actual en el medio
        :param indiceActual: 1-... comienza en 1
        :param cantidadDeElementos:
        :param step:
        :param cantidadDeIndicesAMostrarMaximo: 3-....  3 como minimo
        """
        cantidadDeIndices = int(cantidadDeElementos / step)
        if cantidadDeElementos % step != 0:
            cantidadDeIndices += 1

        #self.listaDeIndices=[i for i in range(1,cantidadDeIndices+1)]
        cantidadDeIndicesALosLados=cantidadDeIndicesAMostrarMaximo-1
        if cantidadDeIndicesAMostrarMaximo>2:
            cantidadDeIndicesALosLados=int((cantidadDeIndicesAMostrarMaximo-1)/2)

        #print(cantidadDeIndices)
        self.listaDeIndices=[]
        self.iActual=-1
        if cantidadDeIndices>0 and indiceActual<=cantidadDeIndices:
            if cantidadDeIndices==1 and indiceActual==1:
                self.listaDeIndices=[1]
                self.iActual=0
            else:
                la = []
                ls = []
                indiceAnterior=-1
                indiceSiguiente=-1
                while (len(la)+len(ls)+1)<cantidadDeIndicesAMostrarMaximo\
                        and (len(la)+len(ls)+1)<cantidadDeIndices:
                    if indiceActual>1:
                        if indiceAnterior==-1:
                            indiceAnterior=indiceActual-1
                            la.append(indiceAnterior)
                        elif indiceAnterior>1:
                            indiceAnterior = indiceAnterior - 1
                            la.append(indiceAnterior)
                    if indiceActual<cantidadDeIndices:
                        if indiceSiguiente==-1:
                            indiceSiguiente=indiceActual+1
                            ls.append(indiceSiguiente)
                        elif indiceSiguiente<cantidadDeIndices:
                            indiceSiguiente = indiceSiguiente + 1
                            ls.append(indiceSiguiente)
                la.reverse()
                self.listaDeIndices.extend(la)
                self.listaDeIndices.append(indiceActual)
                #ls.reverse()
                self.listaDeIndices.extend(ls)
                self.iActual = len(la)

    def __str__(self):
        return str(self.listaDeIndices)+"  "+str(self.iActual)

        # li=[]
        # if cantidadDeIndices>indiceActual:
        #     pass
        # else cantidadDeIndices==
        #if indiceActual>1:



