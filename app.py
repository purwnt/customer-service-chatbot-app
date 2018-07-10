# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from flask_pymongo import PyMongo


#Flask
app = Flask(__name__)
mongo = PyMongo(app)

#Sastrawi
# create stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

#Setup chatterbot
bot = ChatBot(
    "Nusanetbot",
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': 'Help me!',
            'output_text': 'Ok, here is a link: http://chatterbot.rtfd.org'
        }
    ],
    read_only=True,
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database='./database.sqlite3'
)

bot.set_trainer(ListTrainer)

'''
#Chatterbot
indonesian_bot = ChatBot("Nusanetbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")
indonesian_bot.set_trainer(ChatterBotCorpusTrainer)
#indonesian_bot.train("chatterbot.corpus.indonesia")
'''


@app.route('/a')
def show_all():
    tasks = mongo.db.users.find()
    return render_template('list.html', tasks=tasks)

#Routing
@app.route("/")
def home():
    return render_template("index.html")

def identifikasi_pertanyaan(text):
    tanya = ['apa', 'siapa', 'kapan']
    if(text in tanya):
        return('pertanyaan')
    else:
        return("bkn pertanyaan")

def getPaket(text):
    if("paketid" in text):
        return "paket anda adalah 23324 " 

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    #userTextStem = stemmer.stem(str(userText))
    return identifikasi_pertanyaan(userText)
    return getPaket(userText)
    print(userText)
    #bisa simpan nama di database dan ngambil data customer berdasarkan cust.id
    #return str(bot.get_response(userText))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
