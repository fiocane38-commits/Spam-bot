# multi_spam_free.py
# pip install playwright praw discord.py-self instagrapi requests
# playwright install chromium

print("=== 1. INIZIO SCRIPT ===")

import os
print("=== 2. import os ===")
import time
print("=== 3. import time ===")
import random
print("=== 4. import random ===")
import asyncio
print("=== 5. import asyncio ===")
import json
print("=== 6. import json ===")
import traceback
print("=== 7. import traceback ===")
import threading
print("=== 8. import threading ===")
from pathlib import Path
print("=== 9. import Path ===")
from playwright.sync_api import sync_playwright
print("=== 10. import sync_playwright ===")

# ============================================================
# CONFIGURAZIONE DA VARIABILI D'AMBIENTE (Render)
# ============================================================

DISCORD_CHANNEL_IDS_STR = os.environ.get("DISCORD_CHANNEL_IDS", "")
DISCORD_GUILD_IDS_STR = os.environ.get("DISCORD_GUILD_IDS", "")
DISCORD_USER_TOKEN = os.environ.get("DISCORD_USER_TOKEN", "")

IG_SESSIONID = os.environ.get("IG_SESSIONID", "")
IG_COOKIES_JSON = os.environ.get("IG_COOKIES", "")
IG_PROXY = os.environ.get("IG_PROXY", "")

FB_COOKIES = os.environ.get("FB_COOKIES", "")
REDDIT_COOKIES = os.environ.get("REDDIT_COOKIES", "")
TIKTOK_COOKIES = os.environ.get("TIKTOK_COOKIES", "")
X_COOKIES = os.environ.get("X_COOKIES", "")

print("=== 11. VARIABILI D'AMBIENTE LETTE ===")

# ============================================================
# CREAZIONE FILE COOKIE ALL'AVVIO
# ============================================================
def create_cookie_files():
    files_to_create = {
        "fb_cookies.txt": FB_COOKIES,
        "reddit_cookies.txt": REDDIT_COOKIES,
        "tiktok_cookies.txt": TIKTOK_COOKIES,
        "x_cookies.json": X_COOKIES,
    }
    for filename, content in files_to_create.items():
        if content and content.strip():
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"[Setup] Creato file: {filename}")
            except Exception as e:
                print(f"[Setup] Errore creazione {filename}: {e}")
        else:
            print(f"[Setup] ATTENZIONE: {filename} è vuoto o mancante.")

print("=== 12. AVVIO create_cookie_files ===")
create_cookie_files()
print("=== 13. SETUP COMPLETATO ===")

# Configurazione Discord
DISCORD_CHANNEL_IDS = []
if DISCORD_CHANNEL_IDS_STR:
    DISCORD_CHANNEL_IDS = [int(x.strip()) for x in DISCORD_CHANNEL_IDS_STR.split(",") if x.strip()]

DISCORD_GUILD_IDS = []
if DISCORD_GUILD_IDS_STR:
    DISCORD_GUILD_IDS = [int(x.strip()) for x in DISCORD_GUILD_IDS_STR.split(",") if x.strip()]

print("=== 14. CONFIGURAZIONE DISCORD COMPLETATA ===")

# ============================================================
# CONFIG COMUNE
# ============================================================
PROMO_TEXT = """😈💥Jailbreak Any AI Models💥😈
jailbreak AI (Chatgpt,Claude,DeepSeek,Grok,Gemini ecc)
Growing community jailbreak site, discussions about jailbreaking AI of all types, I have a Telegram bot without AI xensure and an Osint bot. Here's the link to my Discord and Telegram bots.

Telegram Bot IA Uncensored:
https://t.me/Zerofilterr_bot?start=_tgr_ugpjer4yNTc8
Bot Osint:
https://t.me/Zeroshadebot?start=_tgr_XRokO3diMDNk

Community Telegram:
https://t.me/Zerofilter_ai

Community Reddit:
https://www.reddit.com/r/hackrebelscommunity/s/F5aR7jcwhn

Community Discord:
https://discord.gg/9XRXkWpptS"""

PROMO_MEMECOIN = """Memecoin season doesn't wait ⚡
Fill form → pay → token ready. That easy.
https://launchcoinn.it  💎"""

MESSAGES = [
    PROMO_TEXT.strip(),
    PROMO_MEMECOIN.strip(),
    PROMO_TEXT.strip() + "\n\n" + PROMO_MEMECOIN.strip(),
]

MESSAGES_X = [PROMO_MEMECOIN.strip()]

