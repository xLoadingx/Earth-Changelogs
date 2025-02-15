import json
import requests
import openai
from datetime import datetime

# 1. Fetch News from Bing Search API
def get_latest_news():
    api_key = "YOUR_BING_SEARCH_API_KEY"
    search_url = "https://api.bing.microsoft.com/v7.0/news/search"
    headers = {"Ocp-Apim-Subscription-Key": api_key}
    params = {"q": "world news", "count": 5, "sortBy": "Date"}

    response = requests.get(search_url, headers=headers, params=params)
    if response.status_code == 200:
        articles = response.json()["value"]
        return [article["name"] for article in articles]
    else:
        return ["🌍 Error fetching news."]

# 2. Generate Patch Notes using OpenAI
def generate_patch_notes(news):
    system_prompt = "You are generating fun, game-style changelogs based on real-world events."
    user_prompt = f"Create a game-style patch note update using these news topics: {news}. Make them sound like video game updates."
    
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo-preview",
        messages=[{"role": "system", "content": system_prompt},
                  {"role": "user", "content": user_prompt}]
    )

    return response["choices"][0]["message"]["content"].split("\n")

# 3. Load existing patchnotes.json
try:
    with open("patchnotes.json", "r") as file:
        data = json.load(file)
except FileNotFoundError:
    data = {"patches": []}

# 4. Create a new patch
news_headlines = get_latest_news()
patch_notes = generate_patch_notes(news_headlines)

new_patch = {
    "version": f"Earth v{datetime.now().strftime('%Y.%m.%d')}",
    "date": datetime.now().strftime("%B %d, %Y"),
    "notes": patch_notes
}

# 5. Save to patchnotes.json
data["patches"].insert(0, new_patch)

with open("patchnotes.json", "w") as file:
    json.dump(data, file, indent=4)

print("🌍 New patch note added successfully!")
