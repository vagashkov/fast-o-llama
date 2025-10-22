import logging

from fastapi import HTTPException
from http import HTTPStatus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def report_error(error_text: str) -> None:
    """
    Routine for uniform error processing (log, raise, report)
    :param error_text:
    :return:
    """
    logger.error(error_text)
    raise HTTPException(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        detail=error_text
    )
