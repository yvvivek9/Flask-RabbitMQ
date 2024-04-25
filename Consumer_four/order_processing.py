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
    print(message_data)


    # Extract name and price from the message
    n = int(message_data['n'])

    mysql_cursor.execute("""INSERT INTO orders (total_amount) VALUES (0)""")
    order_id = mysql_cursor.lastrowid
    print(order_id)

    for i in range(n):
        order = message_data['orders'][i]
        name = order['name']
        quantity = order['quantity']
        # print(name, quantity)

        mysql_cursor.execute("""SELECT item_id, price FROM items WHERE items.name = %(name)s""", {'name': name})
        present_quantity = mysql_cursor.fetchall()
        # if item not present, need to send to error queue and explain that the item needs to be added to table
        print(present_quantity)
        i = present_quantity[0][0]
        price = int(present_quantity[0][1])
        print(i)
        
        mysql_cursor.execute("""INSERT INTO order_items (order_id, item_id, quantity, price_per_item) 
                                VALUES (%(order_id)s, %(item_id)s, %(quantity)s, %(price)s)""", {'order_id': order_id, 'item_id':i, 'quantity': quantity, 'price': price})
        
        mysql_cursor.execute("""UPDATE orders SET total_amount = total_amount + %(price)s WHERE order_id = %(order_id)s""", {'price': price * quantity, 'order_id': order_id})

    time.sleep(10)

    ch.basic_ack(delivery_tag=method.delivery_tag)
    ch.stop_consuming()



try:
    rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
except:
    print("Consumer 4 couldn't connect to RabbitMQ")
    sys.exit(1)

channel = rabbitmq_connection.channel()
channel.queue_declare(queue='op_queue')

messages_received = 0
channel.basic_consume(queue='op_queue', on_message_callback=callback)
print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
mysql_cursor.close()
mysql_connection.close()
rabbitmq_connection.close()