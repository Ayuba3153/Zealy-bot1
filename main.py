import requests
import time
import hashlib
import os

# 🔹 CONFIG
URLS = [
    "https://zealy.io/c/syndicateapp/questboard/sprints",
    "https://zealy.io/cw/2up/questboard/sprints",
    "https://zealy.io/cw/ubuntuone/questboard/sprints",
    "https://zealy.io/cw/vantatemplecommunity/questboard/sprints",
    "https://zealy.io/cw/trustyfy/questboard/sprints"
]

# 🔹 Get Telegram Bot Token from Railway environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ✅ Telegram chat IDs
CHAT_IDS = ["7344418472", "6214087128", "7612005744", "7489135670"]

# 🔹 HEADERS for Zealy
headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9"
}

# 🔹 SEND MESSAGE TO TELEGRAM
def send(msg):
    for chat_id in CHAT_IDS:
        try:
            r = requests.get(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                params={"chat_id": chat_id, "text": msg},
                timeout=10
            )
            print(f"📩 Sent to {chat_id} | Status:", r.status_code)
        except Exception as e:
            print(f"❌ Telegram error for {chat_id}:", e)

# 🔹 GET WEBSITE HASH
def get_hash(url):
    try:
        r = requests.get(url, headers=headers, timeout=15)
        print(f"🌐 {url} status:", r.status_code)

        if r.status_code != 200:
            return None

        return hashlib.md5(r.text.encode()).hexdigest()

    except requests.exceptions.Timeout:
        print(f"⏰ Timeout while connecting to {url}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Website error for {url}:", e)
        return None

# 🔹 START
print("🚀 Starting Zealy Monitor...")

send("✅ Bot started and monitoring multiple Zealy pages")

# Store initial hashes
last_hashes = {}
for url in URLS:
    last_hashes[url] = get_hash(url)

# 🔹 LOOP
while True:
    for url in URLS:
        new_hash = get_hash(url)

        if new_hash and new_hash != last_hashes.get(url):
            send(f"🚨 Update detected!\n{url}\nTasks may be live NOW!")
            last_hashes[url] = new_hash

    time.sleep(5)  # adjust to 3-5 sec if you want faster alerts
