FROM python:3.9.6
COPY ./FarmWiserApp /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE $PORT
CMD gunicorn --workers=4 --bind 0.0.0.0:$PORT flaskApp:app