import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix


def confusionMatrix(Y_pred, labels_test, name='', classes=[]):
    '''
    Función basada en la solución mostrada en:
    https://stackoverflow.com/questions/35572000/how-can-i-plot-a-confusion-matrix
    '''
    df_cm = pd.DataFrame(confusion_matrix(Y_pred, labels_test),
                         classes, classes)
    plt.figure(figsize=(10, 7))
    sn.set(font_scale=1.4)
    sn.heatmap(df_cm, annot=True, annot_kws={'size': 20}, cmap='YlGnBu',
               fmt='g')
    plt.title(f'Resultados de {name}')
    plt.xlabel('Valores predecidos')
    plt.ylabel('Valores reales')


def performance(Y_pred, labels_test):
    return (Y_pred == labels_test).sum() / len(Y_pred)


if __name__ == '__main__':
    mod = '''
    8. Medición de desempeño
    '''
    print(mod)
