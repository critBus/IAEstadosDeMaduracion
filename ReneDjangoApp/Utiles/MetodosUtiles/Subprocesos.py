import threading
from multiprocessing import Process
def subproceso(accion):
    p = Process(target=accion, args=())#'bob',
    p.start()
    return p
def detenerSubproceso(subproceso):
    if isinstance(subproceso,Process):
        subproceso.terminate()
def esperar(segundos):
    c = threading.Condition()
    c.acquire()
    c.wait(segundos)
    return c