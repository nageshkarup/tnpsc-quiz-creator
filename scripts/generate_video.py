import subprocess
import os
from pydub.utils import mediainfo

output_dir = os.path.join(os.getcwd(), "output")
os.makedirs(output_dir, exist_ok=True)


question_audio = f"{output_dir}/voice.mp3"
final_image = f"{output_dir}/question.png"
final_video = f"{output_dir}/short.mp4"

def get_duration(audio_path, original=False):
    info = mediainfo(audio_path)
    duration = float(info['duration'])
    if original:
        return duration  # Return original duration without adjustments
    # Adjust duration for Shorts
    duration = duration + 5.0
    return min(duration, 150.0) 


# 5. Create video using image + voice-over
def create_video():
    duration = get_duration(question_audio)
    cmd = [
        "ffmpeg",
        "-y",
        "-loop", "1",
        "-i", final_image,
        "-i", question_audio,
        "-filter:a", "atempo=1.1",  # Speed up audio
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-t", str(duration),
        "-shortest",
        final_video
    ]
    subprocess.run(cmd)
    video_duration = get_duration(final_video, original=True)  # Ensure video duration is correct
    print(f"✅ Video created ({video_duration:.1f}s):", final_video)


if __name__ == "__main__":
    # Example usage
    example_question = {
        "question": "இந்தியாவின் தலைநகரம் எது?",
        "options": ["சென்னை", "மும்பை", "டெல்லி", "கொல்கத்தா"]
    }
    create_video()
    