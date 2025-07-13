import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_youtube_service():
    creds = Credentials(
        token=None,
        refresh_token=os.getenv("YOUTUBE_REFRESH_TOKEN"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv("YOUTUBE_CLIENT_ID"),
        client_secret=os.getenv("YOUTUBE_CLIENT_SECRET"),
        scopes=SCOPES
    )
    creds.refresh(Request())
    return build("youtube", "v3", credentials=creds)

def upload_video(filepath, title, description, tags, privacy_status="public"):
    youtube = get_youtube_service()

    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "27" # Category ID for Education
        },
        "status": {
            "privacyStatus": privacy_status
        }
    }

    media = MediaFileUpload(filepath, mimetype="video/*", resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=request_body, media_body=media)

    print("Uploading video...")
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")

    print("✅ Upload complete. Video ID:", response["id"])
    return response["id"]


