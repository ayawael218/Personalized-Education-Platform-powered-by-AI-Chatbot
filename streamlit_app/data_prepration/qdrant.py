# This file is part of the Qdrant integration for the chatbot
import faiss
import numpy as np
import pandas as pd
from qdrant_client import models
from qdrant_client_instance import get_qdrant_client

# Upload embeddings and metadata to Qdrant local instance
def upload_to_qdrant(metadata_df, embeddings_matrix, collection_name="courses"):
    client = get_qdrant_client()  # Use the shared singleton client

    # Create the collection if it doesn't exist
    ensure_courses_collection(client, embeddings_matrix.shape[1], collection_name)

    print(f"Uploading to collection '{collection_name}'...")

    try:
        # Upload embeddings and metadata to Qdrant
        # Ensure metadata is a DataFrame emeddings_matrix is a numpy array
        for i, row in metadata_df.iterrows():
            vector = embeddings_matrix[i].tolist()
            # Ensure the vector is a list of floats
            if not isinstance(vector, list) or not all(isinstance(x, (float, np.floating)) for x in vector):
                raise ValueError(f"Invalid vector at index {i}: {vector}")
            # Ensure the rows has the required columns
            client.upsert(
                collection_name=collection_name,
                points=[
                    models.PointStruct(
                        id=int(row['course_id']),
                        vector=vector,
                        payload={
                            "title": str(row['course_title']),
                            "description": str(row['descriptions']),
                            "level": str(row['level']),
                            "subject": str(row['subject']),
                            "url": str(row['url'])
                        }
                    )
                ]
            )
    except Exception as e:
        print(f"Error uploading to Qdrant: {str(e)}")
    else:
        print("Embeddings and metadata uploaded to Qdrant.")


# Retrieve courses based on a pre-embedded query
def retrieve_courses(client, embedded_query, top_k=5, collection_name="courses"):
    # Ensure embedded_query is a list or numpy array
    if isinstance(embedded_query, np.ndarray):
        query_vector = embedded_query.tolist()
    elif isinstance(embedded_query, list):
        query_vector = embedded_query
    else:
        raise ValueError("embedded_query must be a list or numpy array")
    try:
        results = client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=top_k
        )
    except Exception as e:
        print(f"Error retrieving courses: {str(e)}")
        return []
    # Return the courses in a structured format
    return [
        {
            "id": hit.id,
            "title": hit.payload.get("title", ""),
            "description": hit.payload.get("description", ""),
            "level": hit.payload.get("level", ""),
            "subject": hit.payload.get("subject", ""),
            "url": hit.payload.get("url", "")
        }
        for hit in results
    ]


# Ensure 'courses' collection exists
def ensure_courses_collection(client, vector_size: int, collection_name="courses"):
    try:
        existing = [col.name for col in client.get_collections().collections]
        if collection_name not in existing:
            # if the collection does not exist , create it with the specified vector size  and distance metric
            # Qdrant supports cosine similarity for distance metric
            client.recreate_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=vector_size,
                    distance=models.Distance.COSINE
                )
            )
            print(f"[QDRANT] Created collection '{collection_name}' with vector size {vector_size}")
        else:
            print(f"[QDRANT] Collection '{collection_name}' already exists.")
    except Exception as e:
        print(f"Error ensuring collection exists: {str(e)}")
