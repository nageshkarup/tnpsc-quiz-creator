import os
import random

if not os.environ.get("GITHUB_ACTIONS"):
    from dotenv import load_dotenv
    load_dotenv()

from db.db_utils import fetch_next_question, mark_used
from scripts.generate_image import create_style_one, create_style_two, create_style_three, create_style_four, create_style_five, create_style_six
from scripts.generate_audio import generate_voice_google_tts
from scripts.generate_video import create_video
from scripts.youtube_uploader import upload_video
from scripts.youtube_suggestion import get_random_trending_suggestion, fetch_youtube_suggestions
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


trending = get_random_trending_suggestion()
title = "TNPSC Group 2/2A Questions | TNPSC Group 4 Questions"

if trending:
    title = f"{trending} | TNPSC Quizz Questions"

tags=[
        "TNPSC", "Group 4", "GK", "Tamil", "Shorts", "TNPSC Quiz", "TNPSC 2025", "நடப்புநிகழ்வுகள்",
        "TNPSC Group 4 Questions", "TNPSC Shorts", "Tamil Quiz", 
        "TNPSC Current Affairs", "Tamil GK", "Current Affairs Tamil", "TNPSC Questions"
    ]
trending = fetch_youtube_suggestions("TNPSC")
if trending:
    tags.extend(trending)

upload_video(
    filepath=os.path.join(os.getcwd(), "output", "short.mp4"),
    title = title,
    description=(
        "TNPSC தேர்விற்கான தினசரி கேள்வி. பயிற்சி செய்ய மறக்காதீர்கள்!\n\n tnpsc group 4 answer key 2025 tamil\n tnpsc answer key 2025"
        "#TNPSC2025 #TNPSCGroup4 #Group4 #TNPSCQuiz #TNPSCAnswerKey #TamilQuiz\n"
        "#TNPSCPreparation #TNPSCTamil #CurrentAffairsTamil #GKQuestions\n"
        "#TamilGK #DailyTNPSC #TamilShorts #GovernmentJobTamil #TNPSCQuestions"
    ),
    tags=tags
)


mark_used(question_data["id"])