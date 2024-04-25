import pika
import sys
import time
import os

def check_rabbitmq_health():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672))
        connection.close()
        return True
    except:
        return False

def main():
    retries = 5

    for _ in range(retries):
        if check_rabbitmq_health():
            print("RabbitMQ is up and running.")
            sys.exit(0)  # Exit with success status
        else:
            print("RabbitMQ is not reachable. Retrying in {} seconds...".format(5))
            time.sleep(5)

    print("RabbitMQ could not be reached after {} retries. Exiting.".format(retries))

    os.system("docker compose down")
    sys.exit(1)

if __name__ == "__main__":
    main()