import mysql.connector
import csv
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
#mydb = mysql.connector.connect(user='root', password='password', host='127.0.0.1',port=5000,database='test',auth_plugin='mysql_native_password')
#mydb = mysql.connector.connect(user='root', password='password', host='127.0.0.1', database='flask')
mydb = mysql.connector.connect(user='root', password='password', host='localhost', port=33060, database='flask', auth_plugin='mysql_native_password')

count_users = 0

cursor = mydb.cursor()
password_hash = generate_password_hash("12345")
biography = ""
sql = "INSERT INTO users (id, first_name, last_name, password_hash, age, biography, city) VALUES (%s, %s, %s, %s, %s, %s, %s)"

#print(user_id, first_name, last_name, password_hash, age, biography, city)

with open('people.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        count_users += 1

        names = row['name'].split()
        first_name = names[0]
        last_name = names[1]
        city = row['city']
        age = int(int(row['age'])/3 + 15)
        
        user_id = str(uuid.uuid4())

        if count_users > 1000:
            break

        #
        val = (user_id, first_name, last_name, password_hash, age, biography, city)

        cursor.execute(sql, val)
        mydb.commit()
    
    cursor.close()
    mydb.close()

    
    print("DONE!!!!!!!")
#my_cursor.close()
