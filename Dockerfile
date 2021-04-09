FROM python:3.6-slim
RUN apt-get update
RUN apt-get -y install graphviz
ADD . /vs
WORKDIR /vs
RUN pip install recursion-visualiser