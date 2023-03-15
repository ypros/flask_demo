import mysql.connector
import uuid
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

mydb = mysql.connector.connect(
    user='root',
    password='password',
    host='127.0.0.1',
    database='flask')


 
#CREATE NEW USER IN USERS TABLE
def create_new_user(first_name, last_name, password, age, biography, city):
    user_id = str(uuid.uuid4())
    password_hash = generate_password_hash(password)
    print(password_hash)

    cursor = mydb.cursor()
    sql = "INSERT INTO users (id, first_name, last_name, password_hash, age, biography, city) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (user_id, first_name, last_name, password_hash, age, biography, city)

    cursor.execute(sql, val)
    mydb.commit()

    cursor.close()

    return user_id

#GET USER'S DATA FROM USERS TABLE BY ID
def get_user_info(user_id):
    cursor = mydb.cursor()
    sql = "SELECT id, first_name, last_name, age, biography, city FROM users WHERE id = %s"
    val = [(user_id)]

    cursor.execute(sql, val)

    result = None
    
    for (id, first_name, last_name, age, biography, city) in cursor:
        result = {
            "id": id,
            "first_name": first_name,
            "last_name": last_name,
            "age": age,
            "biography": biography,
            "city": city
        }

    cursor.close()



    return result

#GET USERS FROM USERS TABLE SEARCHING ON NAMES 
def search_user(first_name, last_name):

    cursor = mydb.cursor()
    sql = "SELECT id, first_name, last_name, age, biography, city FROM users WHERE first_name LIKE %s AND last_name LIKE %s ORDER BY id"
    val = (f"{first_name}%", f"{last_name}%")

    try:
        cursor.execute(sql, val)
    except mysql.connector.Error as err:
        return {'success': False, 'message': err.msg, 'payload': ""} 

    result = []
    
    for (id, first_name, last_name, age, biography, city) in cursor:
        result.append({
            "id": id,
            "first_name": first_name,
            "last_name": last_name,
            "age": age,
            "biography": biography,
            "city": city
        })

    cursor.close()

    return  {'success': True, 'message': "", 'payload': result}

def add_friend(user_id, friend_id):

    cursor = mydb.cursor()
    sql = "INSERT INTO friends (user, friend) VALUES (%s, %s)"
    val = (user_id, friend_id)

    try:
        cursor.execute(sql, val)
        mydb.commit()
    except mysql.connector.Error as err:
        return err.errno 

    cursor.close()

    return True

def get_feed(user_id):
    cursor = mydb.cursor()
    sql = """SELECT 
                p.id id,
                p.text text,
                p.author_user_id author_user_id
            from users u left join friends f on u.id  = f.user
            left join posts p on f.friend = p.author_user_id
            where u.id = %s
            order by p.created_at DESC limit 1000 offset 0"""
    val = [(user_id)]

    try:
        cursor.execute(sql, val)
    except mysql.connector.Error as err:
        return None

    result = []
    
    for (id, text, author_user_id) in cursor:
        result.append({
            "id": id,
            "text": text,
            "author_user_id": author_user_id
        })

    cursor.close()

    return result




#ADD USER'S POST IN POSTS
def add_post(user_id, text):
    post_id = str(uuid.uuid4())
    current_datetime = datetime.datetime.utcnow()

    cursor = mydb.cursor()
    sql = "INSERT INTO posts (id, author_user_id, text, created_at) VALUES (%s, %s, %s, %s)"
    val = (post_id, user_id, text, current_datetime)

    try:
        cursor.execute(sql, val)
        mydb.commit()
    except mysql.connector.Error as err:
        print(err.msg)
        return None 

    cursor.close()

    return post_id       


#VERIFY USER PASSWORS FOR AUTH
def verify_user(user_id, user_password):
    cursor = mydb.cursor()
    sql = "SELECT id, password_hash FROM users WHERE id = %s"
    val = [(user_id)]

    cursor.execute(sql, val)
    result = False

    for (id, password_hash) in cursor:
        if check_password_hash(password_hash, user_password):
            result = True
      

    cursor.close()

    return result



