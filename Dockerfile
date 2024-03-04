# FROM python:3

# ENV PYTHONUNBUFFERED 1
# ENV PYTHONDONTWRITEBYTECODE 1

# WORKDIR /

# ADD . /

# COPY ./requirements.txt /requirements.txt

# RUN pip install -r requirements.txt

# COPY .  /


FROM python:3


ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1


WORKDIR /app


COPY ./requirements.txt /app/


RUN pip install -r requirements.txt


COPY . /app/

CMD [ "python" ,"manage.py","runserver","0.0.0.0:8000","--noreload"]
