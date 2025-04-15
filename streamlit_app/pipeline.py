import os
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

from streamlit_app.data_prepration.enrich_data import enrich_dataset
from streamlit_app.data_prepration.clean_data import load_dataset,drop_irrelevant_columns,clean_dataset
from streamlit_app.data_prepration.qdrant import upload_to_qdrant
from streamlit_app.qdrant_client_instance import get_qdrant_client

# Constants
CLEANED_DATA_PATH = "cleaned_courses.csv"
EMBEDDINGS_PATH = "course_embeddings.npy"
METADATA_PATH = "course_metadata.csv"
MODEL_NAME = "all-MiniLM-L6-v2"

def prepare_or_load_data(input_file, output_file=CLEANED_DATA_PATH):
    # === STEP 1: Load or generate cleaned data ===
    if not os.path.exists(output_file):
        print("[Data Prep] Cleaned dataset not found. Running full pipeline...")
        df = load_dataset(input_file)
        df = drop_irrelevant_columns(df)
        df = clean_dataset(df)
        df = enrich_dataset(df)
        df.to_csv(output_file, index=False)
        print(f"[Data Prep] Cleaned dataset saved to '{output_file}'")
    else:
        print("[Data Prep] Cleaned dataset already exists. Loading...")
        df = pd.read_csv(output_file)

        # Remove malformed embeddings column if present
        if 'embeddings' in df.columns:
            print("[Data Prep] Removing malformed 'embeddings' column...")
            df = df.drop(columns=['embeddings'])
            df.to_csv(output_file, index=False)

    # === STEP 2: Generate or load embeddings ===
    if not os.path.exists(EMBEDDINGS_PATH):
        print("[Embeddings] Generating new embeddings...")
        model = SentenceTransformer(MODEL_NAME)
        df['embeddings'] = df['lemmatized_descriptions'].apply(
            lambda x: model.encode(x).astype(np.float32)
        )
        df = df[df['embeddings'].apply(lambda x: isinstance(x, np.ndarray) and x.ndim == 1)]
        embeddings_matrix = np.vstack(df['embeddings'].values)
        np.save(EMBEDDINGS_PATH, embeddings_matrix)
        print(f"[Embeddings] Saved to '{EMBEDDINGS_PATH}'")
    else:
        print("[Embeddings] Loading from file...")
        embeddings_matrix = np.load(EMBEDDINGS_PATH)

    print(f"[Embeddings] Matrix shape: {embeddings_matrix.shape}")
    print(f"[Embeddings] First vector type: {type(embeddings_matrix[0])}")

    # Optional: Verify embedding integrity
    for i, vec in enumerate(embeddings_matrix):
        if not isinstance(vec, np.ndarray) or vec.ndim != 1:
            raise ValueError(f"[Error] Malformed embedding at index {i}: {vec}")

    # === STEP 3: Extract or load metadata ===
    if not os.path.exists(METADATA_PATH):
        print("[Metadata] Extracting metadata...")
        metadata_df = df[['course_id', 'course_title', 'descriptions', 'level', 'subject', 'url', 'is_paid']]
        metadata_df.to_csv(METADATA_PATH, index=False)
        print(f"[Metadata] Saved to '{METADATA_PATH}'")
    else:
        print("[Metadata] Loading existing metadata...")
        metadata_df = pd.read_csv(METADATA_PATH)

    # === STEP 4: Upload to Qdrant ===
    print("[Qdrant] Uploading to vector database...")
    client = get_qdrant_client()
    upload_to_qdrant(client, metadata_df, embeddings_matrix)
    print("[Qdrant] Upload complete.")

    return df, embeddings_matrix
