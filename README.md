# IAEstadosDeMaduracion
Sitio web para la clasificación de frutos según su estado de maduración y el entrenamiento de modelos nueronales que ofrescan este servicio mediante nuevos datasets, basado en CNN, creada en Django, y con TensorFlow, scikit-learn  y OpenCV 


IAEstadosDeMaduracion es una plataforma web completa en Django, diseñada para proporcionar una plataforma de entrenamiento de sistemas de visión por computadoras basados en redes convolucionales. Esta herramienta permite a los usuarios almacenar y gestionar datasets de imágenes de frutos, que posteriormente pueden ser utilizados para el entrenamiento de una red neuronal convolucional.

La interfaz de esta plataforma web es muy cómoda y ofrece múltiples opciones de configuración para el entrenamiento de la red neuronal. Estas opciones permiten limitar el número máximo de épocas para el entrenamiento, almacenar solo el mejor modelo obtenido y detener el entrenamiento al alcanzar cierto límite de precisión. Durante el proceso de entrenamiento, IA Estados de Maduración proporciona gráficos que muestran la estadística del progreso, como la precisión y la pérdida.

Al finalizar el entrenamiento, se muestra una matriz de confusión que presenta la precisión real del modelo neuronal resultante. Una vez que se han creado varios modelos neuronales para diferentes tipos de frutos, la plataforma permite a los usuarios clasificar automáticamente sus imágenes utilizando el modelo neuronal que mejor precisión haya alcanzado para su tipo de fruto.

Esta herramienta es una excelente opción para evaluar la calidad de los sembrados de campos agrícolas, ya que no se requiere sacrificar una parte de la producción en el proceso. Es una herramienta útil para científicos, agricultores y cualquier persona interesada en clasificar imágenes de frutos según sus estados de madurez.

