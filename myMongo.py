from pymongo import MongoClient
from logs.logging_setup import setup_logger

client = MongoClient("mongodb://localhost:27017/")
# Создание/подключение к базе данных (если базы данных нет, она будет создана автоматически)
db = client["clients"]  # Замените на имя вашей базы данных
# Создание/подключение к коллекции (если коллекции нет, она будет создана автоматически)
collection = db["users"]  

logger = setup_logger("mongoDb")

collection.delete_many({"phone": ["792762953617"]})
