import requests
import time
import hashlib
import logging
import random

# =========================
# CONFIG
# =========================
COMMUNITIES = [
    "syndicateapp",
    "trustyfy",
    "vemevmsc",
    "vantatemplecommunity"
]

MIN_DELAY = 4
MAX_DELAY = 7

BOT_TOKEN = "8737938934:AAFlrX49kVtPg6iPjwNDJQblzscO3zsz10E"

CHAT_IDS = [
    "7344418472",
    "6214087128",
    "7612005744",
    "7489135670"
]

# =========================
# LOGGING
# =========================
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

seen_tasks = {}

# =========================
# TELEGRAM
# =========================
def send_telegram(msg):
    for chat_id in CHAT_IDS:
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            data = {
                "chat_id": chat_id,
                "text": msg,
                "disable_web_page_preview": True
            }
            requests.post(url, data=data, timeout=10)
        except Exception as e:
            logging.error(f"Telegram error: {e}")

# =========================
# GRAPHQL FETCH (FIXED)
# =========================
def fetch_tasks(community):
    try:
        url = "https://graphql.zealy.io/graphql"

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
            "Origin": "https://zealy.io",
            "Referer": f"https://zealy.io/c/{community}/questboard",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9"
        }

        query = {
            "operationName": "GetCommunityQuests",
            "variables": {
                "communitySlug": community
            },
            "query": """
            query GetCommunityQuests($communitySlug: String!) {
              community(slug: $communitySlug) {
                quests {
                  id
                  title
                  slug
                  updatedAt
                }
              }
            }
            """
        }

        # small human-like delay
        time.sleep(random.uniform(1, 2))

        res = requests.post(url, json=query, headers=headers, timeout=15)

        if res.status_code == 403:
            logging.warning(f"⚠️ 403 blocked on {community}")
            return []

        res.raise_for_status()

        data = res.json()
        quests = data["data"]["community"]["quests"]

        results = []
        for q in quests:
            link = f"https://zealy.io/quests/{q['slug']}"
            content = q["title"] + q["updatedAt"]

            results.append({
                "id": q["id"],
                "title": q["title"],
                "link": link,
                "hash": hashlib.md5(content.encode()).hexdigest()
            })

        return results

    except Exception as e:
        logging.error(f"GraphQL error ({community}): {e}")
        return []

# =========================
# MAIN
# =========================
def monitor():
    global seen_tasks

    logging.info("🚀 GraphQL Zealy sniper started...")

    while True:
        for community in COMMUNITIES:
            tasks = fetch_tasks(community)

            for task in tasks:
                task_id = task["id"]

                if task_id not in seen_tasks:
                    seen_tasks[task_id] = task["hash"]

                    msg = f"🔥 NEW TASK\nCommunity: {community}\n{task['title']}\n{task['link']}"
                    logging.info(msg)
                    send_telegram(msg)

                elif seen_tasks[task_id] != task["hash"]:
                    seen_tasks[task_id] = task["hash"]

                    msg = f"⚡ UPDATED TASK\nCommunity: {community}\n{task['title']}\n{task['link']}"
                    logging.info(msg)
                    send_telegram(msg)

        time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))

# =========================
# RUN
# =========================
if __name__ == "__main__":
    while True:
        try:
            monitor()
        except Exception as e:
            logging.error(f"CRASH: {e}")
            time.sleep(3)
