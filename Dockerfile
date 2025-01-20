FROM python:3.14.0a4-slim-bullseye

WORKDIR /usr/app/src

COPY . ./

RUN pip install requests configparser

CMD ["python3", "./main.py"]