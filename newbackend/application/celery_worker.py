from celery import Celery

def make_celery(app):
    celery = Celery(
        "app",
        backend=app.config['RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    return celery