from flask import Flask, Blueprint
from .config import Config
import os, datetime
from .admin.admin import admin

app =Flask(__name__)

app.config.from_object(Config)
app.config.update(dict(DATABASE=os.path.join(app.root_path,'flapp.db')))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///flapp.db'
app.config['MAX_CONTENT_LENGHT']=1024*1024
app.permanent_session_lifetime=datetime.timedelta(days=15)

app.register_blueprint(admin, url_prefix="/admin")


from app import routes