FROM ubuntu

RUN apt-get update\
    && apt-get install -y python3-pip python3-dev\
    && cd /usr/local/bin \
    && ln -s /usr/bin/python3 python \
    && pip3 install --upgrade pip

COPY . /home/
COPY requeriments.txt requeriments.txt

RUN pip3 install -r requeriments.txt

VOLUME dado/ /home/mmartan/mmartan/data 

WORKDIR  /home/mmartan/mmartan

ENTRYPOINT ["scrapy", "crawl", "robommartan", "-o", "data/arquivo.csv"]



# -*- coding: utf-8 -*-



