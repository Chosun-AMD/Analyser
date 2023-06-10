import os
import glob
import numpy as np
import json

from .__predict__ import Predictor
from .__vt__ import VirusTotal
from .__malwarebazaar__ import MalwareBazaar

from extractor import *

class Classifier:
    def __init__(self, models_dir, word_indexs_dir) -> None:
        self._models_dir = models_dir
        self._word_indexs_dir = word_indexs_dir
        self._file = ''

        self._model_names = ['ascii', 'utf16le', 'opcode', 'pe_header', 'rich_header', 'predict']
        self._model_paths = [glob.glob(os.path.join(self._models_dir, f'{model}-*.h5'))[0] for model in self._model_names]

        self._predictors = {}

        for name, path in zip(self._model_names, self._model_paths):
            self._predictors[name] = Predictor(path)

        self._extractors = {}

        for name, extractor in zip(self._model_names[:-1], [ASCIIExtractor(), UTF16LEExtractor(), OpcodeExtractor(), PEHeaderExtractor(), RichHeaderExtractor()]):
            self._extractors[name] = extractor
            if name == 'ascii' or name == 'utf16le' or name == 'opcode':
                extractor.word_index = os.path.join(self._word_indexs_dir, f'word_index.{name}.msgpack')

        # VirusTotal
        self._vt_api_key = os.getenv('VT_API_KEY')
        self.client = VirusTotal(self._vt_api_key)

    @property
    def file(self) -> str:
        if self._file == '':
            raise ValueError('File is not set')
        return self._file

    @file.setter
    def file(self, file):
        if os.path.isfile(file) is False:
            raise FileNotFoundError('File not found or is not a file')

        self._file = file

    @property
    def sha256(self) -> str:
        return hashlib.sha256(open(self.file, 'rb').read()).hexdigest()

    @property
    def vt_report(self):
        return self.client(self.file)

    # MalwareBazaar
    @property
    def mb_report(self):
        mb = MalwareBazaar()
        return mb(self.file)

    # AI
    @property
    def predict(self):
        predictions = []
        for name in self._model_names[:-1]:
            self._extractors[name].file = self.file
            self._predictors[name].feature = self._extractors[name].input_data
            predictions.append(self._predictors[name].predict)

        self._predictors['predict'].feature =  np.array([predictions], dtype=np.float32)

        result = {}

        for name, prediction in zip(self._model_names[:-1], predictions):
            result[name] = prediction
        result['predict'] = self._predictors['predict'].predict

        return  result

    @property
    def diec(self):
        diec_result = json.loads(subprocess.check_output(['diec', self.file, '-j']))
        temp = []
        for item in diec_result['detects'][0]['values']:
            temp.append(item['string'].split(': '))

        return {'detects': [temp]}
    @property
    def hashes(self):
        return {'sha256': self.sha256, 'md5': hashlib.md5(open(self.file, 'rb').read()).hexdigest(), 'sha1': hashlib.sha1(open(self.file, 'rb').read()).hexdigest()}

    @property
    def file_info(self):
        info = {'filesize': os.path.getsize(self.file)}
        info.update(self.hashes)
        #info.update(self.diec)
        return info
