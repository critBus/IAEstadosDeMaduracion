# Generated by Django 3.2.11 on 2022-10-29 19:11

import ReneDjangoApp.Utiles.MetodosUtiles.ValidacionesModelosDj
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Direccion_Imagenes_Procesadas', models.CharField(max_length=256, unique=True, validators=[ReneDjangoApp.Utiles.MetodosUtiles.ValidacionesModelosDj.validar_direccion])),
                ('Direccion_Imagenes_Originales', models.CharField(max_length=256, unique=True, validators=[ReneDjangoApp.Utiles.MetodosUtiles.ValidacionesModelosDj.validar_direccion])),
                ('Nombre', models.CharField(max_length=50, unique=True)),
                ('FechaDeCreacion', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creacion')),
                ('Descripcion', models.TextField()),
                ('CantidadDeImagenes', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Dataset',
                'verbose_name_plural': 'Datasets',
            },
        ),
        migrations.CreateModel(
            name='Entrenamiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Total_De_Epocas', models.IntegerField()),
                ('Fecha_de_Realizacion', models.DateTimeField(auto_now_add=True)),
                ('Dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Aplicacion.dataset')),
            ],
            options={
                'verbose_name': 'Entrenamiento',
                'verbose_name_plural': 'Entrenamientos',
            },
        ),
        migrations.CreateModel(
            name='Fruto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nombre', models.CharField(max_length=50)),
                ('NombreCientifico', models.CharField(max_length=50, unique=True)),
                ('Variedad', models.CharField(max_length=50)),
                ('Descripcion', models.TextField()),
                ('DireccionImagen', models.CharField(max_length=256)),
                ('Fecha', models.DateTimeField(auto_now_add=True, verbose_name='Ultima Modificacion')),
            ],
            options={
                'verbose_name': 'Fruto',
                'verbose_name_plural': 'Frutos',
            },
        ),
        migrations.CreateModel(
            name='ModeloNeuronal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Direccion', models.CharField(max_length=256, unique=True, validators=[ReneDjangoApp.Utiles.MetodosUtiles.ValidacionesModelosDj.validar_direccion])),
                ('Nombre', models.CharField(max_length=50, unique=True)),
                ('FechaDeCreacion', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creacion')),
                ('Descripcion', models.TextField()),
                ('Precision', models.FloatField()),
                ('Perdida', models.FloatField()),
                ('CantidadDeEpocas', models.IntegerField()),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Modelo Neuronal',
                'verbose_name_plural': 'Modelos Neuronales',
            },
        ),
        migrations.CreateModel(
            name='ProcesamientoDeImagen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ImagenOriginal', models.ImageField(upload_to='Aplicacion/static/img/temp')),
                ('Fecha', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Procesamiento De Imagen',
                'verbose_name_plural': 'Procesamientos De Imagenes',
            },
        ),
        migrations.CreateModel(
            name='Validacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Precision', models.FloatField()),
                ('Porcentaje_Utilizado_Del_Dataset', models.IntegerField()),
                ('Fecha_de_Realizacion', models.DateTimeField(auto_now_add=True)),
                ('Dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Aplicacion.dataset')),
                ('ModeloNeuronal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Aplicacion.modeloneuronal', verbose_name='Modelo Neuronal')),
            ],
            options={
                'verbose_name': 'Validación',
                'verbose_name_plural': 'Validaciones',
            },
        ),
        migrations.CreateModel(
            name='ImagenProcesada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ImagenResultante', models.ImageField(upload_to='Aplicacion/static/img/temp')),
                ('Tipo', models.CharField(max_length=50)),
                ('AlgoritmoUtilizado', models.CharField(max_length=50, verbose_name='Algoritmo Utilizado')),
                ('Fecha', models.DateTimeField(auto_now_add=True)),
                ('ProcesamientoDeImagen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Aplicacion.procesamientodeimagen', verbose_name='Procesamiento De Imagen')),
            ],
            options={
                'verbose_name': 'Imagen Procesada',
                'verbose_name_plural': 'Imagenes Procesadas',
            },
        ),
        migrations.CreateModel(
            name='Epoca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Numero_De_Epoca', models.IntegerField()),
                ('Total_De_Lotes', models.IntegerField()),
                ('Precision', models.FloatField()),
                ('Perdida', models.FloatField()),
                ('Entrenamiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Aplicacion.entrenamiento')),
            ],
            options={
                'verbose_name': 'Epoca',
                'verbose_name_plural': 'Epocas',
            },
        ),
        migrations.AddField(
            model_name='entrenamiento',
            name='ModeloNeuronal',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Aplicacion.modeloneuronal', verbose_name='Modelo Neuronal'),
        ),
        migrations.CreateModel(
            name='DatoEnMatrizDeConfusion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Clasificacion_predicha', models.CharField(max_length=50)),
                ('Clasificacion_real', models.CharField(max_length=50)),
                ('Indice_columna', models.IntegerField()),
                ('Indice_fila', models.IntegerField()),
                ('Cantidad', models.IntegerField()),
                ('Validacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Aplicacion.validacion', verbose_name='Validación')),
            ],
            options={
                'verbose_name': 'Dato En Matriz De Confusión',
                'verbose_name_plural': 'Datos En Matriz De Confusión',
            },
        ),
        migrations.CreateModel(
            name='DatoEnHistorialDeEntrenamiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Lote', models.IntegerField()),
                ('Precision', models.FloatField()),
                ('Perdida', models.FloatField()),
                ('Epoca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Aplicacion.epoca', verbose_name='Modelo Neuronal')),
            ],
            options={
                'verbose_name': 'Dato En Historial De Entrenamiento',
                'verbose_name_plural': 'Datos En Historial De Entrenamiento',
            },
        ),
        migrations.AddField(
            model_name='dataset',
            name='Fruto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Aplicacion.fruto'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='User',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Clasificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Fecha', models.DateTimeField(auto_now_add=True)),
                ('Resultado', models.CharField(max_length=50)),
                ('Username', models.CharField(max_length=256)),
                ('IP_Usuario', models.CharField(max_length=50)),
                ('ImagenProcesada', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Aplicacion.imagenprocesada')),
                ('ModeloNeuronal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Aplicacion.modeloneuronal', verbose_name='Modelo Neuronal')),
                ('Procesamiento', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Aplicacion.procesamientodeimagen')),
            ],
            options={
                'verbose_name': 'Clasificacion',
                'verbose_name_plural': 'Clasificaciones',
            },
        ),
        migrations.CreateModel(
            name='ClaseDeClasificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nombre', models.CharField(max_length=50)),
                ('NombreCarpetaCorrespondiente', models.CharField(max_length=50)),
                ('Indice', models.IntegerField()),
                ('Indice_De_Carpeta', models.IntegerField()),
                ('CantidadDeImagenes', models.IntegerField()),
                ('Descripcion', models.TextField()),
                ('Dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Aplicacion.dataset')),
            ],
            options={
                'verbose_name': 'Clase De Clasificación',
                'verbose_name_plural': 'Clases De Clasificaciones',
            },
        ),
    ]