# ============================================================
# POOL FOLLOW RANDOM
# ============================================================
X_FOLLOW_POOL = ["elonmusk", "nvidia", "openai", "github", "microsoft", "google", "meta", "apple", "tesla", "spacex", "nasa", "vercel", "docker", "huggingface", "solana", "bitcoin", "ethereum", "binance", "coinbase", "kraken"]
IG_FOLLOW_POOL = ["instagram", "natgeo", "nasa", "nike", "adidas", "teslamotors", "spacex", "openai", "google", "meta", "solana", "binance", "coinbase", "apple", "microsoft"]
TT_FOLLOW_POOL = ["tiktok", "charlidamelio", "khaby.lame", "mrbeast", "nasa", "nike", "adidas", "spacex", "google", "microsoft"]
REDDIT_SUB_POOL = ["test", "python", "technology", "cryptocurrency", "solana", "CryptoCurrency", "SatoshiStreetBets", "ethtrader"]
FB_FOLLOW_POOL = ["zuck", "meta", "instagram", "nasa", "natgeo", "Nike", "adidas", "spacex", "tesla", "Microsoft"]

# ============================================================
# ARGOMENTI ANTI-RAM PER CHROMIUM
# ============================================================
CHROMIUM_ARGS = [
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-gpu",
    "--single-process",
    "--no-zygote",
    "--disable-accelerated-2d-canvas",
    "--disable-software-rasterizer",
    "--disable-extensions",
    "--disable-background-networking",
    "--disable-sync",
    "--disable-default-apps",
    "--mute-audio",
    "--no-first-run",
    "--disable-blink-features=AutomationControlled",
]

# ============================================================
# HELPER COOKIE
# ============================================================
def _load_netscape_cookies(path, domain_substr):
    cookies = []
    p = Path(path)
    if not p.exists():
        return cookies
    try:
        with open(p, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split("\t")
                if len(parts) < 7:
                    continue
                domain, flag, path_c, secure, expires, name, value = parts[:7]
                c = {"name": name, "value": value, "domain": domain, "path": path_c, "secure": secure.upper() == "TRUE"}
                try:
                    c["expires"] = int(expires)
                except Exception:
                    pass
                if any(d in domain for d in domain_substr):
                    cookies.append(c)
    except Exception as e:
        print(f"[Cookie] Errore lettura {path}: {e}")
    return cookies

def _load_json_cookies(path, domain_substr):
    cookies = []
    p = Path(path)
    if not p.exists():
        return cookies
    try:
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                for c in data:
                    domain = c.get("domain", "")
                    if any(d in domain for d in domain_substr):
                        cookie = {"name": c.get("name"), "value": c.get("value"), "domain": domain, "path": c.get("path", "/"), "secure": c.get("secure", False)}
                        if "expirationDate" in c:
                            cookie["expires"] = int(c["expirationDate"])
                        cookies.append(cookie)
    except Exception as e:
        print(f"[Cookie] Errore parsing JSON {path}: {e}")
    return cookies

# ============================================================
# WRAPPER PER THREAD
# ============================================================
def run_spam_in_thread(func, *args, **kwargs):
    def target():
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(f"[Thread] Errore in {func.__name__}: {e}")
            traceback.print_exc()

    t = threading.Thread(target=target)
    t.start()
    t.join(timeout=180)
    if t.is_alive():
        print(f"[Thread] Timeout per {func.__name__} (180s)")

# ============================================================
# X
# ============================================================
def spam_x_free(count=1, delay_min=90, delay_max=180):
    print("[X] inizio...")
    try:
        x_cookies = _load_json_cookies("x_cookies.json", ["x.com", "twitter.com"])
        if not x_cookies:
            print("[X] Nessun cookie X valido. Salto.")
            return
        print(f"[X] caricati {len(x_cookies)} cookies")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=CHROMIUM_ARGS)
            context = browser.new_context(
                viewport={"width": 1280, "height": 900},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            )
            context.add_cookies(x_cookies)
            page = context.new_page()

            print("[X] Navigazione a x.com/home...")
            try:
                page.goto("https://x.com/home", timeout=60000, wait_until="domcontentloaded")
            except Exception as e:
                print(f"[X] Timeout su /home: {e}")
                try:
                    browser.close()
                except Exception:
                    pass
                return
            time.sleep(8)

            if "login" in page.url.lower() or "i/flow/login" in page.url:
                print("[X] non loggato - cookies scaduti")
                try:
                    browser.close()
                except Exception:
                    pass
                return

            print("[X] loggato correttamente")

            for i in range(count):
                msg = random.choice(MESSAGES_X).strip()[:280]
                try:
                    print(f"[X] Navigazione a /compose/post (tentativo {i+1})...")
                    try:
                        page.goto("https://x.com/compose/post", timeout=60000, wait_until="domcontentloaded")
                    except Exception as e:
                        print(f"[X] Timeout su /compose/post: {e}")
                        continue

                    time.sleep(6)

                    for _ in range(3):
                        try:
                            page.keyboard.press("Escape")
                            time.sleep(0.3)
                        except Exception:
                            pass

                    box = None
                    for sel in [
                        'div[data-testid="tweetTextarea_0"]',
                        'div[role="textbox"]',
                        'div[contenteditable="true"]',
                    ]:
                        try:
                            loc = page.locator(sel).first
                            if loc.count() > 0:
                                loc.wait_for(state="visible", timeout=8000)
                                box = loc
                                print(f"[X] Selettore trovato: {sel}")
                                break
                        except Exception:
                            continue

                    if box is None:
                        print("[X] Nessun selettore trovato. Salto post.")
                        continue

                    box.click(timeout=8000)
                    time.sleep(1)
                    page.keyboard.press("Control+A")
                    page.keyboard.press("Backspace")
                    time.sleep(0.5)
                    page.keyboard.type(msg, delay=50)
                    time.sleep(2)

                    btn = None
                    for sel in [
                        'button[data-testid="tweetButtonInline"]',
                        'button[data-testid="tweetButton"]',
                        'button:has-text("Post")',
                    ]:
                        try:
                            loc = page.locator(sel).first
                            if loc.count() > 0:
                                btn = loc
                                break
                        except Exception:
                            continue

                    if btn is None:
                        page.keyboard.press("Control+Enter")
                        print("[X] Fallback Ctrl+Enter")
                    else:
                        enabled = False
                        for _ in range(10):
                            try:
                                dis = btn.get_attribute("aria-disabled")
                                if dis in (None, "false"):
                                    enabled = True
                                    break
                            except Exception:
                                pass
                            time.sleep(1)
                        if enabled:
                            btn.click(timeout=8000)
                            print("[X] Click Post")
                        else:
                            page.keyboard.press("Control+Enter")

                    time.sleep(5)
                    print(f"[X] {i+1}/{count} ok")
                except Exception as e:
                    print(f"[X] errore post: {e}")
                time.sleep(random.uniform(delay_min, delay_max))
            print("[X] Chiudo browser...")
            try:
                browser.close()
                print("[X] Browser chiuso")
            except Exception as e:
                print(f"[X] Errore chiusura browser: {e}")
        print("[X] finito")
    except Exception as e:
        print(f"[X] ERRORE GENERALE: {e}")
        traceback.print_exc()

