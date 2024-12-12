import os
from tqdm import tqdm
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from fastembed import TextEmbedding
from qdrant_client import QdrantClient, models
import json

def main():
    dimension_dict = {"snowflake/snowflake-arctic-embed-s": 384}
    collection_name: str = 'startups'
    embed_model_name: str = 'snowflake/snowflake-arctic-embed-s'
    embedding_model = TextEmbedding(model_name=embed_model_name)

    qdrant_client = QdrantClient('http://localhost:6333')

    if not qdrant_client.collection_exists(collection_name=collection_name):
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=dimension_dict.get(embed_model_name), distance=models.Distance.COSINE)
        )
    vectors = []
    payloads = []
    ids = []
    with open(file='data.json', mode='r') as file:
        data = json.load(file)
    for index, obj in enumerate(data):
        # Extract properties
        name: str = obj.get('name')
        images: str = obj.get('images')
        alt: str = obj.get('alt')
        description: str = obj.get('description')
        link: str = obj.get('link')
        city: str = obj.get('city')
        vector = next(embedding_model.embed(documents=description)).tolist()
        vectors.append(vector)
        ids.append(index+1)
        payloads.append({
            "name": name,
            "city": city,
            "description": description,
            "images": images,
            "url": link
        })
    qdrant_client.upload_collection(
        collection_name=collection_name,
        vectors=vectors,
        payload=payloads,
        ids=ids,  
    )
    
if __name__ == "__main__":
    main()