import json
import os
import re
from gtts import gTTS
from pydub import AudioSegment
from google.cloud import texttospeech
from google.oauth2 import service_account

output_dir = os.path.join(os.getcwd(), "output")
os.makedirs(output_dir, exist_ok=True)

question_audio = f"{output_dir}/voice.mp3"

def create_voice(question_data):
    silence = AudioSegment.silent(duration=800)  # 800ms pause

    parts = [silence]
    # 1. Question
    q_text = question_data['question']
    q_text = re.sub(r'_+', 'வெற்று இடம்', q_text)  # Replace underscores with "வெற்று இடம்"
    q_audio_path = "output/q.mp3"
    gTTS(text=q_text, lang='ta').save(q_audio_path)
    parts.append(AudioSegment.from_file(q_audio_path))
    parts.append(silence)
    
    # 2. Each Option
    for i, option in enumerate(question_data['options']):
        opt_path = f"output/opt_{i}.mp3"
        gTTS(text="Option "+option, lang='ta').save(opt_path)
        parts.append(AudioSegment.from_file(opt_path))
        parts.append(silence)
    final_text = "பதிலை கீழே கமெண்ட் பண்ணுங்க."
    cmt_path = f"{output_dir}/cmt.mp3"
    gTTS(text=final_text, lang='ta').save(cmt_path)
    parts.append(AudioSegment.from_file(cmt_path))
    # 3. Combine all parts
    final_audio = sum(parts, AudioSegment.silent(duration=0))
    final_audio.export(question_audio, format="mp3")

    print("✅ Voice with pauses saved:", question_audio)

def generate_voice_google_tts(question_data):

    service_account_info = json.loads(os.getenv('GOOGLE_TTS_SERVICE_ACCOUNT'))
    credentials = service_account.Credentials.from_service_account_info(service_account_info)
    client = texttospeech.TextToSpeechClient(credentials=credentials)

    question = question_data['question']
    question = re.sub(r'_+', 'வெற்று இடம்', question)  #
    
    text = f"{question}\n\n"
    for i, option in enumerate(question_data['options']):
        text += f"Option : {option}\n\n"
    text += "பதிலை கீழே கமெண்ட் செய்யவும்."

    text_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="ta-IN",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
        name="ta-IN-Wavenet-D",
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=1.0,
        pitch=0.0
    )
    response = client.synthesize_speech(
        input=text_input,
        voice=voice,
        audio_config=audio_config
    )
    os.makedirs("output", exist_ok=True)
    with open("output/voice.mp3", "wb") as out:
        out.write(response.audio_content)
        print("✅ Audio content written to file 'output/voice.mp3'")



if __name__ == "__main__":
    # Example usage
    question_data_13 = {
    "id": 13,
    "question": "இந்திய அரசியலமைப்பில் குறிப்பிடப்பட்டுள்ள அடிப்படை உரிமைகளில், 'கல்வி பெறும் உரிமை' எந்த சட்டத் திருத்தத்தின் மூலம் சேர்க்கப்பட்டது, மேலும் அதன் முக்கிய நோக்கம் என்ன?",
    "options": [
        "86வது சட்டத் திருத்தம், 6 முதல் 14 வயது வரையிலான குழந்தைகளுக்கு இலவச மற்றும் கட்டாயக் கல்வி வழங்குதல்",
        "42வது சட்டத் திருத்தம், அனைவருக்கும் சமமான கல்வி வாய்ப்புகளை உறுதி செய்தல்",
        "73வது சட்டத் திருத்தம், கிராமப்புற கல்வி மேம்பாட்டிற்காக நிதி ஒதுக்குதல்",
        "92வது சட்டத் திருத்தம், உயர்கல்வியில் இட ஒதுக்கீட்டை அமல்படுத்துதல்"
    ]
}

    create_voice(question_data_13)
    print("Example voice generated.")