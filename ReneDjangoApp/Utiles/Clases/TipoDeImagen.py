class TipoDeImagen:
    PNG=None
    JPEG=None
    JPG=None
    WEPP=None
    VALUES = None

    def __init__(self, extencion,extencionDesactivada):
        self._extencion = extencion
        self._extencionDesactivada=extencionDesactivada

    def getExtencion(self):
        return self._extencion
    def getExtencionDesactivada(self):
        return self._extencionDesactivada

    def __str__(self):
        return self.getExtencion()

    @staticmethod
    def esTipoDeImagen(a):
        return isinstance(a, TipoDeImagen)

    @staticmethod
    def get(a):
        for i in TipoDeImagen.VALUES:
            if a == i.getExtencion().lower():
                return i
        return None

    @staticmethod
    def pertenece(a):
        return TipoDeImagen.get(a) != None

TipoDeImagen.PNG=TipoDeImagen(".png", ".pn")
TipoDeImagen.JPEG=TipoDeImagen(".jpeg", ".jep")
TipoDeImagen.JPG=TipoDeImagen(".jpg", ".jp")
TipoDeImagen.WEPP=TipoDeImagen(".webp", ".we")
TipoDeImagen.VALUES=[TipoDeImagen.PNG
                     ,TipoDeImagen.JPEG
                     ,TipoDeImagen.JPG
                     ,TipoDeImagen.WEPP]