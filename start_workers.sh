#!/bin/sh

loglevel=${PD_CELERY_LOG_LEVEL:-"INFO"}

# Start the worker
celery --app app.workers.main:app worker --loglevel "${loglevel}"
