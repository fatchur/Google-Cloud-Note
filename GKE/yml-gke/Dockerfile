FROM ubuntu:16.04

COPY . /scripts/
WORKDIR /scripts

# install dependencies
RUN apt-get update && apt-get install -y \
  wget 
RUN apt-get install -y python3-dev python3-pip
RUN pip3 install -r requirements.txt
RUN apt-get update && apt-get install -y libgtk2.0-dev

EXPOSE 8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:app"] 
