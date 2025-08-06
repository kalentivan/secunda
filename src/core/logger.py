import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


LOG_PATH = "./logs"
Path(LOG_PATH).mkdir(exist_ok=True, parents=True)

# Создаем основной логгер
logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)

# Форматтер
formatter = logging.Formatter("%(levelname)s %(asctime)s - %(message)s")

# Обработчики
info_handler = RotatingFileHandler(f"{LOG_PATH}/info.log", maxBytes=1024*1024, backupCount=5, encoding='utf-8')
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(formatter)

warning_handler = RotatingFileHandler(f"{LOG_PATH}/warning.log", maxBytes=1024*1024, backupCount=5, encoding='utf-8')
warning_handler.setLevel(logging.WARNING)
warning_handler.setFormatter(formatter)

error_handler = RotatingFileHandler(f"{LOG_PATH}/error.log", maxBytes=1024*1024, backupCount=5, encoding='utf-8')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)

# CRITICAL лог
critical_handler = RotatingFileHandler(f"{LOG_PATH}/critical.log", maxBytes=1024*1024, backupCount=5, encoding='utf-8')
critical_handler.setLevel(logging.CRITICAL)
critical_handler.setFormatter(formatter)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# Добавляем обработчики
logger.addHandler(console_handler)
logger.addHandler(info_handler)
logger.addHandler(warning_handler)
logger.addHandler(error_handler)
logger.addHandler(critical_handler)

# Настройка стандартных логгеров
uvicorn_logger = logging.getLogger("uvicorn")
uvicorn_logger.handlers = []
uvicorn_error_logger = logging.getLogger("uvicorn.error")
uvicorn_error_logger.handlers = []
fastapi_logger = logging.getLogger("fastapi")
fastapi_logger.handlers = []
