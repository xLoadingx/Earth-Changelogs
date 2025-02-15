import json
import requests
from bs4 import BeautifulSoup
import openai
from datetime import datetime

# 1. Scrape latest headlines from BBC News
def get_latest_news():
    url = "https://www.bbc.com/news"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    headlines = [h3.get_text(strip=True) for h3 in soup.find_all("h3")[:5]]
    return headlines if headlines else ["🌍 No news found today."]

# 2. Generate JSON-formatted Patch Notes using OpenAI
def generate_patch_notes(news):
    system_prompt = "You are generating JSON-formatted video game-style changelogs based on real-world events."
    user_prompt = f"""
    Generate a patch note in **valid JSON format** with the following structure:

    {{
        "version": "Earth vYYYY.MM.DD",
        "date": "Month DD, YYYY",
        "notes": [
            "Note 1",
            "Note 2",
            "Note 3"
        ]
    }}

    Use these headlines: {news}
    Make the patch notes sound **fun and engaging**.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format="json"  # Ensure OpenAI returns proper JSON
    )

    return json.loads(response["choices"][0]["message"]["content"])  # Convert AI output to Python JSON object

# 3. Load existing patchnotes.json
try:
    with open("patchnotes.json", "r") as file:
        data = json.load(file)
except FileNotFoundError:
    data = {"patches": []}

# 4. Create a new patch
news_headlines = get_latest_news()
new_patch = generate_patch_notes(news_headlines)

# 5. Save to patchnotes.json
data["patches"].insert(0, new_patch)  # Insert latest patch at the top

with open("patchnotes.json", "w") as file:
    json.dump(data, file, indent=4)

print("🌍 New patch note added successfully!")
