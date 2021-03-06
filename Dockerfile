FROM raingsei/pyurdme
RUN add-apt-repository ppa:fkrull/deadsnakes
RUN apt-get update
RUN apt-get -y install wget python3.5 python-pip
RUN wget https://bootstrap.pypa.io/ez_setup.py -O - | sudo python3.5
RUN git clone https://github.com/falconry/falcon.git
RUN cd falcon && python3.5 setup.py install
RUN rm -r falcon
RUN git clone https://github.com/beirbear/HarmonicPE.git
RUN git clone https://github.com/beirbear/HarmonicIO.git
RUN apt-get -y install python-zmq libffi-dev python-dev
RUN pip install sqlalchemy boto paramiko python-swiftclient python-novaclient
RUN git clone https://github.com/ahellander/molnsutil.git
RUN cd molnsutil && python setup.py install
RUN rm -r molnsutil
WORKDIR /HarmonicIO
CMD ['/usr/bin/python3.5','-m','worker']