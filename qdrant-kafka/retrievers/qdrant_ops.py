import json
from qdrant_client import QdrantClient, models
# from utils.decorator_utils import execution_time_decorator
from fastembed import TextEmbedding


class HybridQdrantOperations:
    def __init__(self):
        self.embed_model = TextEmbedding(model_name='snowflake/snowflake-arctic-embed-s')
        self.client = QdrantClient(host="localhost", port=6333)
        self.collection_name = 'startups'
    def search(self, text: str,limit:int = 2):
        vector = next(self.embed_model.embed(documents=text)).tolist()
        search_result = self.client.query_points(
            collection_name=self.collection_name,
            query=vector,
            query_filter=None,  
            limit=limit
        ).points
        payloads = [hit.payload for hit in search_result]
        return payloads
    

# class NeuralSearcher:
#     def __init__(self,client, collection_name):
#         self.collection_name = collection_name
#         self.client = client
#         self.model = SentenceTransformer('bkai-foundation-models/vietnamese-bi-encoder',device = 'cuda')
#     def search(self, text: str,limit:int):
#         vector = self.model.encode(text).tolist()
#         search_result = self.client.query_points(
#             collection_name=self.collection_name,
#             query=vector,
#             query_filter=None,  
#             limit=limit
#         ).points
#         payloads = [hit.payload for hit in search_result]
#         return payloads