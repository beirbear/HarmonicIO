# Harmonic IO Streaming Framework

Framework for distributed task execution, key components:

Master Node - maintains queue of tasks, workers, their containers, etc.
Worker Node - manages and hosts docker containers.
Stream_Connector - client for sending tasks for distributed execution.

**This version has support for containers.**

Forked from https://github.com/beirbear/HarmonicIO


## Quickstart

Setup with master and worker on a single node:

Install Docker

Clone and Install:
```
$ git clone https://github.com/benblamey/HarmonicIO.git
$ cd HarmonicIO
$ pip3 install -e .
```

Edit `master/configuration.json` and `worker/configuration.json` so that the addresses are for the local machine (localhost seems problematic).

Start the master and worker:
```
$ ./runMaster.sh
$ ./runWorker.sh
```

Start an (example) processing container on the worker (localhost) node:
```
$ curl -X POST "http://<local-ip>:8081/docker?token=None&command=create" --data '{"c_name" : "benblamey/hio-example:latest", "num" : 1}'
```

Check the container is running:
```
$ docker ps
CONTAINER ID        IMAGE                          COMMAND               CREATED             STATUS              PORTS                  NAMES
5c6146b750ab        benblamey/hio-example:latest   "python example.py"   33 minutes ago      Up 33 minutes       0.0.0.0:9000->80/tcp   happy_jepsen
```

Use the Stream Connector to send data:

```
from harmonicIO.stream_connector.stream_connector import StreamConnector

config = {'master_host': '<local-ip>',
          'master_port': 8080,
          'container_name': 'benblamey/hio-example:latest',
          'container_os': 'ubuntu'}
                       
sc = StreamConnector(config['master_host'], config['master_port'], max_try=1, std_idle_time=1)

message_bytes = b'test data'

sc.send_data(config['container_name'],
             config['container_os'],
             message_bytes)
```


Print the logs to check the container executed the task:
```
$ docker logs happy_jepsen 
Listening for tasks...
attempting to open local port: 0.0.0.0:80
Streaming from  172.17.0.1 : 40742
message was bytes: 125
```
