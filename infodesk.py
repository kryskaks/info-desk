from flask import Flask, session

app = Flask(__name__)

app.config.from_object('config')

import views