import os

if not os.environ.get("GITHUB_ACTIONS"):
    from dotenv import load_dotenv
    load_dotenv()

from db.db_utils import fetch_next_question, mark_used
from scripts.generate_image import create_image_styled
from scripts.generate_audio import create_voice
from scripts.generate_video import create_video
from scripts.youtube_uploader import upload_video

question_data = fetch_next_question()

if not question_data:
    print("📭 No unused questions left.")
    exit()

create_image_styled(question_data)
create_voice(question_data)
create_video()

mark_used(question_data["id"])

upload_video(
    filepath=os.path.join(os.getcwd(), "output", "short.mp4"),
    title = "TNPSC Group 4 | TNPSC Questions | நடப்பு நிகழ்வுகள் தமிழில் | TNPSC Shorts",
    description=(
        "TNPSC தேர்விற்கான தினசரி கேள்வி. பயிற்சி செய்ய மறக்காதீர்கள்!\n\n"
        "#TNPSC2025 #TNPSCGroup4 #Group4 #TNPSCQuiz #TNPSCShorts #TamilQuiz\n"
        "#TNPSCPreparation #TNPSCTamil #CurrentAffairsTamil #GKQuestions\n"
        "#TamilGK #DailyTNPSC #TamilShorts #GovernmentJobTamil #TNPSCQuestions"
    ),
    tags=[
        "TNPSC", "Group 4", "GK", "Tamil", "Shorts", "TNPSC Quiz", "TNPSC 2025", "நடப்புநிகழ்வுகள்",
        "Daily Quiz", "TNPSC Preparation", "TNPSC Tamil", "Current Affairs",
        "TNPSC Group 4 Questions", "TNPSC Shorts", "Tamil Quiz", 
        "TNPSC Current Affairs", "Tamil GK", "Current Affairs Tamil", "TNPSC Questions"
    ]
)


