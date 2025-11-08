import os
import json
import asyncio
from typing import List
from fastapi import FastAPI, Body, HTTPException
import uvicorn
from openai import OpenAI
from datetime import datetime

# Initialize OpenAI client (v1.x.x)
client = OpenAI(
    api_key= os.environ.get("OPENAI_API_KEY")  # or your actual key string
)

app = FastAPI()

DATA_FILE = "data.json"

PROMPT_GENERATE_DRAFT = """
Please write a short social media post for LinkedIn summarizing the following article:

{article_text}
""".strip()

# Helper function to load JSON data
def load_data() -> List[dict]:
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Helper function to save JSON data
def save_data(data: List[dict]):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Asynchronous function that calls OpenAI to generate a post
async def generate_post(article_text: str, platform: str) -> str:
    prompt_template = f"""
Write a short post for {platform}, summarizing this article:
{article_text}
""".strip()
    chat_completion = await asyncio.to_thread(
        client.chat.completions.create,
        messages=[{"role": "user", "content": prompt_template}],
        model="gpt-5-mini",
    )
    return chat_completion.choices[0].message.content.strip()

@app.post("/generate-posts")
async def generate_posts(
    article_text: str = Body(...),
    num_posts: int = Body(3),
    platform: str = Body("LinkedIn")
):
    if num_posts > 5:
        raise HTTPException(
            status_code=400,
            detail="Cannot generate more than 5 posts at a time."
        )
    if len(article_text.strip()) < 20:
        raise HTTPException(
            status_code=400,
            detail="Article text is too short. Please provide at least 20 characters."
        )
    tasks = [asyncio.create_task(generate_post(article_text, platform)) for _ in range(num_posts)]
    drafts = await asyncio.gather(*tasks)

    data = load_data()
    new_entry = {
        "article_text": article_text,
        "drafts": drafts,
        "platform": platform,
        "created_at": datetime.now().isoformat()
    }
    data.append(new_entry)
    save_data(data)

    return {"platform": platform, "drafts": drafts, "created_at": new_entry["created_at"]}

@app.get("/posts")
def get_posts():
    return load_data()

@app.get("/summary")
def get_summary():
    data = load_data()
    total_articles = len(data)
    total_drafts = 0
    platform_count = {}
    for entry in data:
        drafts_count = len(entry.get("drafts", []))
        total_drafts += drafts_count
        platform_name = entry.get("platform", "Unknown")
        platform_count[platform_name] = platform_count.get(platform_name, 0) + 1
    return {
        "total_articles": total_articles,
        "total_drafts": total_drafts,
        "platform_count": platform_count
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
