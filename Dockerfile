FROM python:3.13.1-slim-bookworm

RUN mkdir -p /opt/bos/device/drivers/grpc-example


WORKDIR /opt/bos/device/drivers/grpc-example

RUN pip install python-dateutil
RUN python -m pip install grpcio
RUN python -m pip install grpcio-tools

COPY . /opt/bos/device/drivers/grpc-example/

CMD ["python", "server.py"]