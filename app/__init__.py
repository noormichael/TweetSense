from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

import logging
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

from app import views
