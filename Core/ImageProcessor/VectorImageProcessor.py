def process_images():
    image_json = [
    {
        "image_url": "{url}/kk-reco-images/vecteezy_propeller-fan-turbine_24560488.png",
        "pilot_id": "001",
        "appliance_tags": "2,3"
    },
    {
        "image_url": "{url}/kk-reco-images/electric-vehicle-charging-station-png-1771356244.png",
        "pilot_id": "001",
        "appliance_tags": "2,3"
    },
    {
        "image_url": "{url}/kk-reco-images/Art-13-1-3806602751.png",
        "pilot_id": "001",
        "appliance_tags": "2,3"
    },
    {
        "image_url": "{url}/kk-reco-images/Water-Pump-Background-PNG-2635532705.png",
        "pilot_id": "001",
        "appliance_tags": "2,3"
    },
    {
        "image_url": "{url}/kk-reco-images/vecteezy_ac-unit-isolated-on-background-3d-rendering-illustration_48424659.png",
        "pilot_id": "001",
        "appliance_tags": "2,3"
    },
    {
        "image_url": "{url}/kk-reco-images/vecteezy_3d-render-desk-fan-front-view_11300040.png",
        "pilot_id": "001",
        "appliance_tags": "2,3"
    },
    {
        "image_url": "{url}/kk-reco-images/Adjusting-smart-thermostat-1444862177.jpg",
        "pilot_id": "001",
        "appliance_tags": "2,3"
    },
    {
        "image_url": "{url}/kk-reco-images/adjusting-thermostat-71667831.jpg",
        "pilot_id": "001",
        "appliance_tags": "2,3"
    },
    {
        "image_url": "{url}/kk-reco-images/thermostats-scaled-4282230112.jpg",
        "pilot_id": "001",
        "appliance_tags": "2,3"
    }
    ]

    ids = []
    embeddings = []
    metadatas = []

    print("\n🟡 Starting To Store Images To ChromaDB\n")
    
    for i, item in enumerate(image_json):
        image_embedding = get_clip_embedding(image_url=item[IMAGE_URL_KEY])

        ids.append(f"image_{i}")
        embeddings.append(image_embedding.tolist())
        metadata = {
            PILOT_ID_KEY: item[PILOT_ID_KEY],
            APPLIANCE_TAG_KEY: item[APPLIANCE_TAG_KEY],
            IMAGE_URL_KEY: item[IMAGE_URL_KEY]
        }
        metadatas.append(metadata)

    # Store in DB
    store_images_in_db(embeddings, ids, metadatas)
    store_images_in_pgvector(embeddings, ids, metadatas)
    print("\n🟢 Storing Images To ChromaDB Complete")