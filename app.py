from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from fastapi.openapi.utils import get_openapi

import requests
import tempfile
import zipfile

def download(url, filename):
    headers = {'user-agent': 'Wget/1.16 (linux-gnu)'}
    file = requests.get(url, headers=headers)
    with tempfile.TemporaryDirectory() as tmpdirname:
        with open(tmpdirname + '/download.zip', 'wb') as f:
            for chunk in file.iter_content(chunk_size=128):
                f.write(chunk)
        # Unzip model file
        with zipfile.ZipFile(tmpdirname + '/download.zip', 'r') as zip_ref:
            zip_ref.extractall(f'./{filename}')


print('Downloading models...')
model_url = 'https://www.dropbox.com/sh/lg9q6uyrkhgkmvf/AAB81SAKgbPbuJgFplwAUdb2a?dl=0'
download(model_url, 'models')

print('Downloading word index...')
word_index_url = 'https://www.dropbox.com/sh/u1fhl6f9z1rha3u/AABlr2D9mFqm_DbmUWcb6Y0Pa?dl=0'
download(word_index_url, 'word_index')

from routers import *

app = FastAPI(
    title='A.M.D Malware Classifier API',
    description='...',
    version='0.0.1',
    contact={
            'name': 'Hunmin Kim (Role: Team Leader)',
            'url': 'https://github.com/Chosun-AMD/Analyser/issues',
            'email': 'contact@h4n9u1.dev',
        },
    license_info={
        'name': 'MIT License',
        'url': '[GITHUB LICENSE URL]'
    }
)

def openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        # description=description,
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = openapi

app.include_router(hardware_router)
app.include_router(platform_router)
app.include_router(version_router)
app.include_router(scan_router)
app.include_router(realtime_router)

@app.get('/', include_in_schema=False)
async def root():
    return RedirectResponse(url='/redoc')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app:app", host='0.0.0.0', port=8000, reload=True)
