# 시스템 정보와 관련된 함수

import platform
import cpuinfo
import psutil
import tensorflow as tf
from tensorflow import keras
import nvidia_smi
import distro
import sys
import os
import glob
import socket
import requests

class PlatformInformation:
    """
    시스템의 플랫폼 정보를 담고 있는 클래스
    """
    def __init__(self):
        self._system = platform.system()
        self._version = platform.version()
        self._release = platform.release()
        self._distro = distro.name(pretty=True)
        self._arch = platform.machine()
        self._internal_ip = socket.gethostbyname(socket.gethostname())
        self._external_ip = requests.get('https://api.myip.com').json()['ip']

    @property
    def system(self) -> str:
        """
        Returns the system/OS name, e.g. `Linux`, `Windows`, `Darwin`.
        """
        return self._system

    @property
    def version(self) -> str:
        """
        Returns the system's release version, e.g. `#1 SMP Fri Jan 27 02:56:13 UTC 2023`
        """
        return self._version

    @property
    def release(self):
        """
        Returns the system's release, e.g. `4.4.0-112-generic`
        """
        return self._release

    @property
    def distro(self):
        """
        Returns the system's distro, e.g. `Ubuntu 16.04.3 LTS`
        """
        return self._distro

    @property
    def arch(self):
        """
        Returns the system's architecture, e.g. `x86_64`
        """
        return self._arch

    @property
    def internal_ip(self):
        """
        Returns the system's internal IP address, e.g. `192.168.0.1`
        """
        return self._internal_ip

    @property
    def external_ip(self):
        """
        Returns the system's external IP address, e.g. `*.*.*.*`
        """
        return self._external_ip

class HardwareInformation:
    def __init__(self):
        self._processor = cpuinfo.get_cpu_info()['brand_raw']
        self._core = cpuinfo.get_cpu_info()['count']
        self._arch = cpuinfo.get_cpu_info()['arch_string_raw']
        self._mem = psutil.virtual_memory().total
        self._gpus = self._get_gpus()
        self._partitions = psutil.disk_partitions()

    def _get_gpus(self):
        """
        Returns the list of GPUs and their memory size use NVIDIA SMI.

        if NVIDIA SMI is not installed, returns [('No NVIDIA GPU', -1)]
        """
        details = []
        try:
            nvidia_smi.nvmlInit()
            deviceCount = nvidia_smi.nvmlDeviceGetCount()

            for i in range(deviceCount):
                handdle = nvidia_smi.nvmlDeviceGetHandleByIndex(i)
                info = nvidia_smi.nvmlDeviceGetMemoryInfo(handdle)
                details.append((nvidia_smi.nvmlDeviceGetName(handdle).decode(), info.total))
            nvidia_smi.nvmlShutdown()
            return details
        except:
            return [('No NVIDIA GPU', -1)]

    @property
    def processor(self):
        """
        Returns the processor name and core, e.g. `('Intel(R) Core(TM) i7-10700KF CPU @ 3.80GHz', 16)`
        """
        return self._processor, self._core

    @property
    def arch(self):
        """
        Returns the system's architecture, e.g. `x86_64`
        """
        return self._arch

    @property
    def mem(self):
        """
        Returns the system's RAM size, e.g. `33617625088`
        """
        return self._mem

    @property
    def gpus(self):
        """
        Returns the list of GPUs and their memory size, e.g. `[('GeForce RTX 3080', 10737418240)]`
        """
        return self._gpus

    @property
    def partitions(self):
        """
        Returns the list of partitions and their size, e.g. `[('/', 10737418240)]`
        """
        result = []
        for partition in self._partitions:
            result.append((partition.mountpoint, psutil.disk_usage(partition.mountpoint).total))
        return result

class LibraryInformation:
    def __init__(self):
        self.python_version = sys.version
        self.tf_version = tf.__version__


    @property
    def python(self):
        """
        Returns the python version, e.g. `3.11.3 (main, Apr 19 2023, 23:54:32) [GCC 11.2.0]`
        """
        return self.python_version

    @property
    def tensorflow(self):
        """
        Returns the tensorflow version, e.g. `2.12.0`
        """
        return self.tf_version

class ModelInformation:
    def __init__(self) -> None:
        MODELS = os.environ['MODELS_DIR']

        if MODELS is None:
            raise Exception(f'{MODELS} is not defined')

        if not os.path.exists(MODELS):
            raise FileNotFoundError(f'{MODELS} is not exists')

        self._models_path = glob.glob(os.path.join(MODELS, '*.h5'))
        self._models = self.load_models()

    def load_models(self):
        """
        Load model and version in the `MODELS` directory
        """
        models = []
        for model_path in self._models_path:
            basename_without_ext = os.path.splitext(os.path.basename(model_path))[0]
            model_name = basename_without_ext.split('-')[0]
            model_version = basename_without_ext.split('-')[1]

            models.append({'name': model_name, 'version': model_version})

        return models

    @property
    def models(self):
        """
        Returns the list of models, e.g. `[{name: 'model', version: '1.0.0'}]`
        """
        return self._models