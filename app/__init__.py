from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

if app.debug is not True:   
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('python.log', maxBytes=1024 * 1024 * 100, backupCount=20)
    file_handler.setLevel(logging.ERROR)
    app.logger.setLevel(logging.ERROR)
    app.logger.addHandler(file_handler)

from app import views
