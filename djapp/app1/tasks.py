from __future__ import annotations

from celery import shared_task

import structlog
# import logging

from .models import Value

logger = structlog.get_logger()
# logger = logging.getLogger(__name__)


@shared_task
def calc(pk: int):
    obj = Value.objects.get(pk=pk)
    x = obj.x
    y = obj.y
    result = x + y
    # logger.info("add:\nx=%s\ny=%s\nresult=%s", x, y, result) # stdlib or structlog
    logger.info("add", x=x, y=y, result=result) # structlog
    if obj.result != result:
        obj.result = result
        obj.save()
    return result
