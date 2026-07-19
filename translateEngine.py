from google.cloud import translate_v2 as translate
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_key.json"

def translate_text(text: str, lang: str) -> str:
    try:
        client = translate.Client()
        result = client.translate(text, target_language=lang)
        return result["translatedText"]
    except Exception as e:
        print(f"Translation Error: {e}")
        # Return a user-friendly fallback text instead of throwing a server-crashing exception
        return f"{text} (Translation Unavailable)"


