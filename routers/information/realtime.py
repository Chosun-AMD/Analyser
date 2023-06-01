from fastapi import APIRouter
from typing import List, Dict
from pydantic import BaseModel, Field

from system import RealtimeSystemInformation

# Response Model
class cpu_model(BaseModel):
    usage: float = Field(..., description="The system's CPU usage.", example=0.0)

class mem_model(BaseModel):
    usage: int = Field(..., description="The system's memory usage.", example=1073741824)

class disk_model(BaseModel):
    mountpoint: str = Field(..., description="The mountpoint of the disk.", example='/')
    usage: int = Field(..., description="The usage size of the disk.", example=1073741824)

class disks_model(BaseModel):
    disks: List[disk_model] = Field(..., description="The list of disks and their sizes.", example=[{'mountpoint': '/', 'total': 1073741824}])

router = APIRouter(prefix='/realtime')

sys_info = RealtimeSystemInformation()

@router.get('/cpu', responses={200: {'description': 'Returns the system information.'}}, response_model=cpu_model, tags=['Realtime'])
async def get_cpu():
    return cpu_model(
        usage=sys_info.cpu
    )

@router.get('/mem', responses={200: {'description': 'Returns the system information.'}}, response_model=mem_model, tags=['Realtime'])
async def get_mem():
    return mem_model(
        usage=sys_info.mem
    )

@router.get('/disks', responses={200: {'description': 'Returns the system information.'}}, response_model=disks_model, tags=['Realtime'])
async def get_disks():
    result = []

    for disk in sys_info.disks:
        result.append(disk_model(
            mountpoint=disk[0],
            usage=disk[1]
        ))
    return disks_model(disks=result)