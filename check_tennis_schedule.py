import os
import ssl
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from urllib.parse import urljoin
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

# ===============================
# Load environment variables from .env
# ===============================
load_dotenv()
# ===============================
# SSL fix for macOS venv testing
# ===============================
ssl._create_default_https_context = ssl._create_unverified_context

# ===============================
# Config
# ===============================
SENDGRID_API_KEY = os.environ["SENDGRID_API_KEY"]
if not SENDGRID_API_KEY:
    raise RuntimeError("SENDGRID_API_KEY secret not set")

FROM_EMAIL = "exsabot@outlook.com"
TO_EMAIL = "bogdan.khimych@gmail.com"
HEADERS = {'User-Agent': 'Mozilla/5.0'}
BASE_URL = "https://tennistowerhamlets.com"
URL = "https://tennistowerhamlets.com/coaching?filter_venue=&filter_age_groups%5B%5D=5&filter_from=2026-01-04&filter_to="

# ===============================
# Scraper helpers
# ===============================
def _parse_hour(time_str: str) -> int | None:
    try:
        return datetime.strptime(time_str.strip(), "%I:%M%p").hour
    except ValueError:
        return None

def _extract_weekday_and_start(time_text: str) -> tuple[str, int] | None:
    match = re.search(
        r"(Mon|Tue|Wed|Thu|Fri|Sat|Sun).*?\|\s*(\d{1,2}:\d{2}[ap]m)–(\d{1,2}:\d{2}[ap]m)",
        time_text,
        re.DOTALL
    )
    if not match:
        return None
    weekday = match.group(1)
    start_time = match.group(2)
    hour = _parse_hour(start_time)
    return weekday, hour

def _get_booking_url(card) -> str | None:
    button = card.select_one("div.controls form button.primary")
    if button and "Book now" in button.get_text(strip=True):
        form = card.select_one("div.controls form")
        if form and form.has_attr("action"):
            return urljoin(BASE_URL, form["action"])
    return None

def _is_class_eligible(title: str, weekday: str, hour: int) -> bool:
    return ("Beginner" in title) and (
        (weekday in ["Mon","Tue","Wed","Thu","Fri"] and hour >= 10) or weekday == "Sun"
    )

def _has_sufficient_spaces(booking_url: str, needed) -> bool:
    res = requests.get(booking_url, headers=HEADERS, verify=False)  # SSL bypass
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    cards = soup.find_all("div", class_="session available")
    for card in cards:
        cost_tag = card.find("label").find(class_="cost")
        cost_text = cost_tag.get_text(strip=True)
        m = re.search(r"(\d+)\sspaces", cost_text)
        if m and int(m.group(1)) >= needed:
            return True
    return False

def find_beginner_not_sold_classes(min_spaces: int = 2) -> list[str]:
    res = requests.get(URL, headers=HEADERS, verify=False)  # SSL bypass
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    cards = soup.find_all("div", class_="programme")
    results = []

    for card in cards:
        heading_tag = card.find(class_="heading")
        time_tag = card.find(class_="time")
        if not heading_tag or not time_tag:
            continue
        title = heading_tag.get_text(strip=True)
        weekday_hour = _extract_weekday_and_start(time_tag.get_text(" ", strip=True))
        if not weekday_hour:
            continue
        weekday, hour = weekday_hour
        if not _is_class_eligible(title, weekday, hour):
            continue
        booking_url = _get_booking_url(card)
        if not booking_url:
            continue
        if not _has_sufficient_spaces(booking_url, min_spaces):
            continue
        results.append(f"{title} — {weekday} @ {hour}:00 — {booking_url}")
    return results

# ===============================
# Email sender via SendGrid
# ===============================
def send_email(subject, body):
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=TO_EMAIL,
        subject=subject,
        html_content=body
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print("Email sent! Status:", response.status_code)
    except Exception as e:
        print("SendGrid error:", e)

# ===============================
# Main
# ===============================
if __name__ == "__main__":
    classes = find_beginner_not_sold_classes()
    if not classes:
        print("No available beginner classes")
    else:
        print("Available beginner classes:")
        for c in classes:
            print("-", c)
        body = "<br>".join(classes)
        send_email("Beginner Tennis Classes Available!", body)
