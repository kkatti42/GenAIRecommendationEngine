import chromadb
from transformers import CLIPProcessor, CLIPModel
import torch
import numpy as np
from PIL import Image
import requests
from io import BytesIO


def runRecommendationEngine(run_mode: RunMode):
    print(f"\n\033[1m🛠️ RUNNING RECOMMENDATION ENGINE IN {run_mode.value} MODE 🔍\033[0m\n")
    if run_mode == RunMode.CHAIN:
        return runRecommendationEngineInChainMode()
    elif run_mode == RunMode.AGENT:
        return runRecommendationEngineInAgentMode()
    else:
        raise ValueError(f"Unsupported run mode: {run_mode}")

if __name__ == "__main__":

    # Load processor and model
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    
    client = chromadb.PersistentClient(path="./chroma_langchain_db")
    delete_entire_collection("recommendation_image_collection")

    """
    By default, ChromaDB uses cosine similarity for all queries.
    A distance of 0 = exact match, and distance closer to 1 = less similar

    To explicitly use other similarity ->
    collection = client.get_or_create_collection(
    name="recommendation_image_collection",
    metadata={"hnsw:space": "cosine"})

    Acceptable values ->
    "cosine" -> for cosine distance

    "l2" -> for Euclidean distance

    "ip" -> inner product (dot product)

    Even the ANN can be configured
    # Advanced: "faiss:index_type": "Flat", "IVF", etc. (if supported)
    
    """
    
    collection = client.get_or_create_collection("recommendation_image_collection",
    metadata={"hnsw:space": "cosine"})
    process_images()

    """
    To control the behaviour of the model we can pass various parameters to it.
    Ex - 
    1) temperature (not to be confused with weather temperature) controls the randomness/ creativity of response
    Value |	Behavior
    -----------------
    0     | Most deterministic, safest, same output for same input. Ideal for factual or reproducible answers.
    ~0.7  | Balanced creativity and coherence. Common default.
    1+    | More creative, diverse, but can be less accurate or coherent.


    2) top_p (float: 0 to 1) -> Controls nucleus sampling. Similar to temperature, but different mathematically. Lower values = more focused output.
    Use either temperature or top_p — not both unless you know what you're doing.

    3) max_tokens -> Limits the number of tokens (words/punctuation fragments) the response can have.

    4) frequency_penalty (float: -2 to 2) -> Positive: discourages repetition. Negative: encourages repetition.

    5) presence_penalty (float: -2 to 2) -> Positive: encourages introducing new topics.

    Example -> 

    llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    max_tokens=300,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    """
    # LLM
    llm = ChatOllama(model="llama3", temperature=0)
    
    run_mode = RunMode.CHAIN
    result = runRecommendationEngine(run_mode=run_mode)
    data = json.loads(result)
    recommended_images = fetch_image_for_reco(data["image_description"], target_tag="2", threshold=1, n_results=3, pilot_id="10057")

    # Extract image URLs
    image_urls = [item["metadata"]["image_url"] for item in recommended_images]
    # Add to original data
    data["image_urls"] = image_urls
    data.pop("image_description", None)
    # Print final JSON
    print("\n🧠 Recommendation Assistant Says:\n")
    print(json.dumps(data, indent=2))