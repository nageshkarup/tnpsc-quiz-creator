import os
import random

if not os.environ.get("GITHUB_ACTIONS"):
    from dotenv import load_dotenv
    load_dotenv()

from db.db_utils import fetch_next_question
from scripts.generate_image import create_style_one, create_style_two, create_style_three, create_style_four, create_style_five, create_style_six
from scripts.generate_audio import generate_voice_google_tts
from scripts.generate_video import create_video

question_data = fetch_next_question()

if not question_data:
    print("📭 No unused questions left.")
    exit()

image_styles = [
    create_style_one,
    create_style_two,
    create_style_three,
    create_style_four,
    create_style_five,
    create_style_six
    ]

chosen_style = random.choice(image_styles)
chosen_style(question_data, name="question.png")
generate_voice_google_tts(question_data)
create_video()