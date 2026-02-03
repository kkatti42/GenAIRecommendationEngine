import numpy as np

def get_clip_embedding(text: str = None, image_url: str = None) -> np.ndarray:
    """
    Returns the CLIP embedding for either text or image.
    Provide only one of: text or image_path.
    """
    
    if text:
        print("🔄 Getting Embedding For Reco Text ..")
        
        inputs = processor(text=[text], return_tensors="pt", padding=True)
        with torch.no_grad():
            text_features = model.get_text_features(**inputs)
        # Normalize the embedding
        #CLIP returns raw features, and these can vary in magnitude. To make comparisons fair and consistent, they must be normalized.
        #Unnormalized vectors distort similarity, One long vector could be falsely seen as "similar" just because it has larger values.
        embedding = text_features / text_features.norm(p=2, dim=-1, keepdim=True)
    
    elif image_url:
        print("🔄 Getting Embedding For Images ..")
        
        # Fetch image from URL
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content)).convert("RGB")
        inputs = processor(images=image, return_tensors="pt")
        with torch.no_grad():
            image_features = model.get_image_features(**inputs)
        # Normalize the embedding
        embedding = image_features / image_features.norm(p=2, dim=-1, keepdim=True)
    
    return embedding.squeeze().cpu().numpy()