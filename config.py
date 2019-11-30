from peewee import SqliteDatabase
from sklearn import preprocessing

EPOCH_COUNT = 2000
INPUT_PARAMETERS = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety', 'class']
SQLITE_DB = SqliteDatabase(
        'source data/source_bd.db'
    )
MODEL_NAME = 'Trained model.h5'
ENCODERS = {
        param: preprocessing.LabelEncoder() for param in INPUT_PARAMETERS
    }
