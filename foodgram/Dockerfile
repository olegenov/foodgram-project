FROM python:3.8.5

WORKDIR /code
COPY . /code
RUN python3 -m pip install -r /code/requirements.txt
RUN chmod +x entrypoint.sh
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
