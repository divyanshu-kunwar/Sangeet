from app import get_app_celery

app, celery = get_app_celery()
app.app_context().push()