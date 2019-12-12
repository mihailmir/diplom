import matplotlib.pyplot as plt
from pywaffle import Waffle
from config import INPUT_PARAMETERS
import numpy as np


def plot_waffle(dataset, class_encoder):
    df = dataset.groupby('class').size().reset_index(name='counts')
    n_categories = df.shape[0]
    colors = [plt.cm.inferno_r(i / float(n_categories)) for i in range(n_categories)]
    plt.figure(
        FigureClass=Waffle,
        plots={
            '111': {
                'values': df['counts'],
                'labels': ["Клас - {0}, кількість - {1} ".format(class_encoder.inverse_transform([n[1]])[-1], n[2]) for
                           n in df[['class', 'counts']].itertuples()],
                'legend': {'loc': 'upper left', 'bbox_to_anchor': (1.05, 1), 'fontsize': 12},
                'title': {'label': '# Vehicles by Class', 'loc': 'center', 'fontsize': 18}
            },
        },
        rows=20,
        colors=colors,
        figsize=(16, 9)
    )
    plt.show()


def plot_loss_acc(dataset):
    plt.title('Loss / Mean Squared Error')
    plt.plot(dataset['loss'], label='loss')
    plt.plot(dataset['acc'], label='acc')
    plt.legend()
    plt.show()


def plot_feature_importances_(model):
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    input_params = INPUT_PARAMETERS.copy()
    input_params.remove('class')
    plt.figure()
    plt.title("Feature importances")
    names_indices = ['x_coor', 'y_coor']
    names_indices = [param for param in input_params]
    plt.bar(range(len(importances)), importances, color="r")
    plt.xticks(range(len(importances)), names_indices, rotation=90)

    plt.tight_layout()
    plt.xlim([-1, len(importances)])
    plt.show()
