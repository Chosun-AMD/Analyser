FROM continuumio/miniconda3

RUN conda install tensorflow

RUN apt update -y
RUN apt install libmagic-dev -y

# Download NTINFO DiE
RUN wget https://github.com/horsicq/DIE-engine/releases/download/3.07/die_3.07_Debian_11_amd64.deb && \
    dpkg --force-all -i  die_3.07_Debian_11_amd64.deb && \
    apt install -f -y && \
    rm die_3.07_Debian_11_amd64.deb

RUN mkdir /app
WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

ENV MODELS_DIR /app/models
ENV WORD_INDEXS_DIR /app/word_index
RUN mkdir $MODELS_DIR
RUN mkdir $WORD_INDEXS_DIR

CMD ["python", "-muvicorn", "app:app", "--host", "0.0.0.0"]