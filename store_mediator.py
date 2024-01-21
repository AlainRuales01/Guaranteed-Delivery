from kafka_service import KafkaService
from rabbitMq_service import RabbitMqService

topic = 'test'
kafka_instance = KafkaService()
rabbit_instance = RabbitMqService()
class StoreMediator:
    def enviar_mensaje(self, data):
        isConnected = kafka_instance.validar_conexion_kafka()

        if(isConnected == False):         
            mensaje_respuesta = rabbit_instance.escribir_mensaje(data)
            return mensaje_respuesta
        try:
            mensaje_respuesta = kafka_instance.enviar_mensaje_kafka(data, topic)
        except Exception as e:
            print(f'No se pudo enviar el mensaje a Kafka: {e}')
            mensaje_respuesta = rabbit_instance.escribir_mensaje(data)
        return mensaje_respuesta
    
    def enviar_mensajes_pendientes(self):
        isConnected = kafka_instance.validar_conexion_kafka()
        if(isConnected == False):
            return 'No esta disponible el servicio de Kafka'
    
        mensajes = rabbit_instance.leer_mensajes()
        if len(mensajes) == 0:
            return 'No hay mensajes pendientes'
        
        for mensaje in mensajes:
            mensaje_respuesta = self.enviar_mensaje(mensaje)
            print(mensaje_respuesta)

        return 'Mensajes procesados'
    