#!/bin/bash

# Wait for Kafka to start
sleep 5

# Create topics
kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 3 --topic file-uploaded
kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 3 --topic file-deleted
kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 3 --topic query-requests

echo "Topics created: file-uploaded, file-deleted, query-requests"
