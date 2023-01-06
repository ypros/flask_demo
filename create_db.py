import mysql.connector
#mydb = mysql.connector.connect(user='root', password='password', host='127.0.0.1',port=5000,database='test',auth_plugin='mysql_native_password')
mydb = mysql.connector.connect(user='root', password='password', host='127.0.0.1', database='flask')



my_cursor = mydb.cursor()
try:
    my_cursor.execute("""

    DROP TABLE IF EXISTS flask.users;

    CREATE TABLE flask.users(
        id CHAR(36) NOT NULL PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        age INTEGER,
        biography TEXT,
        city VARCHAR(50),
        created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        password_hash VARCHAR(255) NOT NULL);
    """, multi=True)
except mysql.connector.Error as err:
    print(err.msg)
else:
    print("users table created")

my_cursor.close()
mydb.close()