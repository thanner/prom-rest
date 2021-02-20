# Ubuntu
FROM ubuntu:latest
RUN apt-get update

# Python
RUN apt-get install -y --no-install-recommends python3-pip

# Java
RUN apt-get install -y --no-install-recommends openjdk-8-jdk

# Prepare Project
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt

# Execute
EXPOSE 5000
CMD python3 ./index.py