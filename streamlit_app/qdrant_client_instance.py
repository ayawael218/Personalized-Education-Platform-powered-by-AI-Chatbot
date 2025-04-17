# this file for creating a singleton instance of Qdrant client
from qdrant_client import QdrantClient

# Create a singleton instance for Qdrant client
_qdrant_client = None

def get_qdrant_client():
    global _qdrant_client
    if _qdrant_client is None:
        _qdrant_client = QdrantClient(path="qdrant_local")
    return _qdrant_client
