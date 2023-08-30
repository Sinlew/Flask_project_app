from app import app
from flask import render_template, url_for, request, flash, session, redirect, abort, make_response
from .forms import LoginForm, SigninForm, PostForm
import sqlite3
from .db import *
from .FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash
import re
from .UserLogin import UserLogin
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy



login_manager=LoginManager(app)
login_manager.login_view='signin'
login_manager.login_message = "Авторизуйтесь для доступа к странице"
login_manager.login_message_category = "success"


db2 = SQLAlchemy(app)
dbase =  None

@login_manager.user_loader
def load_user(user_id):
   print("user_loaded")
   return UserLogin().fromDB(user_id, dbase)

@app.before_request
def db_connect():
   global dbase
   db = get_db()
   dbase = FDataBase(db)

@app.teardown_appcontext
def close_db(error):
   if hasattr(g, 'link_db'):
      g.link_db.close()


@app.route("/")
def mainpage():
   session.permanent=True
   if current_user.is_authenticated:
      return redirect(url_for("profile"))
   
   if not current_user.is_authenticated:
      return redirect(url_for("signin"))

   res = make_response(render_template('start_page.html', title="Главная стрнаица", menu=dbase.getMenu()),301)
   return res



@app.route("/chat")
def chat():
   print(url_for('chat'))
   return render_template('chat_page.html', title="Чат", menu=dbase.getMenu())

@app.route("/news")
def news():
   print(url_for('news'))
   return render_template('news_page.html', title="Новости", menu=dbase.getMenu(), posts = dbase.getPostsAnonce())

@app.route("/profile")
@login_required
def profile():
   
   return render_template("user_profile_page.html", title="Профиль", menu=dbase.getMenu())
   

@app.route("/registration" , methods=['POST','GET'])
def registration():
   pattern_number = '^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'
   form = LoginForm()
   if form.validate_on_submit():
      if re.fullmatch(pattern_number, form.phone.data):
         hash_ = generate_password_hash(form.password.data) 
         res = dbase.addUser(form.username.data,form.email.data,form.phone.data,hash_)
         
         if res:
            flash("Вы успешно зарегестрированы", category="success")
            return redirect(url_for('signin'))
         else:
            flash("ошибка бд", category="error")   
   print(url_for('registration'))
   return render_template('reg_page.html',title="Регистрация", menu=dbase.getMenu(), form=form)

@app.route("/signin", methods=['POST','GET'])
def signin():
   if current_user.is_authenticated:
      return redirect(url_for("profile"))
   form = SigninForm()
   if form.validate_on_submit():
      user = dbase.getUserByEmail(form.email.data)
      if user and check_password_hash(user['psw'],form.password.data):
         userLogin = UserLogin().create(user)
         rm = form.remind_me.data
         login_user(userLogin, remember=rm)
         return redirect(request.args.get("next") or url_for('profile'))

      flash("Неверный логин или пароль","error") 

   
   return render_template('sign_page.html',title="Авторизация", menu=dbase.getMenu(), form=form)   

@app.route("/new_post" , methods=['POST','GET'])
def add_post():
   form = PostForm()
   if form.validate_on_submit():
      if len(form.name.data) > 4 and len(form.post.data) > 10:
         res = dbase.addPost(form.name.data, form.post.data, form.url.data)
         if not res:
            flash('Неудалось добавить новость', category='error')
         else:
            flash('Cтатья добавлена', category='success')
      else:
        flash('Неудалось добавить новость', category='error')  

   return render_template('add_post.html',title="Новая запись", menu=dbase.getMenu(), form=form)

@app.route("/post/<alias>")
@login_required
def showPost(alias):
   title, post = dbase.getPost(alias)
   print(post)
   if not title:
      abort(404)
   
   return render_template('post.html', menu=dbase.getMenu(), title=title, post=post)

@app.route("/user_avatar")
@login_required
def user_avatar():
   img = current_user.getAvatar(app)
   if not img:
      print("error")
      return ""

   h = make_response(img)
   h.headers['Content-Type']='image/png'
   return h

@app.route("/upload", methods = ['POST','GET'])
@login_required
def upload():
   if request.method=='POST':
      file_ = request.files['file']
      if file_ and current_user.verifyExt(file_.filename):
         try:
            img = file_.read()
            res = dbase.updateUserAvatar(img, current_user.get_id())
            if not res:
               flash("Ошибка обновления аватара","error")
            flash("Аватар обновлен","success")
         except FileNotFoundError as e:
            flash("Ошибка чтения файла", "error")
   else:
      flash("Ошибка обновления аватара", "error")
   
   return redirect(url_for('profile'))

@app.route("/logout")
@login_required
def logout():
   logout_user()
   session.pop('userLogged',None)
   flash("Выход из аккаунта")
   return redirect(url_for('signin'))


@app.errorhandler(404)
@app.errorhandler(401)
def pagenotfound(error):
   return render_template('pg404.html',title="Страница не найдена", menu=dbase.getMenu()), 404