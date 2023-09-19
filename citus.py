import psycopg2
import uuid
import datetime
import mmh3

#mydb = psycopg2.connect("dbname=postgres user=postgres password=pass host=localhost port=5432")


#SEND DIALOG
def send_dialog(from_user_id, to_user_id, text):
    
    partion_id = mmh3.hash(from_user_id, signed=False) + mmh3.hash(to_user_id, signed=False)

    print(partion_id)

#    dialog_id = str(uuid.uuid4())
#    current_datetime = datetime.datetime.utcnow()

#    cursor = mydb_write.cursor()
#    sql = "INSERT INTO dialogs (id, from_user_id, to_user_id, text, created_at) VALUES (%s, %s, %s, %s, %s)"
#    val = (dialog_id, from_user_id, to_user_id, text, current_datetime)

#    try:
#        cursor.execute(sql, val)
#        mydb_write.commit()
#    except psycopg2.Error as err:
#        return None 

#    cursor.close()

    return str(partion_id)






