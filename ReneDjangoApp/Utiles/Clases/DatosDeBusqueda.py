class DatosDeBusqueda:
    def __init__(self):
        self.seMuestranResultadosDeBusqueda=False
        self.textoBuscado=""
    def seBuscoSobre(self,textoBuscado):
        self.textoBuscado=textoBuscado
        self.seMuestranResultadosDeBusqueda=True