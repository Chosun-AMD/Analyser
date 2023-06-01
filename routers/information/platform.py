from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel, Field

from system import PlatformInformation

# Response Model
class platform_model(BaseModel):
    system: str = Field(..., description="The system/OS name.", example='Linux')
    version: str = Field(..., description="The system's release version.", example='#1 SMP Fri Jan 27 02:56:13 UTC 2023')
    release: str = Field(..., description="The system's release.", example='4.4.0-112-generic')
    distro: str = Field(..., description="The system's distro.", example='Ubuntu 16.04.3 LTS')
    arch: str = Field(..., description="The system's architecture.", example='x86_64')

class ip_model(BaseModel):
    internal: str = Field(..., description="The system's internal IP address.", example='192.168.0.1')
    external: str = Field(..., description="The system's external IP address.", example='*.*.*.*')

platform = PlatformInformation()

router = APIRouter(prefix='/platform')

@router.get('/', responses={200: {'description': 'Returns the platform information.'}}, response_model=platform_model, tags=['Platform'])
async def get_platform():
    return platform_model(
        system=platform.system,
        version=platform.version,
        release=platform.release,
        distro=platform.distro,
        arch=platform.arch
    )

@router.get('/ip', responses={200: {'description': 'Returns the platform IP information.'}}, response_model=ip_model, tags=['Platform'])
async def get_platform_ip():
    return ip_model(
        internal=platform.internal_ip,
        external=platform.external_ip
    )