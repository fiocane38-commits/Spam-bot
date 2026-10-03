# multi_spam_free.py
# pip install playwright praw discord.py-self instagrapi requests
# playwright install chromium

import time
import random
import asyncio
from pathlib import Path
from playwright.sync_api import sync_playwright


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

# Facebook, IG, Discord, Reddit, TikTok → messaggio completo
MESSAGES = [
    PROMO_TEXT.strip(),
    PROMO_MEMECOIN.strip(),
    PROMO_TEXT.strip() + "\n\n" + PROMO_MEMECOIN.strip(),
]

# Solo X → corto
MESSAGES_X = [
    PROMO_MEMECOIN.strip(),
]

# ============================================================
# POOL FOLLOW RANDOM
# ============================================================
X_FOLLOW_POOL = [
    "elonmusk", "nvidia", "openai", "github", "microsoft",
    "google", "meta", "apple", "tesla", "spacex",
    "nasa", "vercel", "docker", "huggingface", "solana",
    "bitcoin", "ethereum", "binance", "coinbase", "kraken",
]

IG_FOLLOW_POOL = [
    "instagram", "natgeo", "nasa", "nike", "adidas",
    "teslamotors", "spacex", "openai", "google", "meta",
    "solana", "binance", "coinbase", "apple", "microsoft",
]

TT_FOLLOW_POOL = [
    "tiktok", "charlidamelio", "khaby.lame", "mrbeast", "nasa",
    "nike", "adidas", "spacex", "google", "microsoft",
]

REDDIT_SUB_POOL = [
    "test", "python", "technology", "cryptocurrency", "solana",
    "CryptoCurrency", "SatoshiStreetBets", "ethtrader",
]

FB_FOLLOW_POOL = [
    # username o ID pubblici (pagine / profili che puoi aprire da browser)
    "zuck",
    "meta",
    "instagram",
    "nasa",
    "natgeo",
    "Nike",
    "adidas",
    "spacex",
    "tesla",
    "Microsoft",
]

def _load_netscape_cookies(path, domain_substr):
    cookies = []
    p = Path(path)
    if not p.exists():
        return cookies
    with open(p, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 7:
                continue
            domain, flag, path_c, secure, expires, name, value = parts[:7]
            c = {
                "name": name,
                "value": value,
                "domain": domain,
                "path": path_c,
                "secure": secure.upper() == "TRUE",
            }
            try:
                c["expires"] = int(expires)
            except Exception:
                pass
            if any(d in domain for d in domain_substr):
                cookies.append(c)
    return cookies

# ============================================================
# X (Playwright + cookies) - GRATIS
# ============================================================
# 1. Loggati su x.com nel browser
# 2. Installa estensione "Cookie-Editor"
# 3. Esporta come JSON e salva come x_cookies.json

def spam_x_free(count=2, delay_min=120, delay_max=300):
    print("[X] inizio (browser headless)...")
    from pathlib import Path

    cookie_file = Path("x_cookies.json")
    if not cookie_file.exists():
        print("[X] file non trovato")
        return

    cookies = []
    with open(cookie_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 7:
                continue
            domain, flag, path, secure, expires, name, value = parts[:7]
            cookie = {
                "name": name,
                "value": value,
                "domain": domain,
                "path": path,
                "secure": secure.upper() == "TRUE",
            }
            try:
                cookie["expires"] = int(expires)
            except Exception:
                pass
            cookies.append(cookie)

    print(f"[X] caricati {len(cookies)} cookies")
    x_cookies = [c for c in cookies if "x.com" in c["domain"] or "twitter.com" in c["domain"]]
    print(f"[X] di cui X/Twitter: {len(x_cookies)}")

    if len(x_cookies) < 3:
        print("[X] troppi pochi cookies di X")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"],
        )
        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        )
        context.add_cookies(x_cookies)
        page = context.new_page()

        page.goto("https://x.com/home", timeout=60000)
        time.sleep(5)

        if "login" in page.url.lower() or "i/flow/login" in page.url:
            print("[X] non loggato - cookies scaduti")
            browser.close()
            return

        print("[X] loggato correttamente")

        for i in range(count):
            msg = random.choice(MESSAGES_X).strip()
            if random.random() < 0.5:
                msg = msg + "\n"
            msg = msg[:280]

            try:
                page.goto("https://x.com/compose/post", timeout=30000)
                time.sleep(4)
                for _ in range(3):
                    page.keyboard.press("Escape")
                    time.sleep(0.3)

                box = page.locator('div[data-testid="tweetTextarea_0"]').first
                box.click(timeout=10000)
                time.sleep(0.5)
                page.keyboard.press("Control+A")
                page.keyboard.press("Backspace")
                time.sleep(0.3)
                page.keyboard.type(msg, delay=40)
                time.sleep(2)

                try:
                    content = page.locator('div[data-testid="tweetTextarea_0"]').inner_text(timeout=3000)
                    print(f"[X] testo nel box ({len(content)} char): {content[:60]!r}")
                except Exception:
                    content = ""

                if len(content.strip()) < 3:
                    print("[X] testo NON inserito, riprovo con JS")
                    page.evaluate(
                        "(t) => { const el = document.querySelector('div[data-testid=\"tweetTextarea_0\"]'); if (!el) return; el.focus(); document.execCommand('selectAll', false, null); document.execCommand('insertText', false, t); }",
                        msg,
                    )
                    time.sleep(1.5)

                # bottone giusto su /compose/post = tweetButtonInline
                btn = page.locator('button[data-testid="tweetButtonInline"]').first
                if btn.count() == 0:
                    btn = page.locator('button[data-testid="tweetButton"]').first
                if btn.count() == 0:
                    btn = page.locator('button:has-text("Post")').first

                enabled = False
                for _ in range(10):
                    try:
                        dis = btn.get_attribute("aria-disabled")
                        print(f"[X] aria-disabled={dis!r}")
                        if dis in (None, "false"):
                            enabled = True
                            break
                    except Exception:
                        pass
                    time.sleep(1)

                if enabled and btn.count() > 0:
                    btn.click(timeout=5000)
                    print("[X] click Post")
                else:
                    page.keyboard.press("Control+Enter")
                    print("[X] fallback Ctrl+Enter")

                time.sleep(5)
                print("[X] URL dopo:", page.url)
                page.screenshot(path=f"x_dopo_{i}.png")

                if "compose" in page.url:
                    print("[X] ancora compose - secondo Ctrl+Enter")
                    page.keyboard.press("Control+Enter")
                    time.sleep(4)
                    print("[X] URL 2:", page.url)
                else:
                    print(f"[X] {i+1}/{count} ok")

            except Exception as e:
                print(f"[X] errore: {e}")
                try:
                    page.screenshot(path=f"errore_x_{i}.png")
                except Exception:
                    pass

            time.sleep(random.uniform(delay_min, delay_max))

        browser.close()
    print("[X] finito")


