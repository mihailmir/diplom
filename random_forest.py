from config import SQLITE_DB, INPUT_PARAMETERS, ENCODERS
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from plot import plot_waffle, plot_feature_importances_
import numpy as np
import argparse
import pandas as pd


def random_forest_cl(path):
    data_vehicle = pd.read_sql("SELECT {} FROM cars".format(', '.join(INPUT_PARAMETERS)), con=SQLITE_DB)
    encoders = ENCODERS.copy()
    for col in data_vehicle.columns:
        data_vehicle[col] = encoders[col].fit_transform(data_vehicle[col])

    model = RandomForestClassifier()
    X_train, X_test, y_train, y_test = train_test_split(data_vehicle.values[::, 0:6], data_vehicle.values[::, 6:7],
                                                        test_size=0.2)
    model.fit(X_train, y_train)

    input_params = INPUT_PARAMETERS.copy()
    input_params.remove('class')
    data = pd.read_csv(path, dtype={param: np.object for param in input_params})

    for param in data.head():
        data[param] = encoders[param].transform(data[param])

    class_encoder = encoders['class']
    plot_waffle(data_vehicle, class_encoder)
    plot_feature_importances_(model)
    classes = class_encoder.inverse_transform(model.predict(data))
    print(classes)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--input', dest='classification_data', required=True, help='Input data for classification')

    args = parser.parse_args()
    random_forest_cl(args.classification_data)
