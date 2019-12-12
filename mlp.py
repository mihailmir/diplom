import pandas as pd
from keras import Sequential
from keras.layers import Dense, Dropout
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from keras.optimizers import SGD
from keras.callbacks import ModelCheckpoint
from keras.models import load_model
from config import INPUT_PARAMETERS, SQLITE_DB, EPOCH_COUNT, ENCODERS, MODEL_NAME
from plot import plot_loss_acc
import numpy as np
import sys
import pickle
import argparse


def read_input_data(path):
    #     data_vehicle_frame = pd.DataFrame(columns=['Date', 'Vehicle Count'])
    #     with open('source data/Dodgers.data', 'r') as file:
    #         data = file.read().splitlines()
    #         for index, col in enumerate(data_vehicle_frame.columns):
    #             data_vehicle_frame[col] = list(map(lambda x: x.split(',')[index], data))
    #         data_vehicle_frame['Date'] = pd.to_datetime(data_vehicle_frame['Date'])
    #         data_vehicle_frame['Vehicle Count'] = pd.to_numeric(data_vehicle_frame['Vehicle Count'])
    #
    #     data_event_frame = pd.DataFrame(
    #         columns=[
    #             'Date', 'Begin Event Time', 'End Event Time', 'Game Attendance', 'Away Team', 'W/L score'
    #         ]
    #     )
    #     with open('source data/Dodgers.events', 'r') as file:
    #         data = file.read().splitlines()
    #         for index, col in enumerate(data_event_frame.columns):
    #             data_event_frame[col] = list(map(lambda x: x.split(',')[index], data))
    #         data_event_frame['Date'] = pd.to_datetime(data_event_frame['Date'])
    #
    #         #data_vehicle_frame.groupby(by=lambda x: datetime.strptime(data_vehicle_frame.loc[x]['Date'], '%m/%d/%Y %H:%M').date())
    #
    #     data_vehicle_frame = data_vehicle_frame.resample('D', on='Date').sum()
    #     result_data_set = pd.merge(left=data_vehicle_frame, right=data_event_frame, left_on='Date', right_on='Date', how='outer', indicator='Has Game')
    #     result_data_set.to_csv(r'result_data_set.txt', sep=',')
    #     result_data_set['Has Game'] = to_categorical(result_data_set['Has Game'])
    #     x_train, y_train = result_data_set.values[::, 1:2], result_data_set.values[::, 7:8]
    #
    #     model = Sequential()
    #     model.add(Dense(64, input_dim=1, activation='relu'))
    # #     model.add(Dropout(0.5))
    # #     model.add(Dense(64, activation='relu'))
    # #     model.add(Dropout(0.5))
    #     model.add(Dense(1, activation='sigmoid'))
    #     model.compile(loss='binary_crossentropy',
    #                   optimizer='rmsprop',
    #                   metrics=['accuracy'])
    #     model.fit(x_train, y_train,
    #               epochs=20,
    #               batch_size=128)
    input_params = INPUT_PARAMETERS.copy()
    input_params.remove('class')
    try:
        data = pd.read_csv(path, dtype={param: np.object for param in input_params})
    except FileNotFoundError:
        sys.exit('Input data for classification not found.')
    # print(data)

    if set(input_params) != set(data.keys()):
        sys.exit('Unexpected input values, expect {}.'.format(', '.join(input_params)))

    for col in data.head():
        try:
            loaded_encoder = open('encoders/{}_encoder.pkl'.format(col), 'rb')
            encoder = pickle.load(loaded_encoder)
            loaded_encoder.close()
        except FileNotFoundError:
            sys.exit('Encoders not found, try ty run scripts without -load option.')
        data[col] = encoder.transform(data[col])
    return data


def train_model(path):
    # with open(DATA_FOR_TRAIN, 'r') as file:
    #     data = file.read().splitlines()
    #     for index, col in enumerate(data_vehicle.columns):
    #         data_vehicle[col] = list(map(lambda x: x.split(',')[index], data))
    data_vehicle = pd.read_sql("SELECT {} FROM cars".format(', '.join(INPUT_PARAMETERS)), con=SQLITE_DB)

    for col in data_vehicle.columns:
        data_vehicle[col] = ENCODERS[col].fit_transform(data_vehicle[col])
        with open('encoders/{}_encoder.pkl'.format(col), 'wb') as save_encoders:
            pickle.dump(ENCODERS[col], save_encoders)

    # Save the model after every epoch.
    checkpointer = ModelCheckpoint(filepath=MODEL_NAME, monitor='loss', save_best_only=True, mode='min')

    X_train, X_test, y_train, y_test = train_test_split(data_vehicle.values[::, 0:6], data_vehicle.values[::, 6:7],
                                                        test_size=0.2)

    model = Sequential()

    model.add(Dense(64, activation='relu', input_dim=6))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(4, activation='softmax'))

    sgd = SGD(lr=0.1)
    model.compile(
        loss='categorical_crossentropy',
        optimizer=sgd,
        metrics=['accuracy']
    )
    history = model.fit(
        X_train, to_categorical(y_train),
        epochs=EPOCH_COUNT,
        batch_size=128,
        callbacks=[checkpointer]
    )

    hist_df = pd.DataFrame(history.history)
    hist_csv_file = 'Training history.csv'
    with open(hist_csv_file, mode='w') as f:
        hist_df.to_csv(f)
    predict_classes(model, read_input_data(path))


def predict_classes(model, data):
    with open('encoders/class_encoder.pkl', 'rb') as f:
        class_encoder = pickle.load(f)
    print(class_encoder.inverse_transform(model.predict_classes(data)))
    data = pd.read_csv('Training history.csv')
    plot_loss_acc(data)


def load_trained_model(path):
    try:
        model = load_model(MODEL_NAME)
    except OSError:
        sys.exit('Unable to get trained model, try to run script without -l option.')

    predict_classes(model, read_input_data(path))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # input args
    parser.add_argument('--load', '-l', dest='load_model',
                        help='Load model', action='store_true')

    parser.add_argument('--input', dest='classification_data', required=True, help='Input data for classification')

    args = parser.parse_args()
    if args.load_model:
        load_trained_model(args.classification_data)
    else:
        train_model(args.classification_data)

