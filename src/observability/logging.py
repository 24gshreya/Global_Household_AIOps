import json
import logging


logger = logging.getLogger(
    "global-household-aiops"
)

logging.basicConfig(
    level=logging.INFO
)


def log_request(
    payload: dict,
) -> None:

    logger.info(
        json.dumps(
            payload,
            default=str,
        )
    )