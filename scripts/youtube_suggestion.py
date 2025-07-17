import requests
import random

def fetch_youtube_suggestions(query):
    url = "https://suggestqueries.google.com/complete/search"
    params = {
        "client": "firefox",
        "ds": "yt",
        "q": query
    }
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return response.json()[1]
        else:
            print("❌ Failed to fetch suggestions")
            return []
    except Exception as e:
        print(f"❌ Error fetching suggestions: {e}")
        return []

def get_random_trending_suggestion(query = 'tnpsc'):
    suggestions = fetch_youtube_suggestions(query)
    if not suggestions:
        return ""
    selected = [opt for opt in suggestions if len(opt) > 15 and len(opt.split(' ')) > 2]
    return random.choice(selected)

if __name__ == "__main__":
    # Example
    trending = get_random_trending_suggestion()
    print(trending)