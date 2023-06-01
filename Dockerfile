FROM python:bullseye

RUN apt update -y

# Download NTINFO DiE
RUN wget https://github.com/horsicq/DIE-engine/releases/download/3.07/die_3.07_Debian_11_amd64.deb && \
    dpkg --force-all -i  die_3.07_Debian_11_amd64.deb && \
    apt install -f -y && \
    rm die_3.07_Debian_11_amd64.deb

RUN mkdir /app
WORKDIR /app
COPY . /app

RUN pip -r requirements.txt

ENV MODEL_PATH /app/models
ENV WORD_INDEXS_DIR /app/word_indexs

CMD ["python", "app.py"]