def follow_x_random(count=3, delay_min=40, delay_max=90):
    print("[X Follow random] inizio...")
    try:
        x_cookies = _load_json_cookies("x_cookies.json", ["x.com", "twitter.com"])
        if not x_cookies:
            print("[X Follow random] manca x_cookies.json valido. Salto.")
            return
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=CHROMIUM_ARGS)
            context = browser.new_context()
            context.add_cookies(x_cookies)
            page = context.new_page()
            page.goto("https://x.com/i/connect_people", timeout=60000)
            time.sleep(5)
            page.keyboard.press("Escape")
            clicked = 0
            buttons = page.query_selector_all('button[data-testid*="follow"]')
            random.shuffle(buttons)
            for btn in buttons:
                if clicked >= count:
                    break
                try:
                    txt = (btn.inner_text() or "").lower()
                    if any(x in txt for x in ("following", "pending", "unfollow")):
                        continue
                    btn.click(timeout=4000)
                    clicked += 1
                    print(f"[X Follow random] follow #{clicked}")
                    time.sleep(random.uniform(delay_min, delay_max))
                except Exception:
                    pass
            print("[X Follow random] Chiudo browser...")
            try:
                browser.close()
            except Exception as e:
                print(f"[X Follow random] Errore chiusura browser: {e}")
        print(f"[X Follow random] finito ({clicked})")
    except Exception as e:
        print(f"[X Follow random] ERRORE: {e}")
        traceback.print_exc()

# ============================================================
# INSTAGRAM
# ============================================================
def spam_instagram(count=1, delay=600):
    print("[Instagram] inizio...")
    try:
        from instagrapi import Client
    except ImportError:
        print("[Instagram] instagrapi non installato. Salto.")
        return

    if not IG_SESSIONID:
        print("[Instagram] IG_SESSIONID non impostato. Salto.")
        return

    try:
        cl = Client()
        try:
            cl.set_app("448.0.0.0.20")
        except Exception:
            pass

        if IG_PROXY:
            try:
                cl.set_proxy(IG_PROXY)
                print(f"[Instagram] Proxy impostato")
            except Exception as e:
                print(f"[Instagram] Errore proxy: {e}")

        if IG_COOKIES_JSON:
            try:
                cookies_list = json.loads(IG_COOKIES_JSON)
                cookie_dict = {}
                for c in cookies_list:
                    if "instagram.com" in c.get("domain", ""):
                        cookie_dict[c["name"]] = c["value"]
                if cookie_dict:
                    cl.set_cookies(cookie_dict)
                    print("[Instagram] Cookie esportati caricati")
            except Exception as e:
                print(f"[Instagram] Errore parsing IG_COOKIES: {e}")

        try:
            cl.login_by_sessionid(IG_SESSIONID)
            print("[Instagram] login ok")
            cl.dump_settings("ig_session.json")
        except Exception as e:
            print(f"[Instagram] login fallito: {e}")
            print("[Instagram] Salto questo ciclo.")
            return

        for i in range(count):
            try:
                if not Path("promo.jpg").exists():
                    print("[Instagram] manca promo.jpg. Salto post.")
                    break
                media = cl.photo_upload(path="promo.jpg", caption=random.choice(MESSAGES))
                print(f"[Instagram] postato → {media.code}")
            except Exception as e:
                print(f"[Instagram] errore post: {e}")
            time.sleep(delay)
        print("[Instagram] finito")
    except Exception as e:
        print(f"[Instagram] ERRORE GENERALE: {e}")
        traceback.print_exc()


