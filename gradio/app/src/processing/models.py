import os

from sentence_transformers import SentenceTransformer
from transformers import BlipProcessor, BlipForConditionalGeneration

from app.config import MODEL_DIR


def get_models():
    # todo save into local and reload from it
    try:
        emb_model = SentenceTransformer(os.path.join(MODEL_DIR, 'gte-large-en-v1.5'), trust_remote_code=True)

    except:
        emb_model = SentenceTransformer('Alibaba-NLP/gte-large-en-v1.5', trust_remote_code=True)
        emb_model.save(os.path.join(MODEL_DIR, "gte-large-en-v1.5"))

    try:
        model = BlipForConditionalGeneration.from_pretrained(os.path.join(MODEL_DIR, "blip-image-captioning-large"), trust_remote_code=True)
    except:
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
        model.save_pretrained(os.path.join(MODEL_DIR, "blip-image-captioning-large"))


    try:
        tokenizer = BlipProcessor.tokenizer_class.from_pretrained(os.path.join(MODEL_DIR, "blip-image-captioning-large"))
        feature_extractor = BlipProcessor.feature_extractor_class.from_pretrained(os.path.join(MODEL_DIR, "blip-image-captioning-large"))
        processor = BlipProcessor(tokenizer=tokenizer, feature_extractor=feature_extractor)
    except:
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large", trust_remote_code=True)
        # processor.tokenizer.save_pretrained(os.path.join(MODEL_DIR, "blip-image-captioning-large"))
        # processor.feature_extractor.save_pretrained(os.path.join(MODEL_DIR, "blip-image-captioning-large"))
        # todo to fix

    return processor, model, emb_model