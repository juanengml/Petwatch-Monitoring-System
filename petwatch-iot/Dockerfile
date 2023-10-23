FROM python:3.9-buster

RUN apt-get update 

RUN apt-get install wget cmake \
    make \
    build-essential \
    libgtk-3-dev \
    libboost-all-dev \
    freeglut3-dev  \
    libopenblas-dev  --yes

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 3030
CMD ["python", "app.py"]