def follow_instagram_random(count=5, delay_min=40, delay_max=90):
    print("[IG Follow random] inizio...")
    try:
        from instagrapi import Client
    except ImportError:
        print("[IG Follow random] instagrapi non installato. Salto.")
        return

    if not IG_SESSIONID:
        print("[IG Follow random] IG_SESSIONID non impostato. Salto.")
        return

    try:
        cl = Client()
        try:
            cl.set_app("448.0.0.0.20")
        except Exception:
            pass

        if IG_PROXY:
            try:
                cl.set_proxy(IG_PROXY)
            except Exception:
                pass

        try:
            if Path("ig_session.json").exists():
                cl.load_settings("ig_session.json")
            cl.login_by_sessionid(IG_SESSIONID)
        except Exception as e:
            print(f"[IG Follow random] login fallito: {e}")
            return

        hashtags = ["crypto", "memecoin", "ai", "solana", "trading", "tech", "coding", "nft", "bitcoin", "web3"]
        tag = random.choice(hashtags)
        print(f"[IG Follow random] hashtag #{tag}")
        try:
            medias = cl.hashtag_medias_recent(tag, amount=40)
        except Exception as e:
            print(f"[IG Follow random] errore hashtag: {e}")
            return

        user_ids = list({m.user.pk for m in medias if getattr(m, "user", None)})
        random.shuffle(user_ids)
        done = 0
        for uid in user_ids:
            if done >= count:
                break
            try:
                cl.user_follow(uid)
                done += 1
                print(f"[IG Follow random] seguito uid={uid} ({done}/{count})")
            except Exception as e:
                print(f"[IG Follow random] skip {uid}: {e}")
            time.sleep(random.uniform(delay_min, delay_max))
        print(f"[IG Follow random] finito ({done})")
    except Exception as e:
        print(f"[IG Follow random] ERRORE GENERALE: {e}")
        traceback.print_exc()

# ============================================================
# REDDIT
# ============================================================
def spam_reddit_free(subreddits, title, body, delay=400):
    print("[Reddit] inizio...")
    try:
        cookie_file = Path("reddit_cookies.txt")
        if not cookie_file.exists():
            print("[Reddit] manca reddit_cookies.txt. Salto.")
            return
        reddit_cookies = _load_netscape_cookies("reddit_cookies.txt", ["reddit.com"])
        if not reddit_cookies:
            print("[Reddit] Nessun cookie Reddit valido. Salto.")
            return

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=CHROMIUM_ARGS)
            context = browser.new_context(viewport={"width": 1280, "height": 900})
            context.add_cookies(reddit_cookies)
            page = context.new_page()

            for sub in subreddits:
                try:
                    page.goto(f"https://www.reddit.com/r/{sub}/submit", timeout=45000)
                    time.sleep(5)
                    page.keyboard.press("Escape")
                    time.sleep(1)
                    page.keyboard.type(title, delay=30)
                    time.sleep(1)
                    page.keyboard.press("Tab")
                    time.sleep(0.5)
                    page.keyboard.type(body, delay=20)
                    time.sleep(1)
                    page.keyboard.press("Control+Enter")
                    time.sleep(3)
                    try:
                        page.click('button:has-text("Post")', timeout=3000)
                    except Exception:
                        pass
                    print(f"[Reddit] tentativo post su r/{sub}")
                except Exception as e:
                    print(f"[Reddit] errore su r/{sub}: {e}")
                time.sleep(delay)
            print("[Reddit] Chiudo browser...")
            try:
                browser.close()
            except Exception as e:
                print(f"[Reddit] Errore chiusura browser: {e}")
        print("[Reddit] finito")
    except Exception as e:
        print(f"[Reddit] ERRORE GENERALE: {e}")
        traceback.print_exc()

