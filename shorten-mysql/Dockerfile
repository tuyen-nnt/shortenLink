# Build image:  docker build -t shortenlink:4.0 .
# Run:          docker run -d -p 88:8888 -e DB_HOST=172.17.0.1 -e DB_USER=root -e DB_PASSWORD=Dauphongthui@9116 -e DB_NAME=url --name tuyenngu shortenlink:4.0

FROM python:3-alpine

WORKDIR /app
# EXPOSE map port 8888 tu trong cointainer ra ngoai may may

RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT ["python3", "/app/main_mysql.py"]
