FROM python:3.9
ENV PYTHONUNBUFFERED=1
ENV DOCKER_DEFAULT_PLATFORM=linux/amd64
WORKDIR /mydjangoapp
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