# ============================================================
# DISCORD
# ============================================================
def spam_discord():
    print("[Discord] inizio...")
    try:
        import discord
    except ImportError:
        print("[Discord] discord.py-self non installato. Salto.")
        return

    if not DISCORD_USER_TOKEN.strip():
        print("[Discord] DISCORD_USER_TOKEN non impostato. Salto.")
        return

    async def _spam():
        try:
            client = discord.Client(self_bot=True)
        except TypeError:
            client = discord.Client()

        @client.event
        async def on_ready():
            print(f"[Discord] loggato come {client.user}")
            try:
                channels = []
                if DISCORD_CHANNEL_IDS:
                    for cid in DISCORD_CHANNEL_IDS:
                        ch = client.get_channel(int(cid))
                        if ch and isinstance(ch, discord.TextChannel):
                            channels.append(ch)
                else:
                    for guild in client.guilds:
                        for channel in guild.text_channels:
                            try:
                                perms = channel.permissions_for(guild.me)
                                if perms.send_messages:
                                    channels.append(channel)
                            except Exception:
                                continue
                    random.shuffle(channels)
                    channels = channels[:15]

                if not channels:
                    print("[Discord] nessun canale target")
                    await client.close()
                    return

                for ch in channels:
                    try:
                        await ch.send(PROMO_TEXT.strip() + "\n\n" + PROMO_MEMECOIN.strip())
                        print(f"[Discord] inviato in #{ch.name}")
                    except Exception as e:
                        print(f"[Discord] errore in #{ch.name}: {e}")
                    await asyncio.sleep(random.uniform(10, 20))
            except Exception as e:
                print(f"[Discord] errore ciclo: {e}")
            finally:
                await client.close()

        try:
            await client.start(DISCORD_USER_TOKEN)
        except Exception as e:
            print(f"[Discord] Errore avvio: {e}")

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(_spam())
    except Exception as e:
        print(f"[Discord] ERRORE GENERALE: {e}")
        traceback.print_exc()
    finally:
        try:
            loop.close()
        except Exception:
            pass

