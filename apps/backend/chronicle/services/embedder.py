from chronicle.clients.openai_client import get_openai_client

def generate_embeddings(texts: list[str], model: str = "text-embedding-3-small") -> list[list[float]]:
    openai_client = get_openai_client()
    
    embeddings = openai_client.embeddings.create(input=texts, model=model)

    embedding_list = []
    for embedding in embeddings.data:
        embedding_list.append(embedding.embedding)

    return embedding_list