import requests
import time
import hashlib
import logging
import random
from bs4 import BeautifulSoup

# =========================
# CONFIG
# =========================
URLS = [
    "https://zealy.io/cw/trustyfy/questboard/sprints",
    "https://zealy.io/cw/vemevmsc/questboard/sprints",
    "https://zealy.io/cw/vantatemplecommunity/questboard/sprints",
    "https://zealy.io/cw/syndicateapp/questboard/sprints"
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
            data = {"chat_id": chat_id, "text": msg}
            requests.post(url, data=data, timeout=10)
        except Exception as e:
            logging.error(f"Telegram error: {e}")

# =========================
# FETCH
# =========================
def fetch_tasks(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": url
        }

        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code != 200:
            logging.warning(f"Bad response {response.status_code} from {url}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")

        tasks = []

        for a in soup.find_all("a"):
            link = a.get("href")
            title = a.get_text(strip=True)

            if link and "/quests/" in link:
                full_link = "https://zealy.io" + link
                content = title + full_link
                task_hash = hashlib.md5(content.encode()).hexdigest()

                tasks.append({
                    "title": title,
                    "link": full_link,
                    "hash": task_hash
                })

        return tasks

    except Exception as e:
        logging.error(f"Fetch failed {url}: {e}")
        return []

# =========================
# MAIN LOOP
# =========================
def monitor():
    logging.info("🚀 Zealy HTML monitor started...")

    while True:
        try:
            for url in URLS:
                tasks = fetch_tasks(url)

                for task in tasks:
                    task_id = task["link"]

                    if task_id not in seen_tasks:
                        seen_tasks[task_id] = task["hash"]

                        msg = f"🔥 NEW TASK\n{task['title']}\n{task['link']}"
                        logging.info(msg)
                        send_telegram(msg)

                    elif seen_tasks[task_id] != task["hash"]:
                        seen_tasks[task_id] = task["hash"]

                        msg = f"⚡ UPDATED TASK\n{task['title']}\n{task['link']}"
                        logging.info(msg)
                        send_telegram(msg)

            delay = random.uniform(MIN_DELAY, MAX_DELAY)
            time.sleep(delay)

        except Exception as e:
            logging.error(f"Loop error: {e}")
            time.sleep(5)

# =========================
# RUN
# =========================
if __name__ == "__main__":
    while True:
        try:
            monitor()
        except Exception as e:
            logging.error(f"Critical crash: {e}")
            time.sleep(10)                    logging.info(msg)
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
            time.sleep(4)
