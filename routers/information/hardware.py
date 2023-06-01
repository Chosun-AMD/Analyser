from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel, Field

from system import HardwareInformation

# Response Model
class cpu_model(BaseModel):
    processor: str = Field(..., description="The CPU's name.", example='Intel(R) Core(TM) i7-10700KF CPU @ 3.80GHz')
    core: int = Field(..., description="The number of cores the CPU has.", example=16)
    arch: str = Field(..., description="The CPU's architecture.", example='x86_64')

class memory_model(BaseModel):
    memory: int = Field(..., description="The RAM size. (Unit: bytes)", example=33617625088)

class gpu_model(BaseModel):
    name: str = Field(..., description="The GPU's name.", example='GeForce RTX 3080')
    memory: int = Field(..., description="The GPU's memory size. (Unit: bytes)", example=10737418240)

class gpus_model(BaseModel):
    gpus: List[gpu_model] = Field(..., description="The list of GPUs and their memory size.", example=[{'name': 'GeForce RTX 3080', 'memory': 10737418240}])

class disk_model(BaseModel):
    mountpoint: str = Field(..., description="The mount point of the disk.", example='/')
    size: int = Field(..., description="The disk size. (Unit: bytes)", example=10737418240)

class disks_model(BaseModel):
    disks: List[disk_model] = Field(..., description="The list of partitions and their size.", example=[{'mountpoint': '/', 'size': 10737418240}])

hwinfo = HardwareInformation()

router = APIRouter(prefix='/hardware')

@router.get('/cpu', responses={200: {'description': 'Returns the CPU information.'}}, response_model=cpu_model, tags=['Hardware'])
async def get_cpu():
    processor, core = hwinfo.processor
    arch = hwinfo.arch
    return cpu_model(
        processor=processor,
        core=core,
        arch=arch
    )

@router.get('/memory', responses={200: {'description': 'Returns the memory information.'}}, response_model=memory_model, tags=['Hardware'])
async def get_memory():
    mem = hwinfo.mem
    return memory_model(memory=mem)

@router.get('/disks', responses={200: {'description': 'Returns the disk information.'}}, response_model=disks_model, tags=['Hardware'])
async def get_disks():
    result = disks_model(disks=[])
    for _disk in hwinfo.partitions:
        mountpoint, size = _disk
        result.disks.append(disk_model(mountpoint=mountpoint, size=size))
    return result

@router.get('/gpu', responses={200: {'description': 'Returns the GPU information.'}, 404: {'description': 'This sytsem does not hava NVIDIA GPU'}}, response_model=gpus_model, tags=['Hardware'])
async def get_gpu():
    result = gpus_model(gpus=[])  # Assign an empty list directly
    for _gpu in hwinfo.gpus:
        name, memory = _gpu
        result.gpus.append(gpu_model(name=name, memory=memory))

    if len(result.gpus) == 1 and result.gpus[0].name == 'No NVIDIA GPU':
        raise HTTPException(status_code=404, detail="This device does not have NVIDIA GPU")

    return result