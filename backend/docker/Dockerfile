FROM python:3.12-alpine

# Change working directory
RUN mkdir -p /backend
WORKDIR /backend

# Arguments and environment variables
ARG PORT=5000
ENV PORT=$PORT

ARG FLASK_ENV=development
ENV FLASK_ENV=$FLASK_ENV

ARG FLASK_APP=/backend
ENV FLASK_APP=$FLASK_APP

# Installation
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY backend/*.py ./
COPY backend/api ./api

COPY docker/entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh

# Configuration
EXPOSE $PORT
WORKDIR /

ENTRYPOINT ["/backend/entrypoint.sh"]