import os
import random
import sys

if not os.environ.get("GITHUB_ACTIONS"):
    from dotenv import load_dotenv
    load_dotenv()

from db.db_utils import fetch_next_question, mark_used
from scripts.generate_image import (
    create_style_one, create_style_two, create_style_three,
    create_style_four, create_style_five, create_style_six
)
from scripts.generate_audio import generate_voice_google_tts
from scripts.generate_video import create_video
from scripts.youtube_uploader import upload_video
from scripts.youtube_suggestion import get_random_trending_suggestion, fetch_youtube_suggestions
from scripts.telegram_alert import send_telegram_alert 

try:
    question_data = fetch_next_question()

    if not question_data:
        print("📭 No unused questions left.")
        sys.exit(0)

    image_styles = [
        create_style_one, create_style_two, create_style_three,
        create_style_four, create_style_five, create_style_six
    ]

    chosen_style = random.choice(image_styles)
    chosen_style(question_data, name="question.png")

    generate_voice_google_tts(question_data)
    create_video()

    trending = get_random_trending_suggestion()
    title = "TNPSC Group 2/2A Questions | TNPSC Group 4 Questions"
    if trending:
        title = f"{trending} | TNPSC Quiz Questions"

    tags = [
        "TNPSC", "TNPSC Quiz", "நடப்புநிகழ்வுகள்",
        "TNPSC Group 4 Questions", "TNPSC Shorts", "Tamil Quiz", 
        "TNPSC Current Affairs", "Current Affairs Tamil"
    ]
    trending_tags = fetch_youtube_suggestions("TNPSC")
    if trending_tags:
        tags.extend(trending_tags)

    upload_video(
        filepath=os.path.join(os.getcwd(), "output", "short.mp4"),
        title=title,
        description=(
            "TNPSC தேர்விற்கான தினசரி கேள்வி. பயிற்சி செய்ய மறக்காதீர்கள்!\n\n"
            "tnpsc group 4 answer key 2025 tamil\nTNPSC Group 2/2A Syllabus Questions\n"
            "#shorts #viralshorts #GKTamilAcademy #TNPSCGroup4 #TNPSCQuiz\n"
            "#TNPSCPreparation #CurrentAffairsTamil\n"
            "#TamilGeneralKnowledge #DailyTNPSC"
        ),
        tags=tags
    )

    mark_used(question_data["id"])

except Exception as e:
    error_message = f"❌ *TNPSC Upload Failed*\n\n`{str(e)}`"
    print(error_message)
    send_telegram_alert(error_message)  # ✅ Notify failure
    sys.exit(1)
