from pymongo import MongoClient
from urllib.parse import quote_plus
from pymongo.errors import PyMongoError, OperationFailure
# # Данные для подключения
# username = "gen_user"
# password = quote_plus("P}<5t#k@?R7;;9")# URL-кодированный пароль
# print(password)
# host = "195.133.27.133"
# database = "default_db"  # Укажите имя базы данных, к которой вы хотите подключиться
# auth_source = "admin"  # Укажите базу данных, где зарегистрирован пользователь

# # Подключение к MongoDB
# client = MongoClient(f"mongodb://{username}:{password}@{host}:27017/{database}?authSource={database}&directConnection=true")

# db = client[database]
# collection = db['users']


# Подключение к MongoDB
from pymongo import MongoClient 
client = MongoClient('mongodb://gen_user:P%7D%3C5t%23k%40%3FR7%3B%3B9@195.133.27.133:27017/default_db?authSource=admin&directConnection=true')
db = client["Users"]
collection = db["Users"]


insert_result = collection.insert_one(new_user)
# print(f"Документ вставлен с id: {insert_result.inserted_id}")

# # Закрытие подключения
# client.close()


# allProcess({"tgId":"2","salebot":{"1":"2","3":"4"}})
# collection.delete_many({})
# getcourseUser_info
# getcourseDeals
# traffic_tg
# salebot
# bizon365
# collection.insert_one({'tgId': "1", 'phone': ["2"], 'email': [], 'getcourse': {'user_info': {}, 'deals': {}}, 'traffic_tg': {}, 'salebot': {}, 'bizon365': {}})
# collection.insert_one({'tgId': "2", 'phone': ["1"], 'email': [], 'getcourse': {'user_info': {}, 'deals': {}}, 'traffic_tg': {}, 'salebot': {}, 'bizon365': {}})


# insertParams({'tgId':'1','phone':'',"email":""})
# l=0
# for i in collection.find({}):
#   print(i)
#   print()
#   l+=1
# print(l)



# collection.update_one({"tgId":1234123},{"$set":{'getcourse':{"getcourseId":1000001}}})
