FROM tiangolo/uwsgi-nginx-flask

WORKDIR /app

COPY . /app 

RUN pip install -r requeriments.txt

#ENTRYPOINT ['python app.py']







