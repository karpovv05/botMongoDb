# logging_setup.py
import logging
import os

# Убедимся, что папка для логов существует
os.makedirs("logs", exist_ok=True)

# Конфигурация логирования
def setup_logger(name):
    """
    Создает настроенный логгер с консольным и файловым выводом.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Минимальный уровень логов

    # Формат логов
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] (%(name)s) %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Вывод в файл
    file_handler = logging.FileHandler("logs/app.log", mode="a", encoding="utf-8")
    file_handler.setFormatter(formatter)

    # Вывод в консоль
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Добавляем обработчики
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