# ============================================================
# FACEBOOK
# ============================================================
def spam_facebook_free(count=1, delay_min=180, delay_max=400):
    print("[Facebook] inizio...")
    try:
        cookie_file = Path("fb_cookies.txt")
        if not cookie_file.exists():
            print("[Facebook] manca fb_cookies.txt. Salto.")
            return
        fb_cookies = _load_netscape_cookies("fb_cookies.txt", ["facebook.com", "fb.com"])
        if len(fb_cookies) < 5:
            print(f"[Facebook] troppi pochi cookies ({len(fb_cookies)}). Salto.")
            return

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=CHROMIUM_ARGS)
            context = browser.new_context(
                viewport={"width": 1280, "height": 900},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            )
            context.add_cookies(fb_cookies)
            page = context.new_page()
            page.goto("https://www.facebook.com/", timeout=60000, wait_until="domcontentloaded")
            time.sleep(10)

            if "login" in page.url.lower():
                print("[Facebook] non loggato. Salto.")
                try:
                    browser.close()
                except Exception:
                    pass
                return

            print("[Facebook] loggato correttamente")

            for i in range(count):
                fb_msg = random.choice([
                    PROMO_MEMECOIN.strip(),
                    PROMO_MEMECOIN.strip()[:150],
                ])
                try:
                    for _ in range(3):
                        try:
                            page.keyboard.press("Escape")
                            time.sleep(0.5)
                        except Exception:
                            pass

                    try:
                        page.screenshot(path=f"fb_home_{i}.png")
                        print(f"[Facebook] Screenshot: fb_home_{i}.png")
                    except Exception:
                        pass

                    # Apri composer - più selettori
                    opened = False
                    composers = [
                        'div[role="button"]:has-text("A cosa stai pensando")',
                        'div[role="button"]:has-text("What\'s on your mind")',
                        'div[role="button"]:has-text("Crea un post")',
                        'div[role="button"]:has-text("Create a post")',
                        'div[role="button"]:has-text("Crea post")',
                        'span:has-text("A cosa stai pensando")',
                        'span:has-text("What\'s on your mind")',
                        'div[aria-label*="Crea un post"]',
                        'div[aria-label*="Create a post"]',
                        'div[aria-label*="A cosa stai pensando"]',
                        'div[aria-label*="What\'s on your mind"]',
                        'div[data-pagelet="FeedUnit"] div[role="button"]',
                        'div[data-pagelet="FeedUnit"] div[aria-label]',
                    ]
                    for sel in composers:
                        try:
                            loc = page.locator(sel).first
                            if loc.count() > 0:
                                loc.wait_for(state="visible", timeout=5000)
                                loc.click(timeout=10000, force=True)
                                print(f"[Facebook] Composer aperto con: {sel}")
                                opened = True
                                break
                        except Exception:
                            continue

                    if not opened:
                        print("[Facebook] Composer non trovato. Salto post.")
                        continue

                    time.sleep(5)

                    # Trova textbox - più selettori
                    text_box = None
                    for sel in [
                        'div[role="textbox"]',
                        'div[contenteditable="true"]',
                        'div[aria-label*="messaggio"]',
                        'div[aria-label*="message"]',
                        'div[aria-label*="A cosa stai pensando"]',
                        'div[aria-label*="What\'s on your mind"]',
                        'div[data-lexical-editor="true"]',
                    ]:
                        try:
                            loc = page.locator(sel).first
                            if loc.count() > 0:
                                loc.wait_for(state="visible", timeout=8000)
                                text_box = loc
                                print(f"[Facebook] Textbox trovata: {sel}")
                                break
                        except Exception:
                            continue

                    if text_box is None:
                        print("[Facebook] Textbox non trovata. Salto post.")
                        try:
                            page.screenshot(path=f"fb_no_textbox_{i}.png")
                        except Exception:
                            pass
                        continue

                    # Click con fallback
                    try:
                        text_box.click(timeout=5000)
                        print("[Facebook] Click normale sulla textbox")
                    except Exception:
                        try:
                            text_box.click(force=True, timeout=5000)
                            print("[Facebook] Click force=True sulla textbox")
                        except Exception:
                            try:
                                text_box.evaluate("el => el.click()")
                                text_box.evaluate("el => el.focus()")
                                print("[Facebook] Click + focus via JS")
                            except Exception as e3:
                                print(f"[Facebook] Click JS fallito: {e3}")

                    time.sleep(1)

                    # Scrivi con JS
                    try:
                        text_box.evaluate(
                            "(el, text) => { el.focus(); el.innerText = text; el.dispatchEvent(new Event('input', {bubbles: true})); }",
                            fb_msg
                        )
                        print(f"[Facebook] Testo impostato via JS ({len(fb_msg)} char)")
                    except Exception as e:
                        print(f"[Facebook] JS fallito, provo keyboard.type: {e}")
                        try:
                            page.keyboard.type(fb_msg, delay=15)
                            print(f"[Facebook] Testo digitato ({len(fb_msg)} char)")
                        except Exception as e2:
                            print(f"[Facebook] Errore digitazione: {e2}")

                    time.sleep(3)

                    # Screenshot prima di cercare Pubblica
                    try:
                        page.screenshot(path=f"fb_before_publish_{i}.png")
                        print(f"[Facebook] Screenshot: fb_before_publish_{i}.png")
                    except Exception:
                        pass

                    # Cerca il bottone Pubblica con MOLTI selettori
                    posted = False
                    post_buttons = [
                        # Italiano - aria-label
                        'div[aria-label="Pubblica"]',
                        'div[aria-label="Pubblica post"]',
                        'div[aria-label="Pubblica adesso"]',
                        # Italiano - role button con testo
                        'div[role="button"]:has-text("Pubblica")',
                        'div[role="button"]:has-text("Pubblica post")',
                        'div[role="button"]:has-text("Pubblica adesso")',
                        # Inglese - aria-label
                        'div[aria-label="Post"]',
                        'div[aria-label="Publish"]',
                        'div[aria-label="Post now"]',
                        # Inglese - role button con testo
                        'div[role="button"]:has-text("Post")',
                        'div[role="button"]:has-text("Publish")',
                        'div[role="button"]:has-text("Post now")',
                        # Generico - qualsiasi bottone con testo
                        'div[role="button"][aria-label*="Pubblica"]',
                        'div[role="button"][aria-label*="Post"]',
                        'div[role="button"][aria-label*="Publish"]',
                        # Fallback: ultimo bottone del dialog
                        'div[role="dialog"] div[role="button"]:last-child',
                        'div[role="dialog"] div[aria-label="Pubblica"]',
                        'div[role="dialog"] div[aria-label="Post"]',
                        'div[role="dialog"] div[aria-label="Publish"]',
                        # Fallback: qualsiasi span con testo Pubblica
                        'span:has-text("Pubblica")',
                        'span:has-text("Post")',
                        # Fallback: cerca il bottone con sfondo blu
                        'div[role="dialog"] div[style*="background-color: rgb(24, 119, 242)"]',
                        'div[role="dialog"] div[style*="background-color: #1877F2"]',
                    ]
                    for sel in post_buttons:
                        try:
                            loc = page.locator(sel).first
                            if loc.count() > 0:
                                loc.wait_for(state="visible", timeout=5000)
                                loc.click(timeout=10000, force=True)
                                posted = True
                                print(f"[Facebook] Click Pubblica con: {sel}")
                                break
                        except Exception:
                            continue

                    if posted:
                        print(f"[Facebook] {i+1}/{count} postato")
                    else:
                        print(f"[Facebook] {i+1}/{count} bottone Pubblica non trovato")
                        try:
                            page.screenshot(path=f"fb_no_publish_{i}.png")
                            print(f"[Facebook] Screenshot: fb_no_publish_{i}.png")
                        except Exception:
                            pass

                except Exception as e:
                    print(f"[Facebook] errore post: {e}")
                time.sleep(random.uniform(delay_min, delay_max))
            print("[Facebook] Chiudo browser...")
            try:
                browser.close()
                print("[Facebook] Browser chiuso")
            except Exception as e:
                print(f"[Facebook] Errore chiusura browser: {e}")
        print("[Facebook] finito")
    except Exception as e:
        print(f"[Facebook] ERRORE GENERALE: {e}")
        traceback.print_exc()


