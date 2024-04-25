import pika
import json
import sys

# Connect to RabbitMQ
try:
    rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
except:
    print("Producer couldn't connect to RabbitMQ")
    sys.exit(1)

channel = rabbitmq_connection.channel()

channel.queue_declare(queue='item_queue')
channel.queue_declare(queue='shipping_queue')
channel.queue_declare(queue='op_queue')

# Consumer four
# Read input data from JSON file
with open('input_data.json', 'r') as file:
    input_data = json.load(file)

# Consumer 2 
name_of_item = input_data["name_of_item"]
price_of_item = input_data["price_of_item"]

# Consumer 3
name = input_data["name"]
quantity = input_data["quantity"]

# Consumer 4
orders = input_data['orders']
n = input_data['n']

print(orders)

message_body_consumertwo = json.dumps({'name': name_of_item, 'price': price_of_item})

message_body_consumerthree = json.dumps({'name': name, 'quantity': quantity})

message_body_consumerfour = json.dumps({'n': n, 'orders': orders})

# Publish the message to the RabbitMQ queue
channel.basic_publish(exchange='',routing_key='item_queue', body=message_body_consumertwo)
channel.basic_publish(exchange='',routing_key='shipping_queue', body=message_body_consumerthree)
channel.basic_publish(exchange='', routing_key='op_queue', body=message_body_consumerfour)


print("Sent item data to RabbitMQ")

# Close the connection
rabbitmq_connection.close()
