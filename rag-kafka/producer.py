from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Gửi metadata file
metadata = {
    "file_name": "document.pdf",
    "file_size": "2MB",
    "user_id": "12345",
    "upload_date": "2024-12-05T12:00:00"
}
producer.send('file-uploaded', value=metadata)

producer.close()
