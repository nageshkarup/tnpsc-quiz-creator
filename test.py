from scripts.generate_image import create_image_styled
from scripts.generate_audio import create_voice
from scripts.generate_video import create_video

question_data = {
    "id": 11,
    "question": "இந்திய சுதந்திரப் போராட்டத்தின் போது, 'மகாத்மா' என்ற பட்டம் காந்திஜிக்கு யாரால் வழங்கப்பட்டது, மேலும் அதன் முக்கியத்துவம் என்னவாக இருந்தது?",
    "options": [
        "A. ரவீந்திரநாத் தாகூர், தேசத்தின் ஆன்மீகத் தலைவராக அங்கீகரிக்கப்பட்டது",
        "B. சுபாஷ் சந்திர போஸ், இந்தியாவின் தேசத் தந்தையாக அறிவிக்கப்பட்டது",
        "C. ஜவஹர்லால் நேரு, சுதந்திர இந்தியாவின் முதல் பிரதமராக பரிந்துரைக்கப்பட்டது",
        "D. சர்தார் வல்லபாய் படேல், இந்திய மாநிலங்களை ஒருங்கிணைத்ததற்காக கௌரவிக்கப்பட்டது"
    ]
}

if __name__ == "__main__":
    create_image_styled(question_data)
    create_voice(question_data)
    create_video()
    print("All media generated successfully.")

    