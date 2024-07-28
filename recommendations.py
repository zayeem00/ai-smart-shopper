# recommendations.py
import openai
from typing import List, Tuple

from utils import get_embedding
from pinecone import Pinecone

# Function to recommend products
def recommend_products(query: str, openai_api_key: str, pinecone_api_key: str, pinecone_env: str, top_k: int = 10) -> List[Tuple[str, str]]:
    """
    Recommend products based on the user query.
    Args:
    query (str): User query.
    openai_api_key (str): OpenAI API key.
    pinecone_api_key (str): Pinecone API key.
    pinecone_env (str): Pinecone environment.
    top_k (int): Number of top recommendations to return. Default is 10.
    Returns:
    List[Tuple[str, str]]: List of recommended products with image URL and product name.
    """
    query_embedding = get_embedding(query, openai_api_key)
    
    if not query_embedding:
        return []

    try:
        # Initialize Pinecone
        pc = Pinecone(api_key=pinecone_api_key)
        index = pc.Index("product-recommendations")
        
        results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
        recommended_products = [(match['metadata']['image_url'], f"{match['metadata']['product_name']} (Score: {match['score']})") for match in results['matches']]
        return recommended_products
    except Exception as e:
        print(f"Error querying Pinecone: {e}")
        return []

# Function to generate contextual message
def generate_contextual_message(query: str, recommendations: List[Tuple[str, str]], openai_api_key: str, system_prompt: str) -> str:
    """
    Generate a contextual message based on the user query and recommendations.
    Args:
    query (str): User query.
    recommendations (List[Tuple[str, str]]): List of recommended products.
    openai_api_key (str): OpenAI API key.
    system_prompt (str): System prompt for the assistant.
    Returns:
    str: Generated contextual message.
    """
    openai.api_key = openai_api_key
    product_names = [rec[1] for rec in recommendations]
    prompt = f"User query: {query}\nRecommended products: {', '.join(product_names)}\n{system_prompt}"
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # or use "gpt-3.5-turbo" if preferred
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error generating contextual message: {e}")
        return "Failed to generate contextual message."