def follow_instagram(usernames=None, count=5, delay_min=40, delay_max=90):
    print("[Instagram Follow] inizio...")
    from instagrapi import Client
    from pathlib import Path
    import random
    import time

    # stesso SESSIONID di spam_instagram
    SESSIONID = ""

    pool = usernames or IG_FOLLOW_POOL
    targets = random.sample(pool, k=min(count, len(pool)))

    cl = Client()
    try:
        cl.set_app("448.0.0.0.20")
    except Exception:
        pass

    try:
        if Path("ig_session.json").exists():
            cl.load_settings("ig_session.json")
        cl.login_by_sessionid(SESSIONID)
    except Exception as e:
        print(f"[Instagram Follow] login fallito: {e}")
        return

    for user in targets:
        try:
            uid = cl.user_id_from_username(user)
            cl.user_follow(uid)
            print(f"[Instagram Follow] seguito @{user}")
        except Exception as e:
            print(f"[Instagram Follow] errore @{user}: {e}")
        time.sleep(random.uniform(delay_min, delay_max))
    print("[Instagram Follow] finito")


def follow_tiktok(usernames=None, count=3, delay_min=50, delay_max=100):
    print("[TikTok Follow] inizio...")
    from pathlib import Path
    import random
    import time
    from playwright.sync_api import sync_playwright

    pool = usernames or TT_FOLLOW_POOL
    targets = random.sample(pool, k=min(count, len(pool)))

    cookie_file = Path("tiktok_cookies.txt")
    if not cookie_file.exists():
        print("[TikTok Follow] manca tiktok_cookies.txt")
        return

    cookies = []
    with open(cookie_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 7:
                continue
            cookies.append({
                "name": parts[5],
                "value": parts[6],
                "domain": parts[0],
                "path": parts[2],
                "secure": parts[3].upper() == "TRUE",
            })
    tiktok_cookies = [c for c in cookies if "tiktok.com" in c["domain"]]

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        context.add_cookies(tiktok_cookies)
        page = context.new_page()

        for user in targets:
            try:
                page.goto(f"https://www.tiktok.com/@{user}", timeout=45000)
                time.sleep(5)

                # chiudi popup
                for _ in range(3):
                    page.keyboard.press("Escape")
                    time.sleep(0.4)
                for label in ["Got it", "Accept", "Allow all", "Rifiuta", "Reject"]:
                    try:
                        page.click(f'button:has-text("{label}")', timeout=1500)
                    except:
                        pass

                # se già seguito
                already = page.query_selector(
                    'button:has-text("Following"), button:has-text("Friends"), '
                    'button:has-text("Segui già"), button:has-text("Messaggio")'
                )
                if already:
                    print(f"[TikTok Follow] già seguito @{user}")
                    time.sleep(random.uniform(delay_min, delay_max))
                    continue

                # prova selettori multipli
                followed = False
                selectors = [
                    'button[data-e2e="follow-button"]',
                    '[data-e2e="follow-button"]',
                    'button[data-e2e="browse-follow"]',
                    'button:has-text("Follow")',
                    'button:has-text("Segui")',
                    'button:has-text("Follow back")',
                    'div[data-e2e="user-page"] button >> text=Follow',
                    'div[data-e2e="user-page"] button >> text=Segui',
                ]
                for sel in selectors:
                    try:
                        btn = page.locator(sel).first
                        if btn.count() == 0:
                            continue
                        txt = (btn.inner_text(timeout=2000) or "").strip().lower()
                        if any(x in txt for x in ["following", "friends", "segui già", "message", "messaggio"]):
                            print(f"[TikTok Follow] già seguito @{user}")
                            followed = True
                            break
                        btn.click(timeout=4000, force=True)
                        print(f"[TikTok Follow] seguito @{user} ({txt or sel})")
                        followed = True
                        break
                    except:
                        continue

                if not followed:
                    # fallback: primo bottone rosso/rosa nella header profilo
                    try:
                        page.locator('button').filter(has_text="Follow").first.click(timeout=3000)
                        print(f"[TikTok Follow] seguito @{user} (fallback)")
                        followed = True
                    except:
                        pass

                if not followed:
                    page.screenshot(path=f"tt_follow_fail_{user}.png")
                    print(f"[TikTok Follow] bottone non trovato @{user} → screenshot tt_follow_fail_{user}.png")

            except Exception as e:
                print(f"[TikTok Follow] errore @{user}: {e}")

            time.sleep(random.uniform(delay_min, delay_max))

        browser.close()
    print("[TikTok Follow] finito")

def follow_facebook(usernames=None, count=3, delay_min=60, delay_max=120):
    """
    Prova a seguire profili/pagine a caso.
    Facebook cambia spesso UI → può fallire; delay alti consigliati.
    """
    print("[Facebook Follow] inizio...")
    from pathlib import Path
    import random
    import time
    from playwright.sync_api import sync_playwright

    pool = usernames or FB_FOLLOW_POOL
    targets = random.sample(pool, k=min(count, len(pool)))

    cookie_file = Path("fb_cookies.txt")
    if not cookie_file.exists():
        print("[Facebook Follow] manca fb_cookies.txt")
        return

    cookies = []
    with open(cookie_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 7:
                continue
            cookies.append({
                "name": parts[5],
                "value": parts[6],
                "domain": parts[0],
                "path": parts[2],
                "secure": parts[3].upper() == "TRUE",
            })
    fb_cookies = [c for c in cookies if "facebook.com" in c["domain"] or "fb.com" in c["domain"]]

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        context.add_cookies(fb_cookies)
        page = context.new_page()

        page.goto("https://www.facebook.com/", timeout=60000)
        time.sleep(5)
        if "login" in page.url.lower():
            print("[Facebook Follow] non loggato")
            browser.close()
            return

        for user in targets:
            try:
                page.goto(f"https://www.facebook.com/{user}", timeout=45000)
                time.sleep(4)
                page.keyboard.press("Escape")
                time.sleep(1)

                followed = False
                for sel in [
                    'div[aria-label="Segui"]',
                    'div[aria-label="Follow"]',
                    'div[aria-label="Mi piace"]',
                    'div[aria-label="Like"]',
                    'div[role="button"]:has-text("Segui")',
                    'div[role="button"]:has-text("Follow")',
                    'div[role="button"]:has-text("Mi piace")',
                    'div[role="button"]:has-text("Like")',
                ]:
                    try:
                        page.click(sel, timeout=3000)
                        print(f"[Facebook Follow] ok → {user} ({sel})")
                        followed = True
                        break
                    except:
                        continue

                if not followed:
                    page.screenshot(path=f"fb_follow_fail_{user}.png")
                    print(f"[Facebook Follow] bottone non trovato → {user}")

            except Exception as e:
                print(f"[Facebook Follow] errore {user}: {e}")

            time.sleep(random.uniform(delay_min, delay_max))

        browser.close()
    print("[Facebook Follow] finito")

def follow_x_random(count=5, delay_min=40, delay_max=90):
    """Suggested: https://x.com/i/connect_people"""
    print("[X Follow random] inizio...")
    x_cookies = _load_netscape_cookies("x_cookies.json", ["x.com", "twitter.com"])
    if not x_cookies:
        print("[X Follow random] manca x_cookies.json")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
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
            except Exception as e:
                print(f"[X Follow random] skip: {e}")
        browser.close()
    print(f"[X Follow random] finito ({clicked})")


def follow_instagram_random(count=5, delay_min=40, delay_max=90):
    """Autori random da hashtag recenti."""
    print("[IG Follow random] inizio...")
    from instagrapi import Client

    # usa lo stesso SESSIONID di spam_instagram
    SESSIONID = ""  # oppure incolla la stringa sessionid qui

    hashtags = [
        "crypto", "memecoin", "ai", "solana", "trading",
        "tech", "coding", "nft", "bitcoin", "web3",
    ]
    cl = Client()
    try:
        cl.set_app("448.0.0.0.20")
    except Exception:
        pass
    try:
        if Path("ig_session.json").exists():
            cl.load_settings("ig_session.json")
        cl.login_by_sessionid(SESSIONID)
    except Exception as e:
        print(f"[IG Follow random] login fallito: {e}")
        return

    tag = random.choice(hashtags)
    print(f"[IG Follow random] hashtag #{tag}")
    try:
        medias = cl.hashtag_medias_recent(tag, amount=40)
    except Exception as e:
        print(f"[IG Follow random] errore: {e}")
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


def follow_facebook_random(count=3, delay_min=60, delay_max=120):
    """People you may know / suggestions."""
    print("[FB Follow random] inizio...")
    fb_cookies = _load_netscape_cookies("fb_cookies.txt", ["facebook.com", "fb.com"])
    if not fb_cookies:
        print("[FB Follow random] manca fb_cookies.txt")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        )
        context.add_cookies(fb_cookies)
        page = context.new_page()
        for url in [
            "https://www.facebook.com/friends/suggestions",
            "https://www.facebook.com/",
        ]:
            page.goto(url, timeout=60000)
            time.sleep(5)
            page.keyboard.press("Escape")
            time.sleep(1)

        clicked = 0
        selectors = [
            'div[aria-label="Segui"]',
            'div[aria-label="Follow"]',
            'div[aria-label="Aggiungi amico"]',
            'div[aria-label="Add friend"]',
            'div[role="button"]:has-text("Segui")',
            'div[role="button"]:has-text("Follow")',
            'div[role="button"]:has-text("Aggiungi amico")',
            'div[role="button"]:has-text("Add friend")',
        ]
        for sel in selectors:
            if clicked >= count:
                break
            btns = page.query_selector_all(sel)
            random.shuffle(btns)
            for btn in btns:
                if clicked >= count:
                    break
                try:
                    btn.click(timeout=3000)
                    clicked += 1
                    print(f"[FB Follow random] azione #{clicked}")
                    time.sleep(random.uniform(delay_min, delay_max))
                except Exception:
                    pass
        if clicked == 0:
            page.screenshot(path="fb_follow_random_fail.png")
            print("[FB Follow random] nessun bottone → fb_follow_random_fail.png")
        browser.close()
    print(f"[FB Follow random] finito ({clicked})")


def follow_tiktok_random(count=3, delay_min=50, delay_max=100):
    """Follow creator dal feed For You."""
    print("[TT Follow random] inizio...")
    tiktok_cookies = _load_netscape_cookies("tiktok_cookies.txt", ["tiktok.com"])
    if not tiktok_cookies:
        print("[TT Follow random] manca tiktok_cookies.txt")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        )
        context.add_cookies(tiktok_cookies)
        page = context.new_page()
        page.goto("https://www.tiktok.com/foryou", timeout=60000)
        time.sleep(5)

        clicked = 0
        for _ in range(count * 4):
            if clicked >= count:
                break
            page.keyboard.press("Escape")
            time.sleep(0.4)
            for sel in [
                'button[data-e2e="follow-button"]',
                '[data-e2e="follow-button"]',
                'button:has-text("Follow")',
                'button:has-text("Segui")',
            ]:
                try:
                    loc = page.locator(sel).first
                    if loc.count() == 0:
                        continue
                    txt = (loc.inner_text(timeout=1500) or "").lower()
                    if any(x in txt for x in ("following", "friends", "segui già")):
                        break
                    loc.click(timeout=3000, force=True)
                    clicked += 1
                    print(f"[TT Follow random] follow #{clicked}")
                    time.sleep(random.uniform(delay_min, delay_max))
                    break
                except Exception:
                    continue
            page.keyboard.press("ArrowDown")
            time.sleep(2)
        browser.close()
    print(f"[TT Follow random] finito ({clicked})")

