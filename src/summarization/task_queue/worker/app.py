import os

import environ
import structlog
from celery import Celery
from celery.signals import setup_logging  # noqa

logger = structlog.get_logger(__name__)

env = environ.Env()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "summarization.settings.base")

celery_main_name = os.environ.get("CELERY_MAIN_NAME", default="worker")

app = Celery(celery_main_name)
app.conf.update({
    'broker_url': env.str("BROKER_URL", default=""),
    'task_ignore_result': True,
    'result_persistent': False,
    'task_serializer': 'json',
    'imports': ("summarization.task_queue.worker.tasks",),
    'task_default_queue': 'summarization-tasks',
    'result_serializer': 'json',
    'accept_content': ['json']}
)


@setup_logging.connect
def config_loggers(*args, **kwargs):
    from logging.config import dictConfig  # noqa
    from django.conf import settings  # noqa

    dictConfig(settings.LOGGING)
