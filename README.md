# Clasificación

## Codigo
Clasificando Estilos Musicales
En la carpeta 'Genres' hay sonidos de distintos géneros musicales.

Utilizando los descriptores que considere pertinentes y su clasificador preferido, clasifique dichos audios.

* Para cada estilo utilice el 80% de las muestras para entrenamiento y el 20% para testeo.

* Entregue la matriz de confusión y la accuracy.

* Comente resultados de la matriz de confusión. ¿Para qué géneros funciona mejor?

## Comentarios

X_train 125 <class 'list'>
labels_train 125 classical
X_test 35 <class 'list'>
labels_test 35 classical

Resultados!
 {
  "Nearest Neighbors 1": 91.42857142857143,
  "Nearest Neighbors 3": 88.57142857142857,
  "Nearest Neighbors 5": 88.57142857142857,
  "Linear SVM": 77.14285714285715,
  "RBF SVM": 22.857142857142858,
  "Neural Net": 82.85714285714286
}


Primero, ejecuté el código utilizando sólo descriptores de MFCC. Los resultados son los siguientes:
{
  "Nearest Neighbors 1": 82.85714285714286,
  "Nearest Neighbors 3": 85.71428571428571,
  "Nearest Neighbors 5": 82.85714285714286,
  "Linear SVM": 82.85714285714286,
  "RBF SVM": 37.142857142857146,
  "Neural Net": 94.28571428571428
}

El mejor resultado se obtiene con un clasificador basado en redes
neuronales, pero los otros clasificadores tienen resultados bastantes
aceptables. Por su parte, el SVM de RBF tiene malos resultados.

Las matrices de confusión muestran más detalle de la clasificación empleada.

En segundo lugar ejecuté el programa con todos los descriptores, obteniendo
los siguientes resultados:

{
  "Nearest Neighbors 1": 88.57142857142857,
  "Nearest Neighbors 3": 91.42857142857143,
  "Nearest Neighbors 5": 94.28571428571428,
  "Linear SVM": 82.85714285714286,
  "RBF SVM": 31.428571428571427,
  "Neural Net": 94.28571428571428
}

Obtuve hasta un 94% de accuracy con redes neuronales y knn de 5 vecinos.
Esto significa que se equivocaron en 2 muestras. Revisando las matrices de
confusión, los clasificadores se confundían con las piezas de jazz que
tenían similitud con la música clásica y la reggae, que escuchandolas
personalmente, encontré que se parecian bastante a esos géneros.

## Optimizacion

### Drive
https://drive.google.com/drive/folders/1N63boWb4v69u9w4Ag1wEZWA6jbjf4stg?usp=sharing

### Overleaf
https://www.overleaf.com/project/6150d12b68219ad26af783db
