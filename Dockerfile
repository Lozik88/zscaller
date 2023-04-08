FROM ubuntu:latest
WORKDIR /app
# some dependencies needed for the python installation
RUN apt-get update && \
    apt-get install -y libssl-dev openssl && \
    apt-get install -y curl && \
    apt-get install -y xz-utils  && \ 
    apt-get install -y build-essential && \
    apt-get install -y libffi-dev && \
    apt-get install -y uuid-dev lzma-dev liblzma-dev && \
    apt-get install -y libgdbm-compat-dev
# installing python
RUN curl https://www.python.org/ftp/python/3.11.3/Python-3.11.3.tar.xz --output python.tar.xz
RUN mkdir tmp && \
    tar -xvf python.tar.xz --strip 1 -C tmp && \
    cd tmp && \
    ./configure && \
    make && \
    make install && \
    cd .. && rm -rf tmp python.tar.xz
# installing zscaller and it's dependencies
RUN pip3 install .
COPY . .
