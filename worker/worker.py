import pika, json, os, time
from ssh_router import get_int_data
from save_data import save_interface
RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST")
RABBITMQ_QUEUE = 'router_jobs'
def callback(ch, method, properties, body):
    print("you got mail", body.decode())

    message_data = json.loads(body.decode())
    ip = message_data.get('ip')
    username = message_data.get('username')
    password = message_data.get('password')
    int_data = get_int_data(ip, username, password)
    save_interface(ip, int_data)
    print("Done (;")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def listening():
    connect = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connect.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE)

    print("Waiting for Queue")

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback)
    channel.start_consuming()

if __name__ == "__main__":
    INTERVAL = 30.0
    next_run = time.monotonic()
    count = 0
    time.sleep(10)

    while True:
        now = time.time()
        now_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))
        ms = int((now % 1) * 1000)  
        now_str_with_ms = f"{now_str}.{ms:03d}"
        print(f"[{now_str_with_ms}] run #{count}")
        listening()
        count += 1
        next_run += INTERVAL
        time.sleep(max(0.0, next_run - time.monotonic()))
