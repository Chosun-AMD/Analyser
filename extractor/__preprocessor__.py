from tensorflow import keras
from keras.preprocessing.sequence import pad_sequences

import pefile
import numpy as np
import os
import magic

from abc import *

class __preprocessor__(metaclass=ABCMeta):
    def __init__(self, maxlen):
        self._file = ''
        self._maxlen = maxlen

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

    @abstractmethod
    def extract(self):
        pass

    @property
    def input_data(self):
        _data = self.extract()

        array = np.frombuffer(_data, dtype=np.uint8)
        padded_sequences = pad_sequences([array], maxlen=self._maxlen, padding='post', truncating='post')
        expanded_sequences = np.expand_dims(padded_sequences, axis=2)

        return expanded_sequences
