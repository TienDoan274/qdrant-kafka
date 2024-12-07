from prometheus_client import Counter

# Counter metric: đếm số lần endpoint `/pairs` được gọi
GET_PAIRS_COUNT = Counter(
    "get_pairs_count", 
    "Number of times the /pairs endpoint is called"
)
