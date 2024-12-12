from pymongo import MongoClient
from logs.logging_setup import setup_logger
import json

client = MongoClient("mongodb://localhost:27017/")
# Создание/подключение к базе данных (если базы данных нет, она будет создана автоматически)
db = client["clients"]  # Замените на имя вашей базы данных
# Создание/подключение к коллекции (если коллекции нет, она будет создана автоматически)
collection = db["users"]  

logger = setup_logger("mongoDb")



def checkKeyInNewJs(jsNewData:dict):
  logger.info(f"Вызов метода getKey с данными {jsNewData}")
  try:
    if jsNewData.get("tgId"): return "tgId"
    elif jsNewData.get("phone"): return "phone"
    elif jsNewData.get("email"): return "email"
    else: return False
  except Exception as ex:
    logger.error(ex)

def getKeyParamsFromNewJs(jsNewData:dict):
  try:
    logger.info(f"Вызов метода getKeyParams с данными {jsNewData}")
    listParams = []
    if jsNewData.get("getcourseUser_info"):
      listParams.append("getcourseUser_info")
    if jsNewData.get("getcourseDeals"):
      listParams.append("getcourseDeals")
    if jsNewData.get("traffic_tg"):
      listParams.append("traffic_tg")
    if jsNewData.get("salebot"):
      listParams.append("salebot")
    if jsNewData.get("bizon365"):
      listParams.append("bizon365")
    return listParams
  except Exception as ex:
    logger.error(ex)
  
def insertParams(jsNewData:dict,mainType):
  try:
    logger.info(f"Вызов метода insertParams с данными {jsNewData}")
    
    if not mainType: 
      logger.info(f"Метод mainType = {mainType}")
      return False
    
    findData = collection.find_one({mainType:jsNewData[mainType]})
    logger.info(f"Поступил обновляемый массив с данными {mainType}:{jsNewData[mainType]}")

    
    if jsNewData.get("getcourseUser_info") and not findData["getcourse"]["user_info"]:
      findData["getcourse"]["user_info"] = jsNewData["getcourseUser_info"]
      logger.info(f"Добавлены новые данные getcourseUser_info")
    if jsNewData.get("getcourseDeals"):
      findData["getcourse"]["deals"].append(jsNewData["getcourseDeals"])
      logger.info(f"Добавлены новые данные deals")
    if jsNewData.get("traffic_tg"):
      findData["traffic_tg"].append(jsNewData["traffic_tg"])
      logger.info(f"Добавлены новые данные traffic_tg")
    if jsNewData.get("salebot"):
      findData["salebot"].append(jsNewData["salebot"])
      logger.info(f"Добавлены новые данные salebot")
      
    if jsNewData.get("bizon365"):
      findData["bizon365"].append(jsNewData["bizon365"])
      logger.info(f"Добавлены новые данные bizon365")


    collection.update_one({mainType:jsNewData[mainType]},{"$set":findData})
    logger.info(f"Данные добавлены в базу данных")
  except Exception as ex:
    logger.error(ex)


def insertBase(jsNewData:dict):
    logger.info(f"Вызов метода insertBase с данными {jsNewData}")
    js = {
          "tgId": "",
          "phone": [],
          "email": [],
          "getcourse": {
            "user_info":{},
            "deals":[]
          },
          "traffic_tg": [],
          "salebot": [],
          "bizon365": []
        }
    try:  
      tgIdNew = jsNewData.get("tgId")
      phoneNew = jsNewData.get("phone")
      emailNew = jsNewData.get("email")
      
      if tgIdNew: tgIdNew=str(tgIdNew)
      if phoneNew: phoneNew=str(phoneNew)
      if emailNew: emailNew=str(emailNew)
      
      
      tgIdDb = collection.find_one({"tgId":tgIdNew}) 
      phoneDb = collection.find_one({"phone":phoneNew})
      emailDb = collection.find_one({"email":emailNew})
      
      # print(phoneDb)
      # return
      if not tgIdNew and not phoneNew and not emailNew:
        logger.info(f"insertBase с данными {jsNewData} не прошли валидацию")

        return
      # Поиск записи по tgId
      if tgIdNew and tgIdDb and tgIdDb["tgId"] == tgIdNew:
        logger.info(f"insertBase tgId наден")
        if phoneNew and phoneNew not in tgIdDb["phone"]:
            tgIdDb["phone"].append(phoneNew)
            logger.info(f"insertBase phone добавлен")
            
            if phoneDb and not phoneDb["tgId"]:
              logger.info(f"insertBase найден Дубль по Телефону")
              tgIdDb = antiDuble(tgIdDb,phoneDb,"phone")
              
        if emailNew and emailNew not in tgIdDb["email"]:
              tgIdDb["email"].append(emailNew)
              logger.info(f"insertBase email добавлен")
              
              if emailDb and not emailDb["tgId"]:
                logger.info(f"insertBase найден Дубль по Email")
                tgIdDb = antiDuble(tgIdDb,emailDb,"email")
              
        collection.update_one({"tgId":tgIdNew},{"$set":tgIdDb})
                  

      #############phone
      elif phoneNew and phoneDb and phoneNew in phoneDb["phone"]:
            logger.info(f"insertBase phone найден")
            if tgIdNew:
              if not phoneDb["tgId"]:
                logger.info(f"insertBase Есть новый tgId но нет телефоа. добавлен")
                phoneDb["tgId"] = tgIdNew
              elif phoneDb["tgId"] and emailDb == None:
                
                logger.info(f"insertBase Данные по tgId не надены, но телефон есть, Добавлен новый пользователь")   
                if tgIdNew:
                  js["tgId"] = tgIdNew
                if phoneNew:
                  js["phone"].append(phoneNew)
                if emailNew:
                  js["email"].append(emailNew)

                collection.insert_one(js)
                return
              
              elif phoneDb["tgId"] and emailDb != None:
                
                logger.info(f"insertBase Данные по tgId не надены, но телефон есть и email, Добавлен новый пользователь")   
                if tgIdNew:
                  js["tgId"] = tgIdNew
                if phoneNew:
                  js["phone"].append(phoneNew)
                if emailNew:
                  js["email"].append(emailNew)

                collection.insert_one(js)
                return
             
            elif emailNew and emailNew not in phoneDb["email"]: 
              logger.info(f"insertBase email наден")
              phoneDb["email"].append(emailNew)
              logger.info(f"insertBase email добавлен")

            collection.update_one({"phone":phoneNew},{"$set":phoneDb})
            return
           
      #############email
      elif emailNew and emailDb and emailNew in emailDb["email"]:
        
            if tgIdNew:
              if not emailDb["tgId"]:
                logger.info(f"insertBase tgId добавлен")             
                emailDb["tgId"] = tgIdNew
              else:
                logger.info(f"insertBase Данные по tgId не надены, но email есть, Добавлен новый пользователь")   
                if tgIdNew:
                  js["tgId"] = tgIdNew
                if phoneNew:
                  js["phone"].append(phoneNew)
                if emailNew:
                  js["email"].append(emailNew)
                  
                collection.insert_one(js)
                return
              
              
            if phoneNew and phoneNew not in emailDb["phone"]:
              logger.info(f"insertBase phone добавлен")
              
              emailDb["phone"].append(phoneNew)
              
            collection.update_one({"email":emailNew},{"$set":emailDb})
            return
      else:
        logger.info(f"insertBase Данные не надены")
        if tgIdNew:
          js["tgId"] = tgIdNew
        if phoneNew:
          js["phone"].append(phoneNew)
        if emailNew:
          js["email"].append(emailNew)
          
        logger.info(f"insertBase новые данные добавлены в DB")

        collection.insert_one(js)
    except Exception as ex:
        logger.error(ex)

def allProcess(jsNewData:dict):
  try:
    logger.info(f"Вызов метода allProcess с данными {jsNewData}")
    insertBase(jsNewData)
    mainType = checkKeyInNewJs(jsNewData)
    insertParams(jsNewData,mainType)
  except Exception:
    logger.error(Exception)
  
  
def makeInCorrectJson(data:dict,key:str)->dict:
    try:
      logger.info(f"Заупстился makeInCorrectJson с параметрами {data} с key = {key}")

      newDict = {}
      if data.get("tgId"):
        newDict["tgId"] = data.pop("tgId")
      if data.get("phone"):
        newDict["phone"] = data.pop("phone")
      if data.get("email"):
        newDict["email"] = data.pop("email")
        
      if key == "getcourseUser_info":
        data.pop("getcourseUser_info")
        newDict["getcourseUser_info"] = data
        
      if key == "getcourseDeals":
        data.pop("getcourseDeals")
        newDict["getcourseDeals"] = data
        
      if key == "traffic_tg":
        data.pop("traffic_tg")
        newDict["traffic_tg"] = data
      
      if key == "salebot":
        data.pop("salebot")
        newDict["salebot"] = data
        
      if key == "bizon365":
        data.pop("bizon365")
        newDict["bizon365"] = data
      
      logger.info(f"makeInCorrectJson вернул {newDict}")
      return newDict
    except Exception:
      logger.error(Exception)
  

def getData():
  # return [i for i in collection.find({})]
  return json.dumps(list(collection.find({}, {'_id': 0})),indent=4, ensure_ascii=False)

def delData():
  collection.delete_many({})
  
  
def antiDuble(tgIdDb,dubleDb,attr):
  try:
    for i in dubleDb.items():
        if i[1] and i[0] == "getcourse" and i[1]:
            if i[1]["user_info"]:
                tgIdDb["getcourse"]["userInfo"] = i[1]["user_info"]
            if i[1]["deals"]:
                for i2 in i[1]["deals"]:
                    tgIdDb["getcourse"]["deals"].append(i2)
        elif i[0] not in ["tgId","phone","email","_id"]:
          for data in i[1]:
                tgIdDb[i[0]].append(data)
    for phone in dubleDb["phone"]:
      if phone not in tgIdDb["phone"]:
        tgIdDb["phone"].append(phone)
    if dubleDb["email"]:
      for email in dubleDb["email"]:
        tgIdDb["email"].append(email) 
    collection.delete_many({attr: dubleDb[attr]})
    return tgIdDb

    
      
      
  except Exception:
    logger.error(Exception)

  