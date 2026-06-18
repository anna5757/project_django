from celery import shared_task
import time

@shared_task
def add(x, y):
    time.sleep(15)
    return x + y


@shared_task
def mul(x, y):
    time.sleep(15)
    return x * y

@shared_task
def long_task():

    print("START")

    time.sleep(30)

    print("END")

    return "finished"


@shared_task
def morning_notification():
    message = (
        f"Доброе утро!"
    )
    print(message)
    return message

