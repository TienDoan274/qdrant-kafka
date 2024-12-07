from kafka import KafkaConsumer
import json
import psycopg2

# Kết nối PostgreSQL
conn = psycopg2.connect(database="file_storage", user="admin", password="password")
cur = conn.cursor()

consumer = KafkaConsumer(
    'file-uploaded',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:
    data = message.value
    print(f"Received: {data}")
    # Lưu metadata vào database
    cur.execute(
        "INSERT INTO files (file_name, file_size, user_id, upload_date) VALUES (%s, %s, %s, %s)",
        (data['file_name'], data['file_size'], data['user_id'], data['upload_date'])
    )
    conn.commit()
