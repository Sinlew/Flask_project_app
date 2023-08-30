from flask import Blueprint, redirect, url_for, flash, render_template, request, session, g
import sqlite3


admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

def login_admin():
   session['admin_logged'] = 1

def isLogged():
   return True if session.get('admin_logged') else False

def logout_admin():
   session.pop("admin_logged", None)

menu = [{'url':'.index', 'title':'Панель'},{'url':'.listtub', 'title':'Список статей'},{'url':'.listuser', 'title':'Список пользователей'},
{'url':'.logout', 'title':'Выйти'}]

db=None

@admin.before_request
def before_request():
   global db
   db = g.get('link_db')

@admin.teardown_request
def teardown_request(request):
   global db
   db = None
   return request

@admin.route("/")
def index():
   if not isLogged():
      return redirect(url_for('.login'))
   return render_template("admin/index.html", menu=menu, title = "Админ панель")



@admin.route("/login", methods=["POST","GET"])
def login():
   if isLogged():
      return redirect(url_for('.index'))
   if request.method == "POST":
      if request.form['user'] == "admin" and request.form['psw'] == "asqweqadaczcsda1213":
         login_admin()
         return redirect(url_for('.index'))
      else:
         flash("Неверный логин/пароль", "error")
   
   return render_template('admin/login.html', title="Админ-панель")

@admin.route("/logout", methods=["POST","GET"])
def logout():
   if not isLogged():
      return redirect(url_for('.login'))
   
   logout_admin()

   return redirect(url_for('.login'))

@admin.route("/list")
def listtub():
   if not isLogged():
      return redirect(url_for('.login'))

   list_ = []
   if db:
      try:
         cur = db.cursor()
         cur.execute(f'SELECT title, text, url FROM posts')
         list_ = cur.fetchall()
      except sqlite3.Error as e:
         print('Ошибка получения данных из бд' + str(e))
   return render_template("admin/list.html", title="Список статей", menu=menu, list=list_)

@admin.route("/list_users")
def listuser():
   if not isLogged():
      return redirect(url_for('.login'))
   if db:
      try:
         cur = db.cursor()
         cur.execute(f'SELECT name, email, numbers FROM users')
         list_ = cur.fetchall()
      except sqlite3.Error as e:
         print('Ошибка получения данных из бд' + str(e))
   return render_template("admin/listuser.html", title="Список пользователей", menu=menu, list=list_)