def follow_facebook_random(count=3, delay_min=60, delay_max=120):
    print("[FB Follow random] inizio...")
    try:
        fb_cookies = _load_netscape_cookies("fb_cookies.txt", ["facebook.com", "fb.com"])
        if not fb_cookies:
            print("[FB Follow random] manca fb_cookies.txt. Salto.")
            return
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=CHROMIUM_ARGS)
            context = browser.new_context(
                viewport={"width": 1280, "height": 900},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            )
            context.add_cookies(fb_cookies)
            page = context.new_page()
            page.goto("https://www.facebook.com/friends/suggestions", timeout=60000, wait_until="domcontentloaded")
            time.sleep(6)
            page.keyboard.press("Escape")
            time.sleep(1)
            clicked = 0
            for sel in ['div[aria-label="Segui"]', 'div[aria-label="Follow"]', 'div[aria-label="Aggiungi amico"]', 'div[aria-label="Add friend"]']:
                if clicked >= count:
                    break
                btns = page.query_selector_all(sel)
                random.shuffle(btns)
                for btn in btns:
                    if clicked >= count:
                        break
                    try:
                        btn.click(timeout=5000)
                        clicked += 1
                        print(f"[FB Follow random] azione #{clicked}")
                        time.sleep(random.uniform(delay_min, delay_max))
                    except Exception:
                        pass
            print("[FB Follow random] Chiudo browser...")
            try:
                browser.close()
            except Exception as e:
                print(f"[FB Follow random] Errore chiusura browser: {e}")
        print(f"[FB Follow random] finito ({clicked})")
    except Exception as e:
        print(f"[FB Follow random] ERRORE: {e}")
        traceback.print_exc()

# ============================================================
# TIKTOK
# ============================================================
def spam_tiktok_free(video_path="promo.mp4", count=1, delay=600):
    print("[TikTok] inizio...")
    try:
        cookie_file = Path("tiktok_cookies.txt")
        if not cookie_file.exists():
            print("[TikTok] manca tiktok_cookies.txt. Salto.")
            return
        if not Path(video_path).exists():
            print(f"[TikTok] manca il video {video_path}. Salto.")
            return
        tiktok_cookies = _load_netscape_cookies("tiktok_cookies.txt", ["tiktok.com"])
        if not tiktok_cookies:
            print("[TikTok] Nessun cookie TikTok valido. Salto.")
            return

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=CHROMIUM_ARGS)
            context = browser.new_context(
                viewport={"width": 1280, "height": 900},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            )
            context.add_cookies(tiktok_cookies)
            page = context.new_page()
            page.goto("https://www.tiktok.com/tiktokstudio/upload", timeout=60000, wait_until="domcontentloaded")
            time.sleep(8)
            for _ in range(4):
                try:
                    page.keyboard.press("Escape")
                    time.sleep(0.4)
                except Exception:
                    pass
            for i in range(count):
                try:
                    time.sleep(3)
                    page.keyboard.press("Escape")
                    time.sleep(1)
                    file_input = None
                    for sel in ['input[type="file"]', 'input[type="file"][accept*="video"]', 'input[type="file"][accept*="mp4"]', 'input[accept*="video"]']:
                        try:
                            loc = page.locator(sel).first
                            if loc.count() > 0:
                                file_input = loc
                                break
                        except Exception:
                            continue
                    if file_input is None:
                        print("[TikTok] input file non trovato. Salto.")
                        continue
                    file_input.set_input_files(video_path)
                    print("[TikTok] video caricato, attendo...")
                    time.sleep(20)
                    page.keyboard.press("Escape")
                    time.sleep(1)
                    for sel in ['div[contenteditable="true"]', 'div[data-e2e="caption_container"] div[contenteditable]']:
                        try:
                            page.click(sel, timeout=5000)
                            page.keyboard.type(random.choice(MESSAGES)[:150], delay=25)
                            break
                        except Exception:
                            continue
                    time.sleep(2)
                    for label in ["Got it", "Cancel", "Turn on", "Close", "OK", "Not now"]:
                        try:
                            page.click(f'button:has-text("{label}")', timeout=2000)
                            time.sleep(1)
                        except Exception:
                            pass
                    posted = False
                    for sel in ['button[data-e2e="post_video_button"]', 'button:has-text("Post")', 'button:has-text("Pubblica")', 'button:has-text("Publish")']:
                        try:
                            elements = page.query_selector_all(sel)
                            for el in elements:
                                text = (el.inner_text() or "").strip().lower()
                                if text in ("post", "pubblica", "publish") or "post" in text:
                                    el.click(force=True, timeout=8000)
                                    posted = True
                                    break
                            if posted:
                                break
                        except Exception:
                            continue
                    if posted:
                        print(f"[TikTok] {i+1}/{count} postato")
                    else:
                        print(f"[TikTok] {i+1}/{count} bottone Post non trovato")
                except Exception as e:
                    print(f"[TikTok] errore post: {e}")
                time.sleep(delay)
            print("[TikTok] Chiudo browser...")
            try:
                browser.close()
                print("[TikTok] Browser chiuso")
            except Exception as e:
                print(f"[TikTok] Errore chiusura browser: {e}")
        print("[TikTok] finito")
    except Exception as e:
        print(f"[TikTok] ERRORE GENERALE: {e}")
        traceback.print_exc()

