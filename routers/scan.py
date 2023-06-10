import os
import tempfile

from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List, Dict
from pydantic import BaseModel, Field

from classifier import Classifier

# Response Model
class upload_result(BaseModel):
    path: str = Field(..., description="The path to the uploaded file.", example='/tmp/1234567890')

class detects_model(BaseModel):
    name: str = Field(..., description="The name of the detect.", example='Trojan')
    type_version: str = Field(..., description="The type version of the detect.", example='v230528')

class file_info(BaseModel):
    filesize: int = Field(..., description="The filesize of the file.", example=1024)
    sha256: str = Field(..., description="The sha256 of the file.", example='1234567890')
    md5: str = Field(..., description="The md5 of the file.", example='1234567890')
    sha1: str = Field(..., description="The sha1 of the file.", example='1234567890')
#    detects : List[detects_model] = Field(..., description="The detects of the file.", example=[])

class vt_result(BaseModel):
    total_vendors: int = Field(..., description="The total vendors of the file.", example=70)
    malicious_vendors: int = Field(..., description="The malicious vendors of the file.", example=10)
    threat_name: str = Field(..., description="The threat name of the file.", example='Trojan')

class mb_report(BaseModel):
    signature: str = Field(..., description="The signature of the file.", example='Trojan.Win32.Generic!BT')
    threat_name: str = Field(..., description="The threat name of the file.", example='Trojan')

class prediction_result(BaseModel):
    ascii: float = Field(..., description="The prediction of the file (ASCII).", example=0.1)
    utf16le: float = Field(..., description="The prediction of the file (UTF16LE).", example=0.1)
    opcode: float = Field(..., description="The prediction of the file (Opcode).", example=0.1)
    pe_header: float = Field(..., description="The prediction of the file (PE Header).", example=0.1)
    rich_header: float = Field(..., description="The prediction of the file (Rich Header).", example=0.1)
    totol: float = Field(..., description="The prediction of the file (Total).", example=0.1)

router = APIRouter(prefix='/scan')

models_dir = os.getenv('MODELS_DIR')
word_indexs_dir = os.getenv('WORD_INDEXS_DIR')

classifier = Classifier(models_dir=models_dir, word_indexs_dir=word_indexs_dir)

tempdir = tempfile.gettempdir()

@router.post('/upload', responses={200: {'description': 'Uploads a file to the server.'}}, response_model=upload_result, tags=['Scan'])
def upload_file(file: UploadFile = File(...)):
    contents = file.file.read()

    with open(os.path.join(tempdir, file.filename), 'wb') as f:
        f.write(contents)
    path = os.path.join(tempdir, file.filename)

    classifier.file = path
    return upload_result(path=path)


responses = {
    400: {'description': 'Parameter Not invaild'},
    404: {'description': 'File Not Found'}
}

def validate_path(path: str = None):
    if path is None:
        raise HTTPException(status_code=400, detail='`path` parameter is required.')

    try:
        classifier.file = path
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail='File not invaild, please upload a file first. or specify a path.')
    except ValueError:
        raise HTTPException(status_code=400, detail='File not invaild, please upload PE file.')

@router.get('/info', responses={ 200: {'description': 'Get file info'}, 400:{'description': '`path` parameter is required.'}}, response_model=file_info, tags=['Scan'])
def info(path: str = None):
    validate_path(path)

    info = classifier.file_info
  #  detects = []
 #   for detect in info['detects'][0]:
    #    print(detect)
   #     detects.append(detects_model(name=detect[0], type_version=detect[1]))

    return file_info(filesize=info['filesize'], sha256=info['sha256'], md5=info['md5'], sha1=info['sha1'])

@router.get('/vt', responses={ 200: {'description': 'Get VirusTotal result of file'},}.update(responses), response_model=vt_result, tags=['Scan'])
def vt(path: str = None):
    validate_path(path)

    vt = classifier.vt_report

    return vt_result(total_vendors=vt['total_vendors'], malicious_vendors=vt['malicious_vendors'], threat_name=vt['threat_name'])

@router.get('/mb', responses={ 200: {'description': 'Get MalwareBazaar result of file'},}.update(responses), response_model=mb_report, tags=['Scan'])
def mb(path: str = None):
    validate_path(path)

    mb = classifier.mb_report

    return mb_report(signature=mb['signature'], threat_name=mb['threat_name'])

@router.get('/prediction', responses={ 200: {'description': 'Get prediction result of file'},}.update(responses), response_model=prediction_result, tags=['Scan'])
def prediction(path: str = None):
    validate_path(path)

    prediction = classifier.predict

    return prediction_result(ascii=prediction['ascii'], utf16le=prediction['utf16le'], opcode=prediction['opcode'], pe_header=prediction['pe_header'], rich_header=prediction['rich_header'], totol=prediction['predict'])
