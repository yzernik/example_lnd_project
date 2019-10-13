FROM ubuntu:18.04

RUN apt-get update && apt-get install -y software-properties-common && add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && apt-get install -y python3.6 python3.6-dev python3-pip

RUN ln -sfn /usr/bin/python3.6 /usr/bin/python3 && ln -sfn /usr/bin/python3 /usr/bin/python && ln -sfn /usr/bin/pip3 /usr/bin/pip

RUN apt-get update && apt-get install -y \
    curl \
    git

COPY requirements.txt /

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY example_lnd_project/ /app/src

WORKDIR /app

# Install the gRPC files for lnd.
RUN git clone https://github.com/googleapis/googleapis.git
RUN curl -o rpc.proto -s https://raw.githubusercontent.com/lightningnetwork/lnd/master/lnrpc/rpc.proto
RUN python -m grpc_tools.protoc --proto_path=googleapis:. --python_out=. --grpc_python_out=. rpc.proto
RUN cp rpc_pb2.py src/
RUN cp rpc_pb2_grpc.py src/

# Copy the entrypoint script.
COPY "docker/app/start-app.sh" .
RUN chmod +x start-app.sh
