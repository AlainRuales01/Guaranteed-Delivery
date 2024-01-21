from kafka import KafkaProducer

class KafkaService:
    def enviar_mensaje_kafka(self, mensaje:str, topic:str):
        # Configurar el productor de Kafka
        producer = KafkaProducer(bootstrap_servers='localhost:9092')

        # Enviar el mensaje al topic especificado
        producer.send(topic, mensaje)

        # Esperar a que el mensaje se envíe correctamente
        producer.flush()

        # Cerrar la conexión con Kafka
        producer.close()

        return f'Mensaje {mensaje} enviado a Kafka a grupo {topic}'
    
    def validar_conexion_kafka(self):
        try:
            producer = KafkaProducer(bootstrap_servers='localhost:9092')
            producer.close()
            return True
        except Exception as e:
            print(f'No se pudo conectar con Kafka: {e}')
            return False