import os
import json
import requests
from datetime import date
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not set")

client = OpenAI(api_key=OPENAI_API_KEY)

# Create FastAPI app
app = FastAPI(title="Tech News Summarizer")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cache setup
CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)

HN_TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"


def get_cache_path():
    today = date.today().isoformat()
    return CACHE_DIR / f"summaries_{today}.json"


def load_cache():
    cache_path = get_cache_path()
    if cache_path.exists():
        with open(cache_path, "r") as f:
            return json.load(f)
    return None


def save_cache(data):
    # Delete any existing cache files
    for file in CACHE_DIR.glob("summaries_*.json"):
        file.unlink()

    # Save today's cache
    cache_path = get_cache_path()
    with open(cache_path, "w") as f:
        json.dump(data, f, indent=2)


def fetch_top_hn_stories(limit=5):
    ids = requests.get(HN_TOP_STORIES_URL).json()
    stories = []

    for story_id in ids:
        item = requests.get(HN_ITEM_URL.format(story_id)).json()
        if item and item.get("type") == "story" and item.get("url"):
            stories.append(item)
        if len(stories) == limit:
            break

    return stories


def summarize_article(title, text, url):
    prompt = f"""
Summarize the following tech news in 3 concise bullet points.
Focus on what happened and why it matters. Read from the URL given below.

Title: {title}

Content: {text}

URL: {url}

OUTPUT FORMAT:
- Bullet Point 1
- Bullet Point 2
- Bullet Point 3
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=120,
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()


@app.get("/news")
def get_news():
    # 1. Check cache
    cached = load_cache()
    if cached:
        return {
            "source": "Hacker News",
            "cached": True,
            "articles": cached,
        }

    # 2. Fetch fresh news
    try:
        stories = fetch_top_hn_stories(limit=5)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch news")
    
    summaries = []

    for story in stories:
        title = story.get("title", "")
        text = story.get("text") or title
        url = story.get("url")

        try:
            summary = summarize_article(title, text, url)
        except Exception:
            summary = "Summary unavailable."

        summaries.append(
            {
                "title": title,
                "summary": summary,
                "url": url,
            }
        )

    # 3. Save cache
    save_cache(summaries)

    return {
        "source": "Hacker News",
        "cached": False,
        "articles": summaries,
    }
