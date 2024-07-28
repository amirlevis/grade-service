FROM python:3.12-alpine
ENV PYTHONUNBUFFERED=1

WORKDIR /app
ADD . /app

RUN pip3 install --upgrade pip && \
    pip install pipenv && \
    pipenv install --system

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh