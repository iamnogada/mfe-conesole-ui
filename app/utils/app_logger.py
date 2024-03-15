import logging
import logging.config

uvicorn_access = logging.getLogger("uvicorn.access")

log = logging.getLogger("uvicorn")
log.setLevel(logging.getLevelName(logging.DEBUG))

log.info(__name__)