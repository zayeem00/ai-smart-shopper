# utils.py
import openai
from pinecone import Pinecone, ServerlessSpec
import pandas as pd
from typing import List

# Function to get embeddings from OpenAI's model
def get_embedding(text: str, openai_api_key: str, model: str = "text-embedding-ada-002") -> List[float]:
    """
    Get embeddings for a given text using OpenAI's model.

    Args:
    text (str): Text to be embedded.
    openai_api_key (str): OpenAI API key.
    model (str): Model to be used for embedding. Default is "text-embedding-ada-002".

    Returns:
    List[float]: Embedding vector.
    """
    openai.api_key = openai_api_key
    try:
        response = openai.Embedding.create(
            model=model,
            input=text
        )
        return response['data'][0]['embedding']
    except Exception as e:
        print(f"Error getting embedding: {e}")
        return []

# Function to process the uploaded CSV and store embeddings in Pinecone
def process_csv(file, openai_api_key: str, pinecone_api_key: str, pinecone_env: str) -> str:
    """
    Process the uploaded CSV file and store embeddings in Pinecone.

    Args:
    file: Uploaded CSV file.
    openai_api_key (str): OpenAI API key.
    pinecone_api_key (str): Pinecone API key.
    pinecone_env (str): Pinecone environment.

    Returns:
    str: Status message.
    """
    try:
        df = pd.read_csv(file.name)
        
        # Initialize Pinecone
        pc = Pinecone(api_key=pinecone_api_key)
        index_name = "product-recommendations"
        
        # Check if index exists
        if index_name not in pc.list_indexes().names():
            try:
                pc.create_index(
                    name=index_name,
                    dimension=1536,
                    spec=ServerlessSpec(cloud="aws", region=pinecone_env)
                )
            except Exception as e:
                print(f"Error creating Pinecone index: {e}")
                return "Failed to create Pinecone index."

        index = pc.Index(index_name)
        
        embeddings = []
        for i, row in df.iterrows():
            embedding = get_embedding(row['description'], openai_api_key)
            if embedding:
                embeddings.append((str(row['product_id']), embedding, {'product_name': row['product_name'], 'image_url': row['image_url']}))
        
        if embeddings:
            try:
                index.upsert(embeddings)
            except Exception as e:
                print(f"Error upserting embeddings to Pinecone: {e}")
                return "Failed to upsert embeddings."
        
        return "Product catalog processed and embeddings stored in Pinecone."
    except Exception as e:
        print(f"Error processing CSV file: {e}")
        return "Failed to process CSV file."
