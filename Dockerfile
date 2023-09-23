FROM python:3.10-slim-buster

RUN apt update --fix-missing
RUN apt upgrade -y

RUN python -m pip install --upgrade pip

RUN apt update --fix-missing

RUN apt install build-essential -y

RUN apt install -y supervisor nano

RUN apt -y install sox

ENV INSTALL_PATH /background_noise_removal

RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

RUN apt update && \
    apt install -y ffmpeg

RUN pip install ffmpeg-python

COPY . .
ADD supervisord.conf /etc/supervisord.conf

ENTRYPOINT ["supervisord", "--nodaemon", "--configuration", "/etc/supervisord.conf"]

# CMD [ "supervisord", "--nodaemon", "--configuration", "/etc/supervisord.conf" ]
# ENTRYPOINT ["gunicorn", "-c", "gunicorn_config.py", "wsgi:app"]

# CMD [ "gunicorn", "-c", "gunicorn_config.py", "wsgi:app" ]
