import paho.mqtt.client as mqtt
import json

from alarmeitbl.myeventloop import Log

class GerenciadorEventos():
    """
    Classe utilizada para gerenciar conexão e mensagens
    de eventos com broker mqtt 
    """
    def __init__(self, mqtt_broker: str, mqtt_port: int, base_topic: str):
        def on_connect(client, userdata, flags, rc):
            Log.info("Connected with mqtt server. Result code "+str(rc))
        
        self.base_topic = base_topic
        self.client = mqtt.Client()
        self.client.on_connect = on_connect

        self.client.connect_async(host = mqtt_broker, port = mqtt_port)

        self.client.loop_start()
    
    def publish(self, topic: str, message: dict) -> bool:
        if self.client.is_connected():
            message_str = json.dumps(message)
            Log.info(f'Enviando mqtt. tópico: {topic}. mensagem: {message_str}')
            final_topic = f'{self.base_topic}/{topic}'
            info = self.client.publish(topic=final_topic, payload=message_str)
            return info.is_published()
        
        Log.warn('Não conectado ao servidor mqtt')
        return False