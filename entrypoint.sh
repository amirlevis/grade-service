#!/bin/sh

pipenv run alembic upgrade head
exec pipenv run gunicorn -w "$SERVICE_WORKERS" -k uvicorn.workers.UvicornWorker app.server:app --bind 0.0.0.0:"$APP_PORT"