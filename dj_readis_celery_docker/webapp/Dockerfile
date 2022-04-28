FROM python:3.10
RUN apt-get update -y
RUN apt-get upgrade -y

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY ./project_dj_redis ./project_dj_redis

CMD ["python3", "./project_dj_redis/manage.py", "runserver", "0.0.0.0:8000"]