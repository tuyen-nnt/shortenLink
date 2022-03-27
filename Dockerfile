# docker build -t senrie/shortenlink:1.1 .
# docker run --rm -p 80:8080 senrie/shortenlink:1.0

FROM python:3


WORKDIR /app
# EXPOSE map port 8888 tu trong cointainer ra ngoai may may

RUN pip3 install -r requirements.txt


COPY . /app



# It functions as a type of documentation between the person who builds the image and the person who runs the container
# https://docs.docker.com/engine/reference/builder/#expose
EXPOSE 8080

ENV DB_HOST 172.31.50.2
ENV DB_PORT 3306
ENV DB_USER root
ENV DB_PASSWORD tuyen
ENV DB_NAME shortlink

# Default value is 8080, use this env to change listening port
#ENV WEB_LISTEN_PORT 8080

# https://stackoverflow.com/questions/29663459/python-app-does-not-print-anything-when-running-detached-in-docker
ENTRYPOINT ["python3", "-u", "/app/main.py"]
