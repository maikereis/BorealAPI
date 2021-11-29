import sys
from loguru import logger
from datetime import datetime

# Select when log in a file or in terminal.
LOG_ON_FILE = True

FORMAT = "<yellow><level>{level: <9}</level></yellow> \
<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> \
msg = <level>{message}</level>  at {time:YYYY-MM-DD HH:mm:ss.SSS - zz!UTC}"

# Need to remove precious logger configuration.
logger.remove()

if LOG_ON_FILE:
    today = datetime.utcnow()
    logger.add(
        f"logs/data/logs_from.log",
        retention="30 days",
        rotation="1 day",
        format=FORMAT,
        level="TRACE",
        compression='zip'
    )

else:
    logger.add(sys.stderr, format=FORMAT, level="TRACE")
