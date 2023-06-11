# Chosun A.M.D - Analyser
학습한 모델을 기반으로 바이너리 파일을 분석하는 서버입니다.

## 실행
해당 서버는 Docker를 지원합니다. 다음과 같이 Docker 이미지를 빌드하고 실행을 하면 됩니다.

```
$ export VT_API_KEY='' # VirusTotal API Key
$ export WORD_INDEXS_DIR='' # Word Index가 저장되는 경로, 최초 실행시 다운로드 됨
$ export MODELS_DIR='' # 모델이 저장되는 경로, 최초 실행시 다운로드 됨
$ docker build -t amd/analyser:1.0.0 .
$ docker run -it --rm -p 8000:8000 -e VT_API_KEY=$VT_API_KEY amd/analyser:1.0.
```