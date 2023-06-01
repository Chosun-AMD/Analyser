from tensorflow import keras
from keras import models

import os
import magic

class Predictor():
    def __init__(self, model_path):
        self._model_path = model_path
        self._model = models.load_model(model_path)
        self._feature = None

    @property
    def file(self) -> str:
        if self._file == '':
            raise ValueError('File is not set')
        return self._file

    @file.setter
    def file(self, file):
        if os.path.isfile(file) is False:
            raise FileNotFoundError('File not found or is not a file')

        if magic.from_file(file).find('PE32') == -1:
            raise ValueError('File is not a PE32 file. Only PE32 files are supported. (e.g. exe, dll, sys)')

        self._file = file

    @property
    def feature(self):
        if self._feature is None:
            raise ValueError('Feature is not set')
        return self._feature

    @feature.setter
    def feature(self, feature):
        self._feature = feature

    @property
    def predict(self):
        return self._model.predict(self.feature)[0][0]


