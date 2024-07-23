# myapp/tasks.py
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from datetime import datetime
from ShowTicketing.celery import app

from apps.core.publisher import BasePublisher

date_today = datetime.now().date()



@app.task(name="hello_world")
def hello_world():
    publisher = BasePublisher(
        routing_key="hello_world",
        body={
            "message": "Hello World!!"
        }
    )
    publisher.run()
    print("Hello World, am running using celery")


@app.task(name="check_celery_task")
def check_celery_task():
    print("************************Metropolitan*********************")
    print("It looks like celery is working fine")
    print("************************Metropolitan*********************")