# South African Lottery API Docker Image
# Creation Date: 09 Sept 2020, 00:38
# Author: Sizwe-se-Afrika Immaculate Mkhonza

# base image, linux distro os
FROM ubuntu:latest

MAINTAINER Sizwe-se-Afrika Immaculate Mkhonza kin.afro@gmail.com

ENV CONTAINER_PATH=./za.lottery.api

# work directory.
WORKDIR $CONTAINER_PATH

# copy all this dir's to za.lottery.api 
COPY . $CONTAINER_PATH

# setup requirements
RUN apt-get install -y python3
RUN /usr/local/bin/python -m pip install --upgrade pip

# import all the packages required by the api from requirements.txt file.
RUN pip --no-cache-dir install -r requirements.txt
RUN pip install pymongo

# region expose, the api url port; 5000
ENV CONTAINER_PORT_TO_EXPOSE=5000
ENV EXPOSE_TO_PORT=1989
# expose, the api latest_draw_result_url port; 5000
EXPOSE $EXPOSE_TO_PORT $CONTAINER_PORT_TO_EXPOSE
# endregion

# region ENTRYPOINT command makes the container executable
ENV PROGRAM_ENTRY_POINT = "python"
ENTRYPOINT $PROGRAM_ENTRY_POINT

# arguments
ENV PROGRAM = "server.py"
CMD $PROGRAM
# endregion