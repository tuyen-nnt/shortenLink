# Build image:  docker build -t shortenlink:1.0 .
# Run:          docker run -d -p 80:8888 shortenlink:1.0

FROM python:3-alpine

WORKDIR /app
EXPOSE 8888
# map port 8888 tu trong cointainer ra ngoai may may


RUN python -m pip install --upgrade pip && pip3 install tornado

COPY index2.html /app/index.html
COPY main2.py ./

ENTRYPOINT ["python3", "/app/main2.py"]
