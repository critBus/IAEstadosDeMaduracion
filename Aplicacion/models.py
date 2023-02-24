from django.db import models
from  django.utils import timezone
from django.contrib.auth import get_user_model
from django.conf import settings

from Aplicacion.UtilesAplicacion.ConstantesApp import APP_CNF

from django import forms

from ReneDjangoApp.Utiles.Utiles import *

class Fruto(models.Model):
    class Meta:
        verbose_name='Fruto'
        verbose_name_plural='Frutos'
    Nombre=models.CharField(max_length=50)
    NombreCientifico = models.CharField(max_length=50,unique=True)
    Variedad=models.CharField(max_length=50)
    Descripcion = models.TextField()
    DireccionImagen=models.CharField(max_length=256)
    Fecha=models.DateTimeField(auto_now_add=True,verbose_name="Ultima Modificacion")

    def __str__(self):
        return self.Nombre+" - "+self.Variedad

class ClaseDeClasificacion(models.Model):
    class Meta:
        verbose_name='Clase De Clasificación'
        verbose_name_plural='Clases De Clasificaciones'
    Nombre = models.CharField(max_length=50)
    NombreCarpetaCorrespondiente = models.CharField(max_length=50)
    Indice = models.IntegerField()
    Indice_De_Carpeta = models.IntegerField()
    CantidadDeImagenes = models.IntegerField()
    Descripcion = models.TextField()
    Dataset = models.ForeignKey(
        'Dataset',
        on_delete=models.CASCADE,
    )
    def __str__(self):
        return self.Nombre+" - "+ self.Dataset.Fruto.Nombre +" - "+ self.Dataset.Nombre

class Dataset(models.Model):
    class Meta:
        verbose_name='Dataset'
        verbose_name_plural='Datasets'
    Direccion_Imagenes_Procesadas = models.CharField(max_length=256, validators=[ValidacionesModelosDj.validar_direccion],unique=True)
    Direccion_Imagenes_Originales = models.CharField(max_length=256,
                                                     validators=[ValidacionesModelosDj.validar_direccion],unique=True)
    Nombre = models.CharField(max_length=50, unique=True)
    FechaDeCreacion = models.DateTimeField(auto_now_add=True,verbose_name="Fecha de Creacion")
    Descripcion = models.TextField()
    CantidadDeImagenes=models.IntegerField()
    #Fruto=models.CharField(max_length=50, )
    User = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    Fruto = models.ForeignKey(
        'Fruto',
        on_delete=models.CASCADE,

    )
    def __str__(self):
        return self.Nombre




class ModeloNeuronal(models.Model):
    class Meta:
        verbose_name='Modelo Neuronal'
        verbose_name_plural='Modelos Neuronales'
    Direccion = models.CharField(max_length=256,validators=[ValidacionesModelosDj.validar_direccion],unique=True)
    Nombre = models.CharField(max_length=50,unique=True)
    #Fruto=models.CharField(max_length=50, )
    User = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    # Dataset = models.ForeignKey(
    #     'Dataset',
    #     on_delete=models.CASCADE,
    # )
    FechaDeCreacion = models.DateTimeField(auto_now_add=True,verbose_name="Fecha de Creacion")
    Descripcion = models.TextField()
    Precision = models.FloatField()
    Perdida = models.FloatField()
    CantidadDeEpocas = models.IntegerField()

    def __str__(self):
        return self.Nombre



class Entrenamiento(models.Model):
    class Meta:
        verbose_name='Entrenamiento'
        verbose_name_plural='Entrenamientos'
    Total_De_Epocas = models.IntegerField()
    Fecha_de_Realizacion = models.DateTimeField(auto_now_add=True)
    ModeloNeuronal = models.OneToOneField(
        'ModeloNeuronal',
        on_delete=models.CASCADE,
        verbose_name="Modelo Neuronal"
        #,unique = True
    )
    Dataset = models.ForeignKey(
        'Dataset',
        on_delete=models.CASCADE,

    )

    def __str__(self):
        return str(self.Dataset.Nombre) + " Dataset: " + str(self.Dataset.Nombre) + " Modelo: " + str(
            self.ModeloNeuronal.Nombre) + " - " + str(self.Fecha_de_Realizacion)


