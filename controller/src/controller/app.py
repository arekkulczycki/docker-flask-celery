from celery import Celery
from kombu import Exchange, Queue

from settings import settings


app = Celery(
    "controller",
    broker=settings.celery_broker_url,
    include=["tasks"],
)

app.conf.task_queues = (
    Queue("controller", Exchange("trains", type="direct"), routing_key="controller"),
)
app.conf.task_default_queue = "controller"
