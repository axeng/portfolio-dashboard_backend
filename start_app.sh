#!/bin/sh

host=${PD_BACKEND_HOST:-"127.0.0.1"}
port=${PD_BACKEND_PORT:-"8000"}

# Let the DB start
python -m app.backend_pre_start

# Run migrations
alembic upgrade head

# Create initial data in DB
python -m app.database.populate_database

# Start the app
uvicorn app.main:app --host "${host}" --port "${port}"
