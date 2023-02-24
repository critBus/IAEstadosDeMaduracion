from typing import TYPE_CHECKING, Dict, List, NoReturn, Optional, Union, Tuple, cast, ClassVar
class ElementoDeLocalizacionDePagina:
    def __init__(self,nombre):
        self.nombre=nombre
        self.tieneLink=False
        self.link=None
        self.esElUltimo=False
class LocalizacionDePagina:
    def __init__(self,*a):
        self.listaLocalizacion:List[ElementoDeLocalizacionDePagina]=[]
        leng=len(a)
        for i in range(leng):
            e=ElementoDeLocalizacionDePagina(str(a[i]))
            if i==leng-1:
                e.esElUltimo=True
            self.listaLocalizacion.append(e)