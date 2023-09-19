import psycopg2
import uuid
import datetime
import mmh3

mydb = psycopg2.connect("dbname=postgres user=postgres password=pass host=localhost port=55432")


#SEND DIALOG
def send_dialog(from_user_id, to_user_id, text):
    
    partion_id = mmh3.hash(from_user_id, signed=False) + mmh3.hash(to_user_id, signed=False)

    dialog_id = str(uuid.uuid4())
    current_datetime = datetime.datetime.utcnow()

    cursor = mydb.cursor()
    sql = "INSERT INTO dialogs (id, partion_id, from_user_id, to_user_id, text) VALUES (%s, %s, %s, %s, %s)"
    val = (dialog_id, partion_id, from_user_id, to_user_id, text)

    try:
        cursor.execute(sql, val)
        mydb.commit()
    except psycopg2.Error as err:

        print(err)

        return None 

    cursor.close()

    return str(partion_id)


def list_dialog(from_user_id, to_user_id):
    
    partion_id = mmh3.hash(from_user_id, signed=False) + mmh3.hash(to_user_id, signed=False)
    
    cursor = mydb.cursor()
    sql = "SELECT id, partion_id, from_user_id, to_user_id, text, created_at FROM dialogs WHERE partion_id = %s and ((from_user_id =%s and to_user_id =%s) or (from_user_id =%s and to_user_id =%s)) order by created_at desc "
    val = (partion_id, from_user_id, to_user_id, to_user_id, from_user_id)

    cursor.execute(sql, val)

    result = []
    
    for (id, partion_id, from_user_id, to_user_id, text, created_at) in cursor:
        result.append({
            "from": from_user_id,
            "to": to_user_id,
            "text": text
        })

    
    cursor.close()

    return result




