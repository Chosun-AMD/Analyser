from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel, Field

from system import LibraryInformation
from system import ModelInformation

# Response Model
class python_model(BaseModel):
    version: str = Field(..., description="The Python version.", example='3.11.3 (main, Apr 19 2023, 23:54:32) [GCC 11.2.0]')

class tf_model(BaseModel):
    version: str = Field(..., description="The TensorFlow version.", example='2.12.0')

class model_model(BaseModel):
    name: str = Field(..., description="The model's name.", example='ascii')
    version: str = Field(..., description="The model's version.", example='v230528')

class models_model(BaseModel):
    models: List[model_model] = Field(..., description="The list of models and their versions.", example=[{'name': 'ascii', 'version': 'v230528'}])

router = APIRouter(prefix='/version')

lib_info = LibraryInformation()
model_info = ModelInformation()


@router.get('/python', responses={200: {'description': 'Returns the library information.'}}, response_model=python_model, tags=['Library'])
async def get_python():
    return python_model(
        version=lib_info.python_version
    )

@router.get('/tf', responses={200: {'description': 'Returns the library information.'}}, response_model=tf_model, tags=['Library'])
async def get_tensorflow():
    return tf_model(
        version=lib_info.tf_version
    )

@router.get('/models', responses={200: {'description': 'Returns the library information.'}}, response_model=models_model, tags=['Library'])
async def get_model():
    return models_model(
        models=model_info.models
    )