# ============================================================
# REDDIT (PRAW - ancora gratis)
# ============================================================
import praw

REDDIT_CLIENT_ID = "..."
REDDIT_CLIENT_SECRET = "..."
REDDIT_USER_AGENT = "promo_bot/1.0 by u/tuo_username"
REDDIT_USERNAME = "..."
REDDIT_PASSWORD = "..."

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT,
    username=REDDIT_USERNAME,
    password=REDDIT_PASSWORD
)

def spam_reddit_free(subreddits, title, body, delay=400):
    print("[Reddit Free] inizio...")
    from pathlib import Path

    cookie_file = Path("reddit_cookies.txt")
    cookies = []
    with open(cookie_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 7:
                continue
            domain, flag, path, secure, expires, name, value = parts[:7]
            cookie = {
                "name": name,
                "value": value,
                "domain": domain,
                "path": path,
                "secure": secure.upper() == "TRUE",
            }
            try:
                cookie["expires"] = int(expires)
            except:
                pass
            cookies.append(cookie)

    reddit_cookies = [c for c in cookies if "reddit.com" in c["domain"]]
    print(f"[Reddit] cookies: {len(reddit_cookies)}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        context.add_cookies(reddit_cookies)
        page = context.new_page()

        for sub in subreddits:
            try:
                # vai prima sulla home del sub
                page.goto(f"https://www.reddit.com/r/{sub}/", timeout=45000)
                time.sleep(4)

                # clicca sul bottone Create / Create Post
                create_selectors = [
                    'button:has-text("Create Post")',
                    'a:has-text("Create Post")',
                    'button:has-text("Create")',
                    '[data-testid="create-post-button"]',
                    'a[href*="/submit"]'
                ]
                clicked = False
                for sel in create_selectors:
                    try:
                        page.click(sel, timeout=4000)
                        clicked = True
                        break
                    except:
                        continue

                if not clicked:
                    # fallback diretto
                    page.goto(f"https://www.reddit.com/r/{sub}/submit", timeout=30000)

                time.sleep(4)
                page.keyboard.press("Escape")
                time.sleep(1)

                # ora prova a scrivere il titolo
                page.keyboard.type(title, delay=30)
                time.sleep(1)

                # vai al corpo (Tab)
                page.keyboard.press("Tab")
                time.sleep(0.5)
                page.keyboard.type(body, delay=20)
                time.sleep(1)

                # Post
                page.keyboard.press("Control+Enter")  # scorciatoia comune
                time.sleep(2)

                # oppure cerca bottone
                try:
                    page.click('button:has-text("Post")', timeout=3000)
                except:
                    pass

                print(f"[Reddit] tentativo post su r/{sub} completato")
            except Exception as e:
                print(f"[Reddit] errore su r/{sub}: {e}")
                page.screenshot(path=f"reddit_errore_{sub}.png")
                print("[Reddit] screenshot salvato")

            time.sleep(delay)

        browser.close()
    print("[Reddit Free] finito")


# ============================================================
# DISCORD (user account / self-bot - gratis)
# ============================================================
# Requirements: pip install discord.py-self
# USER TOKEN (account token, NOT bot token)
# How to get it (browser):
# 1. Open Discord in Chrome/Edge
# 2. F12 → Network tab → filter "api"
# 3. Send any message or reload
# 4. Look for request to /api/v9/users/@me or similar
# 5. Headers → authorization → copy the value

DISCORD_USER_TOKEN = ""

# Target channels (channel IDs as integers)
# Leave empty list [] to spam every text channel the account can see
DISCORD_CHANNEL_IDS = [
     
    # 987654321098765432,
]

# Target guilds (server IDs). If empty and CHANNEL_IDS empty → all accessible channels
DISCORD_GUILD_IDS = [
    # 111111111111111111,
]

# Behaviour
DISCORD_MESSAGES_PER_CHANNEL = 1          # how many messages per channel per cycle
DISCORD_DELAY_BETWEEN_MESSAGES = (25, 55) # seconds (min, max) between individual messages
DISCORD_DELAY_BETWEEN_CHANNELS = (40, 90) # seconds between different channels
DISCORD_MAX_CHANNELS_PER_CYCLE = 15       # safety limit
DISCORD_ONLY_TEXT_CHANNELS = True
DISCORD_CHANNEL_NAME_FILTER = []          # e.g. ["general", "chat", "spam"]

def spam_discord_user():
    """Self-bot: logs in as normal user and spams accessible text channels."""
    try:
        import discord
        from discord.ext import commands
    except ImportError:
        print("[Discord User] Install first: pip install discord.py-self")
        return

    if DISCORD_USER_TOKEN == "YOUR_USER_TOKEN_HERE" or not DISCORD_USER_TOKEN.strip():
        print("[Discord User] ERRORE: inserisci il tuo USER TOKEN in DISCORD_USER_TOKEN")
        print("[Discord User] Non usare un bot token. Serve il token dell'account utente.")
        return

    intents = discord.Intents.default()
    intents.message_content = True
    intents.guilds = True
    intents.members = False

    bot = commands.Bot(command_prefix="!", self_bot=True, intents=intents)

    def get_target_channels():
        channels = []

        if DISCORD_CHANNEL_IDS:
            for cid in DISCORD_CHANNEL_IDS:
                ch = bot.get_channel(int(cid))
                if ch and isinstance(ch, discord.TextChannel):
                    channels.append(ch)
            return channels

        guilds = []
        if DISCORD_GUILD_IDS:
            for gid in DISCORD_GUILD_IDS:
                g = bot.get_guild(int(gid))
                if g:
                    guilds.append(g)
        else:
            guilds = list(bot.guilds)

        for guild in guilds:
            for channel in guild.text_channels:
                perms = channel.permissions_for(guild.me)
                if not perms.send_messages:
                    continue
                if DISCORD_ONLY_TEXT_CHANNELS and not isinstance(channel, discord.TextChannel):
                    continue
                if DISCORD_CHANNEL_NAME_FILTER:
                    name_lower = channel.name.lower()
                    if not any(f.lower() in name_lower for f in DISCORD_CHANNEL_NAME_FILTER):
                        continue
                channels.append(channel)

        random.shuffle(channels)
        return channels[:DISCORD_MAX_CHANNELS_PER_CYCLE]

    async def spam_cycle():
        targets = get_target_channels()
        if not targets:
            print("[Discord User] nessun canale target trovato")
            return

        print(f"[Discord User] {len(targets)} canali selezionati")

        for ch in targets:
            for _ in range(DISCORD_MESSAGES_PER_CHANNEL):
                msg = PROMO_TEXT.strip() + "\n\n" + PROMO_MEMECOIN.strip()
                try:
                    await ch.send(msg)
                    print(f"[Discord User] inviato in #{ch.name} ({ch.guild.name}) → {ch.id}")
                except discord.Forbidden:
                    print(f"[Discord User] no permission in #{ch.name}")
                except discord.HTTPException as e:
                    print(f"[Discord User] HTTP error {e.status} in #{ch.name}: {e}")
                except Exception as e:
                    print(f"[Discord User] errore in #{ch.name}: {e}")

                delay = random.uniform(*DISCORD_DELAY_BETWEEN_MESSAGES)
                await asyncio.sleep(delay)

            delay_ch = random.uniform(*DISCORD_DELAY_BETWEEN_CHANNELS)
            await asyncio.sleep(delay_ch)

    @bot.event
    async def on_ready():
        print(f"[Discord User] loggato come {bot.user} (ID: {bot.user.id})")
        print(f"[Discord User] presente in {len(bot.guilds)} server")
        try:
            await spam_cycle()
        except Exception as e:
            print(f"[Discord User] errore ciclo: {e}")
        await bot.close()

    print("[Discord User] avvio self-bot...")
    try:
        bot.run(DISCORD_USER_TOKEN)
    except discord.LoginFailure:
        print("[Discord User] Login fallito: token non valido o scaduto")
    except Exception as e:
        print(f"[Discord User] Errore avvio: {e}")


# ============================================================
# INSTAGRAM (instagrapi - gratis ma rischio ban)
# ============================================================
def spam_instagram(count=1, delay=600):
    print("[Instagram] inizio...")
    from instagrapi import Client
    from pathlib import Path
    import random
    import time

    # Incolla qui il sessionid preso dal browser
    SESSIONID = ""

    cl = Client()
    try:
        cl.set_app("448.0.0.0.20")
    except Exception:
        pass

    try:
        cl.login_by_sessionid(SESSIONID)
        print("[Instagram] login ok (sessionid)")
        cl.dump_settings("ig_session.json")
    except Exception as e:
        print(f"[Instagram] login fallito: {e}")
        return

    for i in range(count):
        try:
            if not Path("promo.jpg").exists():
                print("[Instagram] manca promo.jpg nella cartella")
                break
            media = cl.photo_upload(
                path="promo.jpg",
                caption=random.choice(MESSAGES)
            )
            print(f"[Instagram] postato → {media.code}")
        except Exception as e:
            print(f"[Instagram] errore post: {e}")
        time.sleep(delay)
    print("[Instagram] finito")

# ============================================================
# FACEBOOK PAGE (Graph API - gratis)
# ============================================================
import requests

FB_PAGE_ID = "..."
FB_PAGE_ACCESS_TOKEN = "..."

def spam_facebook_free(count=1, delay_min=180, delay_max=400):
    """
    Posta su Facebook usando cookies esportati.
    File richiesto: fb_cookies.txt (formato Netscape)
    """
    print("[Facebook] inizio (cookies)...")
    from pathlib import Path
    import random
    import time
    from playwright.sync_api import sync_playwright

    cookie_file = Path("fb_cookies.txt")
    if not cookie_file.exists():
        print("[Facebook] file fb_cookies.txt non trovato")
        return

    cookies = []
    with open(cookie_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 7:
                continue
            domain, flag, path, secure, expires, name, value = parts[:7]
            cookie = {
                "name": name,
                "value": value,
                "domain": domain,
                "path": path,
                "secure": secure.upper() == "TRUE",
            }
            try:
                cookie["expires"] = int(expires)
            except:
                pass
            cookies.append(cookie)

    fb_cookies = [c for c in cookies if "facebook.com" in c["domain"] or "fb.com" in c["domain"]]
    print(f"[Facebook] cookies caricati: {len(fb_cookies)}")

    if len(fb_cookies) < 5:
        print("[Facebook] troppi pochi cookies. Riesporta da facebook.com loggato")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        context.add_cookies(fb_cookies)
        page = context.new_page()

        page.goto("https://www.facebook.com/", timeout=60000)
        time.sleep(6)

        # controllo login
        if "login" in page.url.lower():
            print("[Facebook] non loggato - cookies scaduti o incompleti")
            browser.close()
            return

        print("[Facebook] loggato correttamente")

        for i in range(count):
            msg = random.choice(MESSAGES)
            try:
                # chiudi eventuali popup
                try:
                    page.keyboard.press("Escape")
                    time.sleep(0.8)
                except:
                    pass

                # apri il composer (più selettori per lingue diverse)
                opened = False
                composers = [
                    'div[aria-label*="Crea un post"]',
                    'div[aria-label*="Create a post"]',
                    'div[aria-label*="What\'s on your mind"]',
                    'span:has-text("A cosa stai pensando")',
                    'span:has-text("What\'s on your mind")',
                    'div[role="button"]:has-text("Foto/video")',
                ]
                for sel in composers:
                    try:
                        page.click(sel, timeout=4000)
                        opened = True
                        break
                    except:
                        continue

                if not opened:
                    # fallback: vai diretto alla home e prova di nuovo
                    page.goto("https://www.facebook.com/", timeout=30000)
                    time.sleep(3)
                    page.click('div[aria-label*="Crea"], div[aria-label*="Create"]', timeout=5000)

                time.sleep(2)

                # scrivi il messaggio
                page.keyboard.type(msg, delay=35)
                time.sleep(1.5)

                # pubblica
                post_buttons = [
                    'div[aria-label="Pubblica"]',
                    'div[aria-label="Post"]',
                    'div[aria-label="Publish"]',
                    'div[role="button"]:has-text("Pubblica")',
                    'div[role="button"]:has-text("Post")',
                ]
                posted = False
                for sel in post_buttons:
                    try:
                        page.click(sel, timeout=4000)
                        posted = True
                        break
                    except:
                        continue

                if posted:
                    print(f"[Facebook] {i+1}/{count} postato")
                else:
                    print(f"[Facebook] {i+1}/{count} non ha trovato il bottone Pubblica")
                    page.screenshot(path=f"fb_errore_{i}.png")

            except Exception as e:
                print(f"[Facebook] errore: {e}")
                try:
                    page.screenshot(path=f"fb_errore_{i}.png")
                except:
                    pass

            time.sleep(random.uniform(delay_min, delay_max))

        browser.close()
    print("[Facebook] finito")

# ============================================================
# TIKTOK (cookies + browser - gratis)
# ============================================================

def spam_tiktok_free(video_path="promo.mp4", count=1, delay=600):
    print("[TikTok] inizio (cookies)...")
    from pathlib import Path
    import random
    import time
    from playwright.sync_api import sync_playwright

    cookie_file = Path("tiktok_cookies.txt")
    if not cookie_file.exists():
        print("[TikTok] manca tiktok_cookies.txt")
        return

    if not Path(video_path).exists():
        print(f"[TikTok] manca il video {video_path}")
        return

    cookies = []
    with open(cookie_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 7:
                continue
            domain, flag, path, secure, expires, name, value = parts[:7]
            cookie = {
                "name": name,
                "value": value,
                "domain": domain,
                "path": path,
                "secure": secure.upper() == "TRUE",
            }
            try:
                cookie["expires"] = int(expires)
            except Exception:
                pass
            cookies.append(cookie)

    tiktok_cookies = [c for c in cookies if "tiktok.com" in c["domain"]]
    print(f"[TikTok] cookies: {len(tiktok_cookies)}")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )
        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        )
        context.add_cookies(tiktok_cookies)
        page = context.new_page()

        page.goto("https://www.tiktok.com/tiktokstudio/upload", timeout=60000)
        time.sleep(6)

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
                for sel in [
                    'input[type="file"]',
                    'input[type="file"][accept*="video"]',
                    'input[type="file"][accept*="mp4"]',
                    'input[accept*="video"]',
                ]:
                    try:
                        loc = page.locator(sel).first
                        if loc.count() > 0:
                            file_input = loc
                            print(f"[TikTok] input trovato: {sel}")
                            break
                    except Exception:
                        continue

                if file_input is None:
                    for label in ["Select video", "Upload", "Carica", "Seleziona"]:
                        try:
                            page.click(f'text={label}', timeout=2500)
                            time.sleep(2)
                        except Exception:
                            pass
                    try:
                        if page.locator('input[type="file"]').count() > 0:
                            file_input = page.locator('input[type="file"]').first
                    except Exception:
                        pass

                if file_input is None:
                    page.screenshot(path=f"tiktok_no_input_{i}.png")
                    print("[TikTok] input file non trovato → tiktok_no_input_*.png")
                    print("[TikTok] URL:", page.url)
                    continue

                file_input.set_input_files(video_path)
                print("[TikTok] video caricato, aspetto elaborazione...")
                time.sleep(18)

                page.keyboard.press("Escape")
                time.sleep(1)

                for sel in [
                    'div[contenteditable="true"]',
                    'div[data-e2e="caption_container"] div[contenteditable]',
                    'div.public-DraftEditor-content',
                ]:
                    try:
                        page.click(sel, timeout=3000)
                        page.keyboard.type(random.choice(MESSAGES)[:150], delay=25)
                        break
                    except Exception:
                        continue

                time.sleep(2)
                for label in ["Got it", "Cancel", "Turn on", "Close", "OK", "Not now"]:
                    try:
                        page.click(f'button:has-text("{label}")', timeout=2000)
                        print(f"[TikTok] chiuso popup: {label}")
                        time.sleep(1)
                    except Exception:
                        pass
                page.keyboard.press("Escape")
                time.sleep(1)

                posted = False
                for sel in [
                    'button[data-e2e="post_video_button"]',
                    'button:has-text("Post")',
                    'button:has-text("Pubblica")',
                    'button:has-text("Publish")',
                ]:
                    try:
                        elements = page.query_selector_all(sel)
                        for el in elements:
                            text = (el.inner_text() or "").strip().lower()
                            if text in ("post", "pubblica", "publish") or "post" in text:
                                el.click(force=True, timeout=5000)
                                posted = True
                                print(f"[TikTok] cliccato: {text}")
                                break
                        if posted:
                            break
                    except Exception:
                        continue

                if not posted:
                    page.mouse.click(1100, 700)
                    print("[TikTok] tentativo click coordinate")

                time.sleep(2)
                for label in ["Cancel", "Turn on", "Got it"]:
                    try:
                        page.click(f'button:has-text("{label}")', timeout=2000)
                        print(f"[TikTok] chiuso dopo Post: {label}")
                    except Exception:
                        pass

                time.sleep(2)
                try:
                    page.click(
                        'button:has-text("Post"), button:has-text("Pubblica")',
                        timeout=5000,
                    )
                    print("[TikTok] Post finale")
                except Exception:
                    pass

                time.sleep(12)
                print("[TikTok] URL finale:", page.url)
                page.screenshot(path=f"tiktok_dopo_{i}.png")
                if "upload" in page.url or "draft" in page.url.lower():
                    print("[TikTok] ancora su upload → controlla Bozze")
                else:
                    print(f"[TikTok] {i+1}/{count} ok")

            except Exception as e:
                print(f"[TikTok] errore: {e}")
                try:
                    page.screenshot(path=f"tiktok_errore_{i}.png")
                except Exception:
                    pass

            time.sleep(delay)

        browser.close()
    print("[TikTok] finito")

# ============================================================
# MAIN - LOOP CONTINUO
# ============================================================
def spam_discord():
    import discord
    from discord.ext import commands
    import asyncio
    import random

    TOKEN = ""
    CHANNEL_IDS = []   # metti qui i tuoi ID canale

    intents = discord.Intents.default()
    intents.message_content = True
    intents.guilds = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f"[Discord] loggato come {bot.user}")
        for ch_id in CHANNEL_IDS:
            channel = bot.get_channel(int(ch_id))
            if channel is None:
                try:
                    channel = await bot.fetch_channel(int(ch_id))
                except Exception as e:
                    print(f"[Discord] canale {ch_id} non trovato: {e}")
                    continue
            try:
                await channel.send(random.choice(MESSAGES))
                print(f"[Discord] inviato in {ch_id}")
            except Exception as e:
                print(f"[Discord] errore invio: {e}")
            await asyncio.sleep(random.randint(20, 40))
        await bot.close()

    bot.run(TOKEN)

if __name__ == "__main__":
    import os
    import threading
    from http.server import BaseHTTPRequestHandler, HTTPServer

    def _health():
        port = int(os.environ.get("PORT", 10000))

        class H(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"ok")

            def log_message(self, *args):
                pass

        print(f"[Health] in ascolto su 0.0.0.0:{port}")
        HTTPServer(("0.0.0.0", port), H).serve_forever()

    threading.Thread(target=_health, daemon=True).start()
    time.sleep(1)

    print("=== BOT MULTI-SOCIAL ATTIVO ===")
    # ... resto del while True come ora ...
    print("=== BOT MULTI-SOCIAL ATTIVO ===")
    print("Ctrl+C per fermarlo\n")

    ciclo = 1
    while True:
        print(f"\n========== CICLO {ciclo} ==========")

        # 1. X POST
        try:
            print("\n--- X POST ---")
            spam_x_free(count=1, delay_min=90, delay_max=180)
        except Exception as e:
            print(f"[X] errore: {e}")

        # 2. X FOLLOW RANDOM
        try:
            print("\n--- X FOLLOW RANDOM ---")
            follow_x_random(count=5)
        except Exception as e:
            print(f"[X Follow] errore: {e}")

        # 3. REDDIT
        try:
            print("\n--- REDDIT ---")
            spam_reddit_free(
                subreddits=random.sample(REDDIT_SUB_POOL, k=min(2, len(REDDIT_SUB_POOL))),
                title="Nuova community + bot",
                body=PROMO_TEXT,
            )
        except Exception as e:
            print(f"[Reddit] errore: {e}")

        # 4. DISCORD
        try:
            print("\n--- DISCORD ---")
            spam_discord()
        except Exception as e:
            print(f"[Discord] errore: {e}")

        # 5. FACEBOOK POST
        try:
            print("\n--- FACEBOOK ---")
            spam_facebook_free(count=1)
        except Exception as e:
            print(f"[Facebook] errore: {e}")

        # 5b. FACEBOOK FOLLOW RANDOM
        try:
            print("\n--- FB FOLLOW RANDOM ---")
            follow_facebook_random(count=3)
        except Exception as e:
            print(f"[FB Follow] errore: {e}")

        # 6. INSTAGRAM POST
        try:
            print("\n--- INSTAGRAM ---")
            spam_instagram(count=1)
        except Exception as e:
            print(f"[Instagram] errore: {e}")

        # 6b. INSTAGRAM FOLLOW RANDOM
        try:
            print("\n--- IG FOLLOW RANDOM ---")
            follow_instagram_random(count=5)
        except Exception as e:
            print(f"[IG Follow] errore: {e}")

        # 7. TIKTOK POST
        try:
            print("\n--- TIKTOK ---")
            spam_tiktok_free(video_path="promo.mp4", count=1)
        except Exception as e:
            print(f"[TikTok] errore: {e}")

        # 7b. TIKTOK FOLLOW RANDOM
        try:
            print("\n--- TT FOLLOW RANDOM ---")
            follow_tiktok_random(count=3)
        except Exception as e:
            print(f"[TT Follow] errore: {e}")

        print(f"\n=== Fine ciclo {ciclo} ===")
        print("Aspetto 15 minuti...\n")
        ciclo += 1
        time.sleep(900)
