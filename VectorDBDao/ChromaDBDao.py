def store_images_in_db(embeddings, ids, metadatas):
    print("\n🚧 Creating New Collection")
    collection.add(
        embeddings = embeddings,
        ids = ids,
        metadatas = metadatas
    )

"""
The vector DB uses the indexed metadata to quickly narrow down the set of documents.
Most vector DBs (including ChromaDB) use an inverted index or hash map for fast filtering
metadata is automatically indexed, when a filtering is used on metadata, it does not do a full db scan.

Under the Hood (ChromaDB specifically):
- Chroma automatically builds an index on all metadata fields as they are inserted.
- These indexes are optimized for exact-match filtering (e.g., ==, not full-text or fuzzy search).
- The performance is near constant time for most common filters.

When where clause is used, the results are first filtered by the where clause,
and the similarity search is done only on the filtered set.
The metadata filtering happens before the similarity search.
It reduces the search space, which improves performance and ensures relevance to your constraints.
"""

def fetch_results(embedding, n_results, pilot_id):
    results = collection.query(
        query_embeddings = [embedding.tolist()],
        n_results = n_results,
        include = ['distances', 'metadatas', 'documents', 'embeddings'],
        where={"pilot_id": pilot_id}
    )
    return results

def delete_images_based_on_id(ids):
    # Delete by ID
    collection.delete(ids=ids)

def delete_entire_collection(collection_name):
    client.delete_collection(collection_name)
    print(f"🚨 Deleted Collection : {collection_name}")