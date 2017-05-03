from celery import Celery

app = Celery('appl', backend='http:127.0.0.1:5672', broker='http:127.0.0.1:5672')

@app.task
def add(x, y):
    return x + y