class Epoca(models.Model):
    class Meta:
        verbose_name='Epoca'
        verbose_name_plural='Epocas'

    Numero_De_Epoca = models.IntegerField()
    Total_De_Lotes = models.IntegerField()
    Precision = models.FloatField()
    Perdida = models.FloatField()
    Entrenamiento = models.ForeignKey(
        'Entrenamiento',
        on_delete=models.CASCADE,
    )
    def __str__(self):
        return " Epoca: "+str(self.Numero_De_Epoca)+" - "+str(self.Entrenamiento)
class DatoEnHistorialDeEntrenamiento(models.Model):
    class Meta:
        verbose_name='Dato En Historial De Entrenamiento'
        verbose_name_plural='Datos En Historial De Entrenamiento'

    Epoca = models.ForeignKey(
        'Epoca',
        on_delete=models.CASCADE,
        verbose_name="Modelo Neuronal"
    )
    Lote = models.IntegerField()
    Precision = models.FloatField()
    Perdida = models.FloatField()
    def __str__(self):
        return " Epoca: "+str(self.Epoca)+" Lote: "+str(self.Lote)+" Precision: "+str(self.Precision)

class Validacion(models.Model):
    class Meta:
        verbose_name = 'Validación'
        verbose_name_plural = 'Validaciones'
    Precision = models.FloatField()
    Porcentaje_Utilizado_Del_Dataset = models.IntegerField()
    Fecha_de_Realizacion = models.DateTimeField(auto_now_add=True)
    ModeloNeuronal = models.ForeignKey(
        'ModeloNeuronal',
        on_delete=models.CASCADE,
        verbose_name="Modelo Neuronal"
    )
    Dataset = models.ForeignKey(
        'Dataset',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.Dataset.Nombre)+" Dataset: "+str(self.Dataset.Nombre)+" Modelo: "+str(self.ModeloNeuronal.Nombre)+" - "+str(self.Fecha_de_Realizacion)

class DatoEnMatrizDeConfusion(models.Model):
    class Meta:
        verbose_name='Dato En Matriz De Confusión'
        verbose_name_plural='Datos En Matriz De Confusión'
    Clasificacion_predicha = models.CharField(max_length=50)
    Clasificacion_real = models.CharField(max_length=50)
    Indice_columna = models.IntegerField()
    Indice_fila = models.IntegerField()
    Cantidad = models.IntegerField()
    Validacion = models.ForeignKey(
        'Validacion',
        on_delete=models.CASCADE,
        verbose_name="Validación"
    )
    def __str__(self):
        return self.Clasificacion_real+" fila: "+str(self.Indice_fila)+" , "+ self.Clasificacion_predicha+" columna: "+str(self.Indice_columna)+" cantidad: "+str(self.Cantidad)



class ProcesamientoDeImagen(models.Model):
    class Meta:
        verbose_name='Procesamiento De Imagen'
        verbose_name_plural='Procesamientos De Imagenes'
    ImagenOriginal = models.ImageField(upload_to=APP_CNF.getRutaCarpetaImg())
    # User = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE,
    # )
    Fecha = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "nada por ahora"
        #return str(self.id)
class ImagenProcesada(models.Model):
    class Meta:
        verbose_name='Imagen Procesada'
        verbose_name_plural='Imagenes Procesadas'
    ImagenResultante = models.ImageField(upload_to=APP_CNF.getRutaCarpetaImg())
    ProcesamientoDeImagen = models.ForeignKey(
        'ProcesamientoDeImagen',
        on_delete=models.CASCADE,
        verbose_name="Procesamiento De Imagen"
    )
    Tipo = models.CharField(max_length=50)
    AlgoritmoUtilizado = models.CharField(max_length=50,verbose_name="Algoritmo Utilizado")
    Fecha = models.DateTimeField(auto_now_add=True)

class Clasificacion(models.Model):
    class Meta:
        verbose_name='Clasificacion'
        verbose_name_plural='Clasificaciones'
    ImagenProcesada = models.OneToOneField(
        'ImagenProcesada',
        on_delete=models.CASCADE,
    )
    Procesamiento = models.OneToOneField(
        'ProcesamientoDeImagen',
        on_delete=models.CASCADE,
    )
    Fecha = models.DateTimeField(auto_now_add=True)
    Resultado = models.CharField(max_length=50)
    # User = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE,
    # )
    Username= models.CharField(max_length=256)
    IP_Usuario= models.CharField(max_length=50)

    ModeloNeuronal = models.ForeignKey(
        'ModeloNeuronal',
        on_delete=models.CASCADE,
        verbose_name="Modelo Neuronal"
    )


#
# # Create your models here.
