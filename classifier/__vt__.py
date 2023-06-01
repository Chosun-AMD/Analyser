from typing import Any
import vt # VirusTotal API
import os
import hashlib

class VirusTotal:
    def __init__(self, vt_api_key):
        self._vt_api_key = vt_api_key
        self._client = vt.Client(self._vt_api_key)
        self._filename = ''

    def __del__(self):
        self._client.close()

    @property
    def filename(self) -> str:
        if self._filename == '':
            raise ValueError('File is not set')
        return self._filename

    @filename.setter
    def filename(self, filename):
        if os.path.isfile(filename) is False:
            raise FileNotFoundError('File not found or is not a file')

        self._filename = filename

    @property
    def sha256(self) -> str:
        return hashlib.sha256(open(self.filename, 'rb').read()).hexdigest()

    def __call__(self, filename) -> Any:
        self.filename = filename
        try:
            vt_file = self._client.get_object("/files/{}", self.sha256)

            total_vendors = sum(vt_file.last_analysis_stats.values())
            malicious_vendors = vt_file.last_analysis_stats.get('malicious', 0)

            try:
                threat_name = vt_file.popular_threat_classification['suggested_threat_label']
            except:
                threat_name = 'Harmless'

            return {'total_vendors': total_vendors, 'malicious_vendors': malicious_vendors, 'threat_name': threat_name}
        except:
            return {'total_vendors': 0, 'malicious_vendors': 0, 'threat_name': 'Not Found'}