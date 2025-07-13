import os
from gtts import gTTS
from pydub import AudioSegment

output_dir = os.path.join(os.getcwd(), "output")
os.makedirs(output_dir, exist_ok=True)

question_audio = f"{output_dir}/voice.mp3"

def create_voice(question_data):
    silence = AudioSegment.silent(duration=800)  # 800ms pause

    parts = [silence]
    # 1. Question
    q_text = question_data['question']
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


if __name__ == "__main__":
    # Example usage
    example_question = {
        "question": "இந்தியாவின் தலைநகரம் எது?",
        "options": ["சென்னை", "மும்பை", "டெல்லி", "கொல்கத்தா"]
    }
    create_voice(example_question)
    print("Example voice generated.")