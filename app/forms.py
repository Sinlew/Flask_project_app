from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, InputRequired, Length, EqualTo

class LoginForm(FlaskForm):
   username = StringField('Имя', validators=[DataRequired(),InputRequired(), Length(min=4,max=20, message="Имя должен быть от 4 до 20 символов")])
   email = StringField('Почта', validators=[DataRequired(),Email("Некорректный email"), InputRequired()])
   phone = StringField('Телефон', validators=[DataRequired(), InputRequired()])
   password = PasswordField('Пароль', validators=[DataRequired(),InputRequired(),Length(min=4,max=100, message="Пароль должен быть от 4 до 100 символов")])
   ret_password = PasswordField('Повторить пароль', validators=[DataRequired(),InputRequired(), Length(min=4,max=100, message="Пароль должен быть от 4 до 100 символов"), EqualTo("password", "Пароли должны совпадать")])
   submit = SubmitField('Зарегестрироваться')

class SigninForm(FlaskForm):
   email = StringField(label = 'Почта', validators=[DataRequired(), InputRequired(), Email("Некорректный email")])
   password = PasswordField(label = 'Пароль', validators=[DataRequired(),InputRequired(),  Length(min=4,max=100, message="Пароль должен быть от 4 до 100 символов")])
   remind_me=BooleanField(label = 'Запомнить меня',default=False)
   submit = SubmitField(label = 'Зайти')

class PostForm(FlaskForm):
   name = StringField('post_name', validators=[DataRequired(),InputRequired()])
   url = StringField('url', validators=[DataRequired(),InputRequired()])
   post = TextAreaField('post', validators=[DataRequired(),InputRequired()])
   submit = SubmitField('Отправить')