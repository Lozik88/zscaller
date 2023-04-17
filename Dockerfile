# FROM ubuntu:latest
FROM python:slim-buster
WORKDIR /app

ARG ZSCALER_USR
ARG ZSCALER_PW
ARG ZSCALER_API_KEY

ENV ZSCALER_USR=$ZSCALER_USR
ENV ZSCALER_PW=$ZSCALER_PW
ENV ZSCALER_API_KEY=$ZSCALER_API_KEY

# # some dependencies needed for the python installation
# RUN apt-get update && \
#     apt-get install -y libssl-dev openssl && \
#     apt-get install -y curl && \
#     apt-get install -y xz-utils  && \ 
#     apt-get install -y build-essential && \
#     apt-get install -y libffi-dev && \
#     apt-get install -y uuid-dev lzma-dev liblzma-dev && \
#     apt-get install -y libgdbm-compat-dev && \
#     apt-get install -y libbz2-dev
# # installing python
# RUN curl https://www.python.org/ftp/python/3.11.3/Python-3.11.3.tar.xz --output python.tar.xz
# RUN mkdir tmp && \
#     tar -xvf python.tar.xz --strip 1 -C tmp && \
#     cd tmp && \
#     ./configure && \
#     make && \
#     make install && \
#     cd .. && rm -rf tmp python.tar.xz
# installing zscaller and it's dependencies
COPY . .
RUN pip3 install .

# Running web gui in local
# https://flask.palletsprojects.com/en/2.2.x/quickstart/#a-minimal-application
# https://docs.docker.com/engine/reference/builder/#cmd
CMD [ "python3", "-m" , "flask", "--app", "webgui/main", "run", "--host=0.0.0.0" ]

