web: daphne config.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: celery worker --app=elk.taskapp --loglevel=info