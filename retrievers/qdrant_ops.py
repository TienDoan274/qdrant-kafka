import json
from qdrant_client import QdrantClient, models
from utils.decorator_utils import execution_time_decorator


class HybridQdrantOperations:
    def __init__(self):
        self.payload_path = "../data.json"
        self.collection_name = "startups"
        self.DENSE_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
        self.SPARSE_MODEL_NAME = "prithivida/Splade_PP_en_v1"
        # collect to our Qdrant Server
        self.client = QdrantClient(host="localhost", port=6333)
        self.client.set_model(self.DENSE_MODEL_NAME)
        # comment this line to use dense vectors only
        self.client.set_sparse_model(self.SPARSE_MODEL_NAME)
        self.metadata = []
        self.documents = []

    @execution_time_decorator
    def hybrid_search(self, text: str, top_k: int = 5):
        # self.client.query will have filters also if you want to do query on filter data.
        search_result = self.client.query(
            collection_name=self.collection_name,
            query_text=text,
            limit=top_k,  # 5 the closest results
        )
        # `search_result` contains found vector ids with similarity scores
        # along with the stored payload

        # Select and return metadata
        metadata = [hit.metadata for hit in search_result]
        return metadata
    

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