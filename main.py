from flask import Flask,Response,request
from mongoDb import allProcess,makeInCorrectJson,getData,delData
from logs.logging_setup import setup_logger


logger = setup_logger("app")
app = Flask(__name__)
logger.info("Приложение запускается")


@app.route('/', methods=['GET', 'POST'])
def putUserData():
    if request.method == 'POST':
        try:
            req = request.json
            logger.info(f"Поступил POST с JSON ({req})")
            allProcess(req)

            return "Данные в бд"
        except Exception as ex:
            logger.error(f"{ex}")
            return "Чет пошло не так"
        
    if request.method == 'GET':
        try:
            data = request.args.to_dict()
            logger.info(f"Поступил GET с  Query ({data})")
            if data.get("getcourseUser_info"):
                logger.info(f"Данные с ключом getcourseUser_info")
                goodJson = makeInCorrectJson(data,"getcourseUser_info")
                allProcess(goodJson)
                return "Добавил"
            if data.get("getcourseDeals"):
                logger.info(f"Данные с ключом getcourseDeals")
                goodJson = makeInCorrectJson(data,"getcourseDeals")
                allProcess(goodJson)
                return "Добавил"
            if data.get("traffic_tg"):
                logger.info(f"Данные с ключом traffic_tg")
                goodJson = makeInCorrectJson(data,"traffic_tg")
                allProcess(goodJson)
                return "Добавил"
            if data.get("salebot"):
                goodJson = makeInCorrectJson(data,"salebot")
                logger.info(f"Данные с ключом salebot")
                allProcess(goodJson)
                return "Добавил"
            if data.get("bizon365"):
                goodJson = makeInCorrectJson(data,"bizon365")
                logger.info(f"Данные с ключом bizon365")
                allProcess(goodJson)
                return "Добавил"
            else:
                logger.info(f"В запросе нет необходимого параметра")
                return "В запросе нет необходимого параметра)"
        except Exception as ex:
            logger.error(f"{ex}")

@app.route('/get', methods=['GET'])
def dataUnswer():
    # x = str(getData()).replace("{'_id'","---------{'_id'",)
    # return x
    return Response(getData(), mimetype='application/json')
        
@app.route('/del', methods=['GET'])
def delUnswer():
    delData()
    return "OK"
    



if __name__ == '__main__':
    app.run()
