from google.cloud import translate_v2 as translate, client
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_key.json"

def translate(text: str, lang: str) -> str:

    client = translate.Client()

    result = client.translate(text, target_language=lang)
    return result["translatedText"]

