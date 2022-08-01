FROM python:3.9.6
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE $PORT
CMD gunicorn --wokers=4 --bind 0.0.0.0:$PORT flaskApp:app