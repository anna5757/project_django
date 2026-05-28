from celery import shared_task
import time

@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y

@shared_task
def long_task():

    print("START")

    time.sleep(30)

    print("END")

    return "finished"