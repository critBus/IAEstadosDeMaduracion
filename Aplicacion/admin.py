from django.contrib import admin
from Aplicacion.models import *

# Register your models here.
class VistaFruto(admin.ModelAdmin):
    list_display = ("Nombre","Variedad","NombreCientifico","Fecha",)
    search_fields = ("Nombre","Variedad","NombreCientifico","Fecha",)
    list_filter =("Nombre",)
    date_hierarchy = "Fecha"



class VistaModeloNeuronal(admin.ModelAdmin):
    list_display = ("Nombre","Precision","User","FechaDeCreacion",)#"Tipo", ,"Direccion"
    search_fields = ("Nombre","User","FechaDeCreacion",)#"Tipo",
    list_filter =("User","FechaDeCreacion",)#"Tipo",
    date_hierarchy = "FechaDeCreacion"

# class VistaImagen(admin.ModelAdmin):
#     list_display = ("Nombre","Formato",)
#     search_fields = ("Nombre","Formato",)
#     list_filter =("Formato",)
#

class VistaClasificacion(admin.ModelAdmin):
    list_display = ("Fecha","Resultado","Username","ModeloNeuronal",)
    search_fields = ("Resultado","Username","ModeloNeuronal",)
    list_filter =("Resultado","Username","ModeloNeuronal","Fecha",)
    date_hierarchy = "Fecha"
class VistaProcesamientoDeImagen(admin.ModelAdmin):
    list_display = ("Fecha",)
    search_fields = ("Fecha",)
    list_filter =("Fecha",)
    date_hierarchy = "Fecha"
class VistaImagenProcesada(admin.ModelAdmin):
    list_display = ("ProcesamientoDeImagen","Tipo","AlgoritmoUtilizado","Fecha",)
    search_fields = ("ProcesamientoDeImagen","Tipo","AlgoritmoUtilizado","Fecha",)
    list_filter =("Tipo","AlgoritmoUtilizado","Fecha",)
    date_hierarchy = "Fecha"
#
# class VistaConfiguracionGeneral(admin.ModelAdmin):
#     list_display = ("DireccionCarpetaModelosNeuronales",)
class VistaClaseDeClasificacion(admin.ModelAdmin):
    list_display = ("Nombre","NombreCarpetaCorrespondiente","Dataset",)
    search_fields = ("Nombre","NombreCarpetaCorrespondiente","Dataset",)
    list_filter = ("Dataset",)
class VistaDataset(admin.ModelAdmin):
    list_display = ("Nombre","Fruto","User","FechaDeCreacion",)
    search_fields = ("Nombre","Fruto","User","FechaDeCreacion",)
    date_hierarchy = "FechaDeCreacion"
    list_filter = ("Fruto","User","FechaDeCreacion",)
#
# class VistaRelacionClasesDeClasificacionYDataset(admin.ModelAdmin):
#     list_display = ("Dataset","ClaseDeClasificacion",)
#     list_filter =("Dataset",)
# class VistaRelacionClasesDeClasificacionYModeloNeuronal(admin.ModelAdmin):
#     list_display = ("ModeloNeuronal","ClaseDeClasificacion",)
#     list_filter =("ModeloNeuronal",)
#
# admin.site.register(RelacionClasesDeClasificacionYModeloNeuronal,VistaRelacionClasesDeClasificacionYModeloNeuronal)
# admin.site.register(RelacionClasesDeClasificacionYDataset,VistaRelacionClasesDeClasificacionYDataset)
admin.site.register(Dataset,VistaDataset)
admin.site.register(ClaseDeClasificacion,VistaClaseDeClasificacion)
# admin.site.register(ConfiguracionGeneral,VistaConfiguracionGeneral)
#
admin.site.register(ModeloNeuronal,VistaModeloNeuronal)
#
admin.site.register(Clasificacion,VistaClasificacion)
admin.site.register(ProcesamientoDeImagen,VistaProcesamientoDeImagen)
admin.site.register(ImagenProcesada,VistaImagenProcesada)


# from Aplicacion.perfiles.misPerfiles import *
# admin.site.register(MySiteProfile)

class VistaEntrenamiento(admin.ModelAdmin):
    list_display = ("ModeloNeuronal","Dataset","Fecha_de_Realizacion",)
    search_fields = ("ModeloNeuronal","Dataset","Fecha_de_Realizacion",)
    list_filter = ("ModeloNeuronal","Dataset","Fecha_de_Realizacion",)
    date_hierarchy = "Fecha_de_Realizacion"

class VistaEpoca(admin.ModelAdmin):
    list_display = ("Numero_De_Epoca","Precision","Entrenamiento",)
    search_fields = ("Numero_De_Epoca","Precision","Entrenamiento",)
    list_filter = ("Entrenamiento",)

class VistaDatoEnHistorialDeEntrenamiento(admin.ModelAdmin):
    list_display = ("Epoca","Lote","Precision",)
    search_fields = ("Epoca","Lote","Precision",)
    list_filter = ("Epoca",)

class VistaValidacion(admin.ModelAdmin):
    list_display = ("ModeloNeuronal","Dataset","Fecha_de_Realizacion",)
    search_fields = ("ModeloNeuronal","Dataset","Fecha_de_Realizacion",)
    list_filter = ("ModeloNeuronal","Dataset","Fecha_de_Realizacion",)
    date_hierarchy = "Fecha_de_Realizacion"



class VistaDatoEnMatrizDeConfusion(admin.ModelAdmin):
    list_display = ("Clasificacion_real","Clasificacion_predicha","Cantidad","Validacion",)
    search_fields = ("Clasificacion_real","Clasificacion_predicha","Cantidad","Validacion",)
    list_filter = ("Clasificacion_real","Clasificacion_predicha","Validacion",)



# admin.site.register(ClaseDeClasificacion)
# admin.site.register(Dataset)
admin.site.register(Validacion,VistaValidacion)
admin.site.register(DatoEnMatrizDeConfusion,VistaDatoEnMatrizDeConfusion)
admin.site.register(Entrenamiento, VistaEntrenamiento)
admin.site.register(Epoca,VistaEpoca)
admin.site.register(DatoEnHistorialDeEntrenamiento,VistaDatoEnHistorialDeEntrenamiento)
admin.site.register(Fruto,VistaFruto)
# admin.site.register(ProcesamientoDeImagen)
# admin.site.register(ImagenProcesada)
# admin.site.register(Clasificacion)
# admin.site.register(ModeloNeuronal)



