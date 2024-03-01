import uuid
from confluent_kafka import SerializingProducer
from config.settings import KAFKA_BOOTSTRAP_SERVER
import simplejson as json

class KafkaProducer:
    def __init__(self):
        self.producer = self._create_producer()

    def _create_producer(self):
        producer_conf = {
            'bootstrap.servers': KAFKA_BOOTSTRAP_SERVER,
            # 'key.serializer': 'org.apache.kafka.common.serialization.StringSerializer',
            # 'value.serializer': 'org.apache.kafka.common.serialization.StringSerializer'
        }
        return SerializingProducer(producer_conf)

    def publish(self, topic, data, topic_identifier):
        # Convert the UUID key to a string and encode it to bytes
        key_bytes = str(data['id']).encode('utf-8')

        # Serialize the data to a JSON string and encode it to bytes
        # Use the bytes-like objects for key and value
        value_bytes = json.dumps(data, default=self.json_serializer).encode('utf-8')
        
        # self.producer.produce(topic=topic, key=key_bytes, value=value_bytes, on_delivery=self.delivery_report)
        # Adjust the produce call to include the topic_identifier in the callback lambda
        self.producer.produce(topic=topic, key=key_bytes, value=value_bytes, on_delivery=lambda err, msg: self.delivery_report(err, msg, topic_identifier))
        self.producer.flush()



    def json_serializer(self, data):
        if isinstance(data, uuid.UUID):
            return str(data)
        raise TypeError(f"Object of Type {data.__class__.__name__} is not serializable")
    
    def delivery_report(self, err, msg, topic_identifier):
        if err is not None:
            print(f"Message delivery failed: {err}")
        else:
            # Updated message format for clarity
            print(f"Message[{msg.topic()}] delivered to topic '{topic_identifier}' [Partition {msg.partition()}]")
