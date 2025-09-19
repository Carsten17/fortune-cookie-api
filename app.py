from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import random

app = FastAPI(title="Fortune Cookie API", version="1.2.0")

# --------- Base routes ----------
@app.get("/")
def read_root():
    return {"message": "Hello, your API is running!"}

@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello, {name}! Welcome to your API."}

# --------- Fortune logic ----------
# 50+ fortunes touching topics people love on Twitter/Reddit
FORTUNES = [
    "Your Wi-Fi will reconnect right before the Zoom ends.",
    "A bug you fear is just a semicolon you missed.",
    "Ship today. Future-you will thank present-you.",
    "Beware of meetings disguised as 'quick syncs'.",
    "Your next idea is already in your drafts.",
    "The deploy will pass when someone is watching.",
    "Coffee is temporary; shipped code is forever.",
    "A stranger will star your repo at 3 AM.",
    "New opportunity: check your spam folder 👀",
    "Your keyboard knows the answer. Trust your fingers.",
    "Dark mode won’t fix your sleep schedule—but it helps.",
    "Your side project will outgrow your day job when you least expect it.",
    "The best A/B test is shipping it.",
    "Your {topic} hot take will go viral if you’re nice about it.",
    "A clean desk invites messy ideas. That’s good.",
    "Your TypeScript will compile on the first try today.",
    "Someone important is lurking your profile right now.",
    "A tiny feature will make a huge user happy.",
    "You’re one README away from more stars.",
    "Your tests will pass after you hydrate.",
    "The {topic} thread you’re avoiding is the one to write.",
    "Close 3 tabs, unlock 3 IQ points.",
    "Your next DM changes the trajectory.",
    "The algorithm secretly loves kindness (and consistency).",
    "Your morning walk is worth a new feature.",
    "Tweet it, then do the work. In that order.",
    "Your {topic} meme is funnier than you think.",
    "Documentation is a love letter to your future self.",
    "Ka-ching: your Stripe dashboard will blink this week.",
    "The best growth hack is a helpful product.",
    "You’ll find the bug in a log you didn’t read yet.",
    "Stop perfecting the logo. Ship the link.",
    "Your PR will get merged with a smiley comment.",
    "Today’s ‘no’ makes room for tomorrow’s ‘yes’.",
    "The right collaborator is two replies away.",
    "Your {topic} idea needs a 10-second demo, not a 10-page plan.",
    "Five lines of code will beat your 50-line anxiety.",
    "Your laptop battery lasts longer when you’re excited.",
    "Friday deploy? Bold. Monday you will still be fine.",
    "A quiet hour beats a noisy day.",
    "Your best insight is hiding in user #7’s feedback.",
    "Say 'no' to one thing; say 'yes' to momentum.",
    "Your Notion will never be perfect. That’s okay.",
    "The right emoji doubles engagement :)",
    "Start with ugly; end with shipped.",
    "Your next commit message will be poetry.",
    "You’re closer than you think—keep going.",
    "Touch grass; ship faster.",
    "Your {topic} post will help the exact person you wanted to meet.",
    "Refactor later; delight now.",
    "Your curiosity is the roadmap.",
    "An uncomfortable message will unlock a comfortable future.",
    "You’ll sleep better after clicking 'Publish'.",
    "Your API rate limit will hold—believe.",
    "Take the screenshot. Post the demo.",
    "Luck = shipped × shared.",
    "[{topic}] A boring solution will win hearts.",
    "Your next feature request is already in your inbox.",
    "The comment you’re afraid to write is the one they need.",
    "Build the tiny thing people use every day.",
    "Cold outreach works when it’s warm-hearted.",
    "Your roadmap is hiding in your support tickets.",
    "Write the docs as if your best friend will read them.",
    "Your {topic} side quest becomes the main story.",
    "Small audience, big impact.",
    "People love tidy URLs and tidy ideas.",
    "The first draft is allowed to be terrible.",
    "Caffeine helps; clarity helps more.",
]

# Where we send people (monetization funnel → your bot)
CTA_URL = "https://poe.com/Micro-API_Launchpad?utm_source=fortune_api&utm_medium=json&utm_campaign=demo"
CTA_SHORT = "Try our bot → https://poe.com/Micro-API_Launchpad"

# Accept topic for free & pro endpoints, so folks can niche the joke
class FortuneReq(BaseModel):
    name: Optional[str] = None
    vibe: Optional[str] = None     # 'funny', 'motivational', 'savage'
    topic: Optional[str] = None    # e.g., 'startups','ai','fitness','crypto','dating','remote work','gaming'

def tweak_by_vibe(text: str, vibe: Optional[str]) -> str:
    if not vibe:
        return text
    v = vibe.lower().strip()
    if v in {"savage", "roast"}:
        return text + " Also: your tabs… close a few."
    if v in {"motivational", "wholesome"}:
        return text + " Keep going—you’re closer than you think."
    if v in {"funny", "joke", "lol"}:
        return text + " P.S. hydrate before you debug."
    return text

def apply_topic(base: str, topic: Optional[str]) -> str:
    """Insert topic if placeholder is present, else prefix with [topic] sometimes."""
    if not topic:
        return base
    t = topic.strip()
    if "{topic}" in base:
        return base.replace("{topic}", t)
    if random.random() < 0.5:
        return f"[{t}] " + base
    return base

# --------- Free endpoint (public hook) ----------
@app.post("/fortune")
def fortune(req: FortuneReq):
    base = random.choice(FORTUNES)
    base = apply_topic(base, req.topic)
    if req.name:
        base = f"{req.name}, " + base[0].lower() + base[1:]
    base = tweak_by_vibe(base, req.vibe)
    return {
        "fortune": base,
        "cta_url": CTA_URL,
        "cta_short": CTA_SHORT,
        "powered_by": "Fortune Cookie API v1.2"
    }

# --------- Paid endpoint (Pro) ----------
API_KEYS = {"DEMO-KEY-123"}  # replace later

class ProReq(FortuneReq):
    count: int = 3  # up to 5

@app.post("/fortune/pro")
def fortune_pro(req: ProReq, api_key: Optional[str] = Header(None, alias="X-API-Key")):
    if not api_key or api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid or missing API key. Use header X-API-Key.")
    n = min(max(req.count, 1), 5)

    picks: List[str] = []
    for _ in range(n):
        base = random.choice(FORTUNES)
        base = apply_topic(base, req.topic)
        if req.name:
            base = f"{req.name}, " + base[0].lower() + base[1:]
        base = tweak_by_vibe(base, req.vibe)
        picks.append(base)

    return {
        "fortunes": picks,
        "plan": "pro",
        "note": "Pass X-API-Key header. Replace DEMO-KEY-123 with your real key when deploying.",
        "cta_url": CTA_URL,
        "cta_short": CTA_SHORT
    }
