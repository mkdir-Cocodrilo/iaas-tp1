from celery import Celery, chain
from celery.schedules import crontab

celery_app = Celery(
    'celery_app',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)

celery_app.conf.timezone = 'Europe/Paris'

celery_app.conf.beat_schedule = {
    'call_api_and_run_postgres_every_day_at_6pm': {
        'task': 'celery_app.call_api_and_run_postgres',
        'schedule': crontab(hour=18, minute=30),
    },
}

@celery_app.task(name='celery_app.call_api')
def call_api(*args, **kwargs):
    import requests
    response = requests.get("http://fastapi_app:8080/trigger-youtube-api-job")
    print(response.json())
    return response.json()  # Return something if needed

@celery_app.task(name='celery_app.run_postgres')
def run_postgres(*args, **kwargs):
    import subprocess
    result = subprocess.run(["python", "/app/postgres.py"], capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)

@celery_app.task(name='celery_app.call_api_and_run_postgres')
def call_api_and_run_postgres(*args, **kwargs):
    return chain(call_api.s(), run_postgres.s())()
