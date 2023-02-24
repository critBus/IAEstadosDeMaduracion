import tensorflow as tf
import numpy as np
from keras.models import load_model

def obtenerPrediccion(urlDelModelo,urlImagenProcesada,listaDeNombresDeClases)->str:
    model = load_model(urlDelModelo)
    image=tf.keras.utils.load_img(
        urlImagenProcesada
    )
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])
    predictions = model.predict(input_arr)
    maximo=-9999999999
    clasePredicha=""
    for i in range(len(predictions[0])):
        valorPerdiccion=predictions[0][i]
        if valorPerdiccion>maximo:
            maximo=valorPerdiccion
            clasePredicha=listaDeNombresDeClases[i]
    return clasePredicha
#train_ds.class_names