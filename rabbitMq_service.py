import pika

class RabbitMqService:
    def escribir_mensaje(self,mensaje: str):
        try:
            # Establecer conexión con el servidor RabbitMQ
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            channel = connection.channel()

            # Declarar la cola en la que se escribirá el mensaje
            channel.queue_declare(queue='FailLoverStore', durable=True)

            # Publicar el mensaje en la cola
            channel.basic_publish(exchange='', routing_key='FailLoverStore', body=mensaje)

            # Cerrar la conexión
            connection.close()
            return f'Mensaje: {mensaje} enviado a RabbitMQ'
        except Exception as e:
            return f'No se pudo guardar el mensaje en RabbitMq: {e}'

    def leer_mensajes(self):
        # Lista de mensajes
        mensajes = []
        try:
            # Establecer conexión con el servidor RabbitMQ
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            channel = connection.channel()

            # Declarar la cola de la que se leerán los mensajes
            queue = channel.queue_declare(queue='FailLoverStore', durable=True)
                        
            if queue.method.message_count > 0:
                print(f"Hay {queue.method.message_count} mensajes en la cola.")
                # Leer los mensajes de la cola
                channel.basic_qos(prefetch_count=1)
                while True:
                    method_frame, header_frame, body = channel.basic_get(queue='FailLoverStore', auto_ack=True)

                    # Check if there are no more messages in the queue
                    if method_frame is None:
                        # print("No more messages in the queue.")
                        break

                    # Process the message (you can replace this with your own logic)
                    #print(f"Received message: {body}")
                    mensajes.append(body)
            else:
                return []
            # Cerrar la conexión
            connection.close()
        except Exception as e:
            print(f'No se pudo leer los mensaje de RabbitMq: {e}')
            return []
        return mensajes

