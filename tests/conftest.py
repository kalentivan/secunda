# Базовый URL для тестов
import subprocess
import time

import pytest
import requests
from dotenv import load_dotenv

BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture(scope="session", autouse=True)
def start_server():
    # Запускаем сервер
    load_dotenv()
    proc = subprocess.Popen(["uvicorn", "main:app", "--port", "8000"])
    time.sleep(2)  # Подождать, пока сервер стартует

    # Проверить, что сервер доступен
    for _ in range(10):
        try:
            requests.get("http://127.0.0.1:8000/docs")
            break
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)

    yield
    proc.terminate()