def follow_tiktok_random(count=3, delay_min=50, delay_max=100):
    print("[TT Follow random] inizio...")
    try:
        tiktok_cookies = _load_netscape_cookies("tiktok_cookies.txt", ["tiktok.com"])
        if not tiktok_cookies:
            print("[TT Follow random] manca tiktok_cookies.txt. Salto.")
            return
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=CHROMIUM_ARGS)
            context = browser.new_context(
                viewport={"width": 1280, "height": 900},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            )
            context.add_cookies(tiktok_cookies)
            page = context.new_page()
            page.goto("https://www.tiktok.com/foryou", timeout=60000, wait_until="domcontentloaded")
            time.sleep(6)
            clicked = 0
            for _ in range(count * 4):
                if clicked >= count:
                    break
                page.keyboard.press("Escape")
                time.sleep(0.4)
                for sel in ['button[data-e2e="follow-button"]', '[data-e2e="follow-button"]', 'button:has-text("Follow")', 'button:has-text("Segui")']:
                    try:
                        loc = page.locator(sel).first
                        if loc.count() == 0:
                            continue
                        txt = (loc.inner_text(timeout=1500) or "").lower()
                        if any(x in txt for x in ("following", "friends", "segui già")):
                            break
                        loc.click(timeout=5000, force=True)
                        clicked += 1
                        print(f"[TT Follow random] follow #{clicked}")
                        time.sleep(random.uniform(delay_min, delay_max))
                        break
                    except Exception:
                        continue
                page.keyboard.press("ArrowDown")
                time.sleep(2)
            print("[TT Follow random] Chiudo browser...")
            try:
                browser.close()
            except Exception as e:
                print(f"[TT Follow random] Errore chiusura browser: {e}")
        print(f"[TT Follow random] finito ({clicked})")
    except Exception as e:
        print(f"[TT Follow random] ERRORE: {e}")
        traceback.print_exc()

# ============================================================
# MAIN - LOOP CONTINUO CON UN SOCIAL PER CICLO
# ============================================================
if __name__ == "__main__":
    print("=== 15. MAIN INIZIATO ===")
    import threading
    import http.server
    import socketserver

    PORT = int(os.environ.get("PORT", 10000))

    class ReusableTCPServer(socketserver.TCPServer):
        allow_reuse_address = True

    class HealthHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"ok")

        def do_HEAD(self):
            self.send_response(200)
            self.end_headers()

        def log_message(self, *args):
            pass

    def start_health_server():
        try:
            with ReusableTCPServer(("0.0.0.0", PORT), HealthHandler) as httpd:
                print(f"[Health] Server in ascolto su porta {PORT}")
                httpd.serve_forever()
        except Exception as e:
            print(f"[Health] ERRORE: {e}")

    print("=== 16. AVVIO THREAD HEALTH ===")
    health_thread = threading.Thread(target=start_health_server, daemon=True)
    health_thread.start()

    print("=== 17. BOT MULTI-SOCIAL ATTIVO ===")
    print(f"=== PORT={PORT} - Il server HTTP è in un thread separato ===")
    print("Ctrl+C per fermarlo\n")

    socials = ["facebook", "tiktok", "instagram", "reddit", "discord", "x"]
    indice = 0
    ciclo = 1

    while True:
        social = socials[indice]
        print(f"\n========== CICLO {ciclo} - Social: {social.upper()} ==========")

        try:
            if social == "x":
                print("--- X POST ---")
                run_spam_in_thread(spam_x_free, count=1, delay_min=30, delay_max=60)
                print("--- X FOLLOW ---")
                run_spam_in_thread(follow_x_random, count=3, delay_min=15, delay_max=30)

            elif social == "reddit":
                print("--- REDDIT ---")
                run_spam_in_thread(
                    spam_reddit_free,
                    subreddits=random.sample(REDDIT_SUB_POOL, k=min(1, len(REDDIT_SUB_POOL))),
                    title="Nuova community + bot",
                    body=PROMO_TEXT,
                    delay=120,
                )

            elif social == "discord":
                print("--- DISCORD ---")
                run_spam_in_thread(spam_discord)

            elif social == "facebook":
                print("--- FACEBOOK ---")
                run_spam_in_thread(spam_facebook_free, count=1, delay_min=60, delay_max=120)
                print("--- FB FOLLOW ---")
                run_spam_in_thread(follow_facebook_random, count=2, delay_min=30, delay_max=60)

            elif social == "tiktok":
                print("--- TIKTOK ---")
                run_spam_in_thread(spam_tiktok_free, video_path="promo.mp4", count=1, delay=120)
                print("--- TT FOLLOW ---")
                run_spam_in_thread(follow_tiktok_random, count=2, delay_min=30, delay_max=60)

            elif social == "instagram":
                print("--- INSTAGRAM ---")
                run_spam_in_thread(spam_instagram, count=1, delay=120)
                print("--- IG FOLLOW ---")
                run_spam_in_thread(follow_instagram_random, count=3, delay_min=20, delay_max=40)

        except Exception as e:
            print(f"[{social}] errore critico: {e}")
            traceback.print_exc()

        indice = (indice + 1) % len(socials)
        ciclo += 1

        print(f"\n=== Fine ciclo {ciclo-1} ===")
        print("Aspetto 30 secondi...\n")
        time.sleep(30)
