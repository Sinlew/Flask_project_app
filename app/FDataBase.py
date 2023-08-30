import math, time, sqlite3, re
from flask import url_for


class FDataBase:
   def __init__(self, db):
      self.__db = db
      self.__cur = db.cursor()

   def getMenu(self):
      sql = '''SELECT * FROM mainmenu'''
      try:
         self.__cur.execute(sql)
         res = self.__cur.fetchall()
         if res: return res
      except:
         print("Ошибка чтения бд")
      return []

   def addPost(self, title, text, url):
      try:
         self.__cur.execute(f"SELECT COUNT() as 'count' FROM posts WHERE url LIKE '{url}'")
         res = self.__cur.fetchone()
         if res['count']>0:
            print("Статья с данным url уже существует")
            return false
         base = url_for('static', filename = 'images_htnl')
         text = re.sub(r"(?P<tag><img\s+[^>]*src=)(?P<quote>[\"'])(?P<url>.+?)(?P=quote)>","\\g<tag>"+ base + "/\\g<url>>", text )
            
         time_this = math.floor(time.time())
         self.__cur.execute("INSERT INTO posts VALUES(NULL,?,?,?,?)", (title,text,url,time_this))
         self.__db.commit()
      except sqlite3.Error as e:
         print("Ошибка добавления статьи"+str(e))
         return False
      
      return True

   def getPost(self, alias):
      try:
         self.__cur.execute(f"SELECT title, text FROM posts WHERE url LIKE '{alias}' LIMIT 1")
         res = self.__cur.fetchone()
         if res:
            return res
      except sqlite3.Error as e:
         print("Ошибка получения статьи"+str(e))

      return (False, False)

   def getPostsAnonce(self):
      try:
         self.__cur.execute(f"SELECT id, title, text, url FROM posts ORDER BY time DESC")
         res = self.__cur.fetchall()
         if res: return res
      except sqlite3.Error as e:
         print("Ошибка получения статей"+str(e))

      return []

   def addUser(self, name, email, number, hpas):
      try:
         self.__cur.execute(f"SELECT COUNT() as 'count' FROM users WHERE email LIKE '{email}'")
         res = self.__cur.fetchone()
         if res['count']>0:
            print("Данный email уже используется")
            return False

         self.__cur.execute(f"SELECT COUNT() as 'count' FROM users WHERE name LIKE '{name}'")
         res = self.__cur.fetchone()
         if res['count']>0:
            print("Данный username уже используется")
            return False
         
         tm = math.floor(time.time())
         self.__cur.execute("INSERT INTO users VALUES(NULL,?,?,?,?,NULL,?)",(name,email,number,hpas,tm))
         self.__db.commit()
      except sqlite3.Error as e:
         print("Ошибка добавления в бд")
         return False
      
      return True

   def getUser(self, user_id):
      try:
         self.__cur.execute(f'SELECT * FROM users WHERE id = {user_id} LIMIT 1')
         res = self.__cur.fetchone()
         if not res:
            print("Пользователь не найден")
            return False

         return res
      except sqlite3.Error as e:
         print("ошибка получения данный"+str(e))

      return false

   def getUserByEmail(self, email):
      try:
         self.__cur.execute(f"SELECT * FROM users WHERE email='{email}' LIMIT 1")
         res = self.__cur.fetchone()
         if not res:
            print("Пользователь не найден")
            return False
         
         return res
      except sqlite3.Error as e:
         print("Ошибка получения данных из бд"+str(e))

      return False 

   def updateUserAvatar(self, avatar, user_id):
      if not avatar:
         return False

      try:
         binary = sqlite3.Binary(avatar)
         self.__cur.execute(f"UPDATE users SET avatar = ? WHERE id=?",(binary,user_id))
         self.__db.commit()
      except sqlite3.Error as e:
         print("Ошибка обновления аватара в бд"+str(e))
         return False
      return True
   