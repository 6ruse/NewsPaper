from celery import shared_task
import time

@shared_task
def send_subscribers():
    time.sleep(10)
    print("Hello, world!")