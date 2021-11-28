import sys
from loguru import logger
from datetime import datetime

LOG_FILE = False

FORMAT = "<yellow><level>{level: <9}</level></yellow> \
<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> \
msg = <level>{message}</level>  at {time:YYYY-MM-DD HH:mm:ss.SSS - zz!UTC}"


logger.remove()

if LOG_FILE:
    today = datetime.utcnow()
    logger.add(
        f"logs/data/{today.year}/{today.month}/{today.day}/logs.log",
        retention="1 days",
        rotation="500 mb",
        format=FORMAT,
        level="TRACE",
    )

else:
    logger.add(sys.stderr, format=FORMAT, level="TRACE")
