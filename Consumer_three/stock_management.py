import pika
import mysql.connector
import json
import time
import sys



mysql_connection = mysql.connector.connect(
    host='mysql',
    user='root',
    password='newyork1176',
    database='inventory',
    port=3306,
    autocommit = True
)
mysql_cursor = mysql_connection.cursor()

def callback(ch, method, properties, body):
    message_data = json.loads(body.decode())

    name = message_data['name']
    quantity = int(message_data['quantity'])

    mysql_cursor.execute("""SELECT item_id, quantity FROM stock NATURAL JOIN items WHERE items.name = %(name)s""", {'name': name})
    present_quantity = mysql_cursor.fetchall()
    i = present_quantity[0][0]
    q = int(present_quantity[0][1])
    n = q - quantity

    mysql_cursor.execute("""UPDATE stock SET quantity = %(new_quantity)s WHERE item_id=%(id)s""", {'id': i, 'new_quantity': n})
    mysql_cursor.execute("""SELECT stock_id from stock WHERE item_id=%(id)s AND quantity=%(new_quantity)s""", {'id': i, 'new_quantity': n})
    stock_id = mysql_cursor.fetchall()
    stock_id = stock_id[0][0]
    mysql_cursor.execute("""INSERT INTO stock_shipment (stock_id, item_id, quantity) 
                        VALUES (%(stock_id)s,%(id)s,%(new_quantity)s ) """, {'stock_id':stock_id,'id': i, 'new_quantity': n})
    mysql_connection.commit()
    time.sleep(15)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    ch.stop_consuming()

try:
    rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
except:
    print("Consumer 3 couldn't connect to RabbitMQ")
    sys.exit(1)

channel = rabbitmq_connection.channel()
channel.queue_declare(queue='shipping_queue')

messages_received = 0
channel.basic_consume(queue='shipping_queue', on_message_callback=callback)
print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
mysql_cursor.close()
mysql_connection.close()
rabbitmq_connection.close()