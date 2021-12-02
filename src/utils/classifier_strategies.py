
# Clasificadores
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

from utils.classifier_performance import performance, confusionMatrix

'''
Las estructuras de las estrategias empleadas se basaron en la estructura de la
actividad en clases:
https://github.com/domingomery/patrones/tree/master/clases/Cap03_Seleccion_de_Caracteristicas/ejercicios/PCA_SFS
'''

# Útiles


def classifier_tests(X_train, labels_train, X_test, labels_test,
                     classes=[]):
    '''
    Rutina de comparación entre distintos clasificadores.

    Código inspirado en:
    https://scikit-learn.org/stable/auto_examples/classification/plot_classifier_comparison.html
    '''

    names = [
        "Nearest Neighbors 1",
        "Nearest Neighbors 3",
        "Nearest Neighbors 5",
        "Linear SVM",
        "RBF SVM",
        "Neural Net"
    ]

    classifiers = [
        KNeighborsClassifier(1),
        KNeighborsClassifier(3),
        KNeighborsClassifier(5),
        SVC(kernel="linear", C=0.025),
        SVC(gamma=2, C=1),
        MLPClassifier(alpha=1, max_iter=1000, random_state=2)
    ]

    results = {}

    # Probamos cada uno de los clasificadores
    for name, classifier in zip(names, classifiers):
        classifier.fit(X_train, labels_train)
        Y_pred = classifier.predict(X_test)
        accuracy = performance(Y_pred, labels_test)
        confusionMatrix(Y_pred, labels_test, name=name, classes=classes)

        results[name] = accuracy*100

    return results
