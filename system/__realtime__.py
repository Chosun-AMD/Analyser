import os
import psutil

class RealtimeSystemInformation:
    """
    실시간 분석 서버 정보
    """
    def __init__(self) -> None:
        pass

    @property
    def cpu(self) -> float:
        """
        Returns the system's CPU usage, e.g. `0.0`
        """
        return psutil.cpu_percent()
    
    @property
    def mem(self) -> int:
        """

        """
        return psutil.virtual_memory().used
    
    @property
    def disks(self) -> list:
        """
        Returns the list of partitions and their size, e.g. `[('/', 10737418240)]`
        """
        result = []
        for partition in psutil.disk_partitions():
            result.append((partition.mountpoint, psutil.disk_usage(partition.mountpoint).used))
        return result
    

