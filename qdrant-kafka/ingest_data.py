from pymongo import MongoClient
from utils.app_utils import create_qdrant_collection
from fastembed import TextEmbedding
import json
import certifi
from pymongo.server_api import ServerApi
def main():
    collection_name: str = 'startups'
    embed_model_name: str = 'snowflake/snowflake-arctic-embed-s'

    # Ste 0: create qdrant_collection
    create_qdrant_collection(collection_name=collection_name, embed_model=embed_model_name)

    with open(file='data.json', mode='r') as file:
        data = json.load(file)

    # Step 1: Connect to MongoDB
    client = MongoClient("mongodb+srv://doannhattien4:tiendoan@cluster0.azzl0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

    # Step 2: Select Database
    db = client['startups']

    # Step 3: Select Collection
    collection = db['docs']

    for index, obj in enumerate(data):
        # Extract properties
        name: str = obj.get('name')
        images: str = obj.get('images')
        alt: str = obj.get('alt')
        description: str = obj.get('description')
        link: str = obj.get('link')
        city: str = obj.get('city')

        # Step 4: Create a Document to Insert
        embedding_model = TextEmbedding(model_name=embed_model_name)
        vector = next(embedding_model.embed(documents=description)).tolist()
        document = {
            "collection_name": collection_name,
            "id": index+1,
            "vector": vector,
            "payload": {
                "name": name,
                "city": city,
                "description": description,
                "images": images,
                "url": link
            }
        }

        # Step 5: Insert the Document into the Collection
        result = collection.insert_one(document)

        # Step 6: Print the Inserted Document's ID
        print("Inserted document ID:", result.inserted_id)
if __name__ == "__main__":
    main()
        