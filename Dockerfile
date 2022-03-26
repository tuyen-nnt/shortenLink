# Build image:  docker build -t shortenlink:4.0 .
# Run:          docker run -d -p 88:8888 -e DB_HOST=172.17.0.1 -e DB_USER=root -e DB_PASSWORD=Dauphongthui@9116 -e DB_NAME=url --name tuyenngu shortenlink:4.0
# Run on VM: docker run senrie/test-repo

FROM python:3

WORKDIR /app
# EXPOSE map port 8888 tu trong cointainer ra ngoai may may

COPY . /app

# It functions as a type of documentation between the person who builds the image and the person who runs the container
# https://docs.docker.com/engine/reference/builder/#expose
EXPOSE 8888

RUN pip3 install -r requirements.txt

ENV DB_HOST 172.31.50.2
ENV DB_USER root
ENV DB_PASSWORD tuyen
ENV DB_NAME shortlink

# https://stackoverflow.com/questions/29663459/python-app-does-not-print-anything-when-running-detached-in-docker
ENTRYPOINT ["python3", "-u", "/app/main.py"]
