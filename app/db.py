from app import app
import sqlite3
from flask import g


def connect_db():
   conn=sqlite3.connect(app.config['DATABASE'])
   conn.row_factory=sqlite3.Row
   return conn

def create_db():
   db = connect_db()
   with app.open_resource('sq_db.sql', mode='r') as f:
      db.cursor().executescript(f.read())
   db.commit()
   db.close()

def get_db():
   if not hasattr(g, 'link_db'):
      g.link_db = connect_db()
   return g.link_db