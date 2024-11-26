# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# install python3 & pip
RUN apt-get update && apt-get install -y python3 python3-pip

# install git
RUN apt-get install -y git

# copy requirement.txt
COPY requirements.txt /

# install app independencies
RUN pip install -r requirements.txt

# clone latest repo
RUN git clone https://github.com/kgp33/quebec_v2.git

# change working dir to quebec_v2
WORKDIR /quebec_v2