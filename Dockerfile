FROM python:3.9-alpine3.13
# from dockerhub
# https://hub.docker.com/_/python
# alpine is a lightweight linux distribution
LABEL maintainer="ladonbv"

ENV PYTHONUNBUFFERED 1
# This is a recommended best practice for Python Dockerfiles.
# This avoids writing .pyc files to disk, which can cause problems in some

# Install dependencies
# copies the requirements.txt file to the /tmp/requirements.txt
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements-dev.txt
# copy app  directory 
COPY ./app /app
WORKDIR /app
EXPOSE 8000

# run the command to install the dependencies
# runs a command on the alpine image\
ARG DEV=flase
# creates a new virtual environment in the /py directory
RUN python -m venv /py && \
    # upgrade pip
    /py/bin/pip install --upgrade pip && \
    # install the dependencies from the requirements.txt file
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
    then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    # remove the /tmp directory
    rm -rf /tmp && \
    # create a new user called django-user
    # best practice not to use the root user in the container
    adduser \
    --disabled-password \
    --no-create-home \
    django-user

# set the environment variable PATH to /py/bin:$PATH
ENV PATH="/py/bin:$PATH"

# switch to the django-user
USER django-user

