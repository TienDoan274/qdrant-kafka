from retrievers.qdrant_ops import HybridQdrantOperations
search = HybridQdrantOperations()
print(search.hybrid_search(text='green'))