import psycopg2
from pgvector.psycopg2 import register_vector
import pandas as pd

# ---- Connection Setup ----

def get_pg_connection():
    conn = psycopg2.connect(
        dbname="reco_vectordb",
        user="kartik",       # Replace with actual username or use `import getpass; getpass.getuser()`
        password="",            # Fill in if needed
        host="localhost",
        port=5432
    )
    register_vector(conn)
    return conn

# ---- Table Creation ----

def create_pgvector_table():
    """
    Creates the reco_images table with vector support.
    """
    with get_pg_connection() as conn:
        with conn.cursor() as cur:
            # Step 1: Create the table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS reco_images (
                    id TEXT PRIMARY KEY,
                    pilot_id TEXT,
                    image_url TEXT,
                    appliance_tags TEXT,
                    embedding VECTOR(512)
                );
            """)

            
            # Step 2: Create the index for ANN search using ivfflat
            # ivfflat needs at least 1000 entries, else it will give error, so not creating index for now
            
            #cur.execute("""
            #    CREATE INDEX IF NOT EXISTS reco_images_embedding_idx
            #    ON reco_images
            #    USING ivfflat (embedding vector_l2_ops)
            #    WITH (lists = 100);
            #""")
            
            conn.commit()
    print("Table created in PGVector")

# ---- Insert Embeddings ----

def store_images_in_pgvector(embeddings, ids, metadatas):
    """
    Store image embeddings in pgvector-based PostgreSQL table.
    Args:
        embeddings (List[List[float]]): List of vector embeddings.
        ids (List[str]): List of unique string IDs.
        metadatas (List[Dict[str, str]]): Keys: 'pilot_id', 'appliance_tags', 'image_url'.
    """

    #Calling create first
    create_pgvector_table()
    
    with get_pg_connection() as conn:
        with conn.cursor() as cur:
            for i in range(len(ids)):
                cur.execute("""
                    INSERT INTO reco_images (id, pilot_id, appliance_tags, image_url, embedding)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING;
                """, (
                    ids[i],
                    metadatas[i].get("pilot_id"),
                    metadatas[i].get("appliance_tags"),
                    metadatas[i].get("image_url"),
                    embeddings[i]
                ))
            conn.commit()
    print("Stored Images in PGVector")

# ---- Vector Search ----

def fetch_results_from_pgvector(embedding, n_results, pilot_id):
    """
    Fetch top-n similar image embeddings from pgvector table.
    """
    with get_pg_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, pilot_id, appliance_tags, image_url,
                       embedding <-> %s AS distance
                FROM reco_images
                WHERE pilot_id = %s
                ORDER BY embedding <-> %s
                LIMIT %s
            """, (embedding, pilot_id, embedding, n_results))

            rows = cur.fetchall()
            results = []
            for row in rows:
                results.append({
                    "id": row[0],
                    "metadata": {
                        "pilot_id": row[1],
                        "appliance_tags": row[2],
                        "image_url": row[3]
                    },
                    "distance": row[4]
                })

            return results