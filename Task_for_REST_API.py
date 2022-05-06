from flask import Flask
from sqlalchemy import create_engine
import json
import psycopg2
import requests


app = Flask(__name__)  #app.config["DEBUG"] = True,    TESTING = True (вкл. режим тестирования)
app.config.update(
    DEBUG=True,
    SERVER_NAME='127.0.0.1:5432'
)


@app.route('/home', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"


@app.route('/connect', methods=['GET'])
def connect_db():
    return psycopg2.connect(database="postgres", user="postgres", password="admin", # пароль, который указали при установке PostgreSQL
                            host="127.0.0.1", port="5432")

def query_db(query, args=(), one=False):
    cursor = connect_db().cursor()
    cursor.execute(query, args)
    r = [dict((cursor.description[i][0], value) \
        for i, value in enumerate(row)) for row in cursor.fetchall()]
    cursor.connection.close()
    return (r[0] if r else None) if one else r

tables = query_db("select * from mobile;")
with open("../RESTfull API/json_api.json", "w") as fp:        #октрываем файл json_api.json
    json_api = json.dump(tables, fp)                          #записываем данные таблицы в этот файл
    print ('"mobile"', 'таблица успешно записана в JSON-файл')
connect_db().close()


#Далее в разработке..
@app.route('/post', methods=['POST'])
def response_db():
    print('Connect + record')
engine = create_engine('postgresql+psycopg2://postgres:admin@127.0.0.1:5432/postgres')
engine.connect()

params = {'id': 'value1', 'model': 'value2', 'standart': 'value3', 'price': 'value4'}
#requests.post('postgresql+psycopg2://postgres:admin@127.0.0.1/postgres')
response = requests.post('postgresql+psycopg2://postgres:admin@127.0.0.1/post', data=params)
engine.disconnect()
response_db().close()

app.run()


