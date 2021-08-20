FROM python:3.8-slim
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
COPY requirements.txt /code/requirements.txt
COPY entrypoint.sh entrypoint.sh
WORKDIR /code
RUN apt-get update
RUN apt-get install -y binutils
RUN apt-get install -y gdal-bin
RUN pip install -r requirements.txt
COPY . /code/
RUN chmod +x entrypoint.sh
