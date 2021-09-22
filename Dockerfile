# syntax=docker/dockerfile:1
# Build image:  docker build -t shorten-link .
# Run:          docker run -d -p 80:8888 shorten-link
# Use IP:80/index.html to see the web app

FROM python:3

WORKDIR /app

COPY requirements.txt .              

RUN pip3 install -r requirements.txt       

RUN apt-get -y update
RUN apt-get install -y sqlite3 libsqlite3-dev

COPY index.html main.py ./            

# CMD [ "python3 -m http.server 8888"]
ENTRYPOINT ["python3", "/app/main.py"]