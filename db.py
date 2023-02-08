import mysql.connector
import uuid
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

    mydb = mysql.connector.connect(
        user='root',
        password='password',
        host='127.0.0.1',
        database='flask')

    cursor = mydb.cursor()
    sql = "SELECT id, first_name, last_name, age, biography, city FROM users WHERE first_name LIKE %s AND last_name LIKE %s ORDER BY id"
    val = (f"{first_name}%", f"{last_name}%")

    cursor.execute(sql, val)

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
    mydb.close()

    return result

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



