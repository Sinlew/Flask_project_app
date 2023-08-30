import os

class Config(object):
   SECRET_KEY=os.environ.get('SECRET_KEY') or '34k2jzokpzpad3e2pP1324ER$#%R#9943223dfdfyh564w2$%#@232'

   DATABASE = '/base/flask_app.db'
   SQLALCHEMY_DATABASE_URI = 'sqlite:///flapp.db'
   MAX_CONTENT_LENGHT = 1024*1024