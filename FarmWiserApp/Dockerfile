FROM python:3.9.6

WORKDIR /FarmWiserApp

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
EXPOSE $PORT
CMD gunicorn --workers=4 --bind 0.0.0.0:$PORT flaskApp:app