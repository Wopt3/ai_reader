import os
from google.cloud import texttospeech_v1beta1 as tts
from sqlalchemy.ext.asyncio import result

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_key.json"

def synthesize_page(text: str,
                    audio_path: str,)->list[dict]:
    client = tts.TextToSpeechClient()

    ssml_parts = ["<speak>"]
    words = text.split()
    for idx, word in enumerate(words):
        escaped_word = word.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        ssml_parts.append(f'<mark name="{idx}"/>{escaped_word} ')

    ssml_parts.append('</speak>')
    ssml_string = "".join(ssml_parts)

    synthesis_input = tts.SynthesisInput(ssml=ssml_string)

    voice = tts.VoiceSelectionParams(
        language_code="en-US",
        name = "en-US-Neural2-J"  # High-quality female studio voice
    )

    audio_config = tts.AudioConfig(
        audio_encoding=tts.AudioEncoding.MP3,
        speaking_rate=0.95,
        pitch=-1.2
    )

    request = tts.SynthesizeSpeechRequest(
        input = synthesis_input,
        voice = voice,
        audio_config = audio_config,
        enable_time_pointing=[tts.SynthesizeSpeechRequest.TimepointType.SSML_MARK]
    )

    response = client.synthesize_speech(request=request)

    with open(audio_path, "wb") as out:
        out.write(response.audio_content)

    timestamps = []
    for tp in response.timepoints:
        timestamps.append({"word_index": int(tp.mark_name),
                           "start_time": tp.time_seconds})
    return timestamps