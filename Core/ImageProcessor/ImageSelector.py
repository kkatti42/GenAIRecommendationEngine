def fetch_image_for_reco(text, target_tag, threshold, n_results, pilot_id):
    print("🔍 Searching For Matching Images ..\n")
    
    embedding = get_clip_embedding(text=text)
    #results = fetch_results(embedding, n_results, pilot_id)

    results = fetch_results_from_pgvector(embedding, n_results, pilot_id)
    print(results)
    return results

    # Filter by distance first (to match structure)
    #filter_results_based_on_distance(results, threshold)

    # Then filter by appliance tag
    #final_results = filter_results_based_on_appliance_tag(results, target_tag)

    #print(final_results)
    #return final_results

def filter_results_based_on_distance(results, threshold):
    print("\n🧲 Filtering Images Based On Vector Distance")
    
    distances = results['distances'][0]
    ids = results['ids'][0]
    metadatas = results['metadatas'][0]
    documents = results['documents'][0]
    embeddings = results['embeddings'][0]

    valid_indices = [i for i, dist in enumerate(distances) if dist <= threshold]

    results['distances'][0] = [distances[i] for i in valid_indices]
    results['ids'][0] = [ids[i] for i in valid_indices]
    results['metadatas'][0] = [metadatas[i] for i in valid_indices]
    results['documents'][0] = [documents[i] for i in valid_indices]
    results['embeddings'][0] = [embeddings[i] for i in valid_indices]


def filter_results_based_on_appliance_tag(results, target_tag):
    print("\n🧲 Filtering Images Based On Appliance Tags")
    filtered = []

    for dist, id_, metadata, doc, embedding in zip(
        results['distances'][0],
        results['ids'][0],
        results['metadatas'][0],
        results['documents'][0],
        results['embeddings'][0]
    ):
        tags = metadata.get("appliance_tags", "")
        if target_tag in tags.split(","):
            filtered.append({
                "id": id_,
                "distance": dist,
                "metadata": metadata,
                "document": doc,
                "embedding": embedding
            })

    return filtered