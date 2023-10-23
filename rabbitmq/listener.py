import asyncio
from aio_pika import connect, IncomingMessage
import json
import psycopg2
import uuid
import datetime



async def on_message(message: IncomingMessage):

    try:
        data_dict = json.loads(message.body.decode())
        user_id = data_dict.get('user_id')
        text = data_dict.get('text')
    except:
        return None

    mydb_write = psycopg2.connect("dbname=postgres user=postgres password=pass host=localhost port=5432")

    post_id = str(uuid.uuid4())
    current_datetime = datetime.datetime.utcnow()

    cursor = mydb_write.cursor()
    sql = "INSERT INTO posts (id, author_user_id, text, created_at) VALUES (%s, %s, %s, %s)"
    val = (post_id, user_id, text, current_datetime)

    try:
        cursor.execute(sql, val)
        mydb_write.commit()
    except psycopg2.Error as err:
        print(err.msg)
        return None 

    cursor.close()

    mydb_write.close()



async def main(loop):
    connection = await connect("amqp://guest:guest@localhost/", loop = loop)

    channel = await connection.channel()

    queue = await channel.declare_queue("flask-queue", durable = True)

    await queue.consume(on_message, no_ack = True)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main(loop))
    loop.run_forever()