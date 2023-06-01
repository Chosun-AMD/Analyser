from tensorflow import keras
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer

import msgpack
import magic
import os

from abc import *

class __tokenizer__(metaclass=ABCMeta):
    """
    Tokenizer class for the strings and opcodes.
    """

    def __init__(self, truncate_len = 128) -> None:
        if truncate_len != 0:
            self._truncate = lambda x: x[:truncate_len]
        else:
            self._truncate = lambda x: x

        self._file = ''
        self._word_index = None

    @property
    def word_index(self) -> dict:
        if self._word_index is None:
            raise ValueError('Word index is not set')
        return self._word_index

    @word_index.setter
    def word_index(self, word_index: str):
        if os.path.isfile(word_index) is False:
            raise FileNotFoundError('File not found or is not a file')

        self._word_index = msgpack.load(open(word_index, 'rb'))

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

    def _tokenize(self, strings: list) -> list:
        """
        Returns the tokenized list of strings.
        """
        serialized_strings = ' '.join([self._truncate(s) for s in strings])
        tokenizer = Tokenizer()
        tokenizer.word_index = self.word_index

        sequences = tokenizer.texts_to_sequences([serialized_strings])
        padded_sequences = pad_sequences(sequences, maxlen=100)
        return padded_sequences

    @abstractmethod
    def parse(self):
        pass

    @property
    def input_data(self) -> list:
        """
        Returns the tokenized data.
        """
        datas = self.parse()
        return self._tokenize(datas)