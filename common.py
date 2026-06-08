import os
import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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
# Email configuration
# ===============================
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
FROM_EMAIL = os.environ["EMAIL_ADDRESS"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
TO_EMAIL = "bogdan.khimych@gmail.com"

if not FROM_EMAIL or not EMAIL_PASSWORD:
    raise RuntimeError("EMAIL_ADDRESS and EMAIL_PASSWORD environment variables not set")

HEADERS = {'User-Agent': 'Mozilla/5.0'}
BASE_URL = "https://tennistowerhamlets.com"


def send_email(subject, body):
    """Send email via SMTP"""
    try:
        msg = MIMEMultipart()
        msg["From"] = FROM_EMAIL
        msg["To"] = TO_EMAIL
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html"))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(FROM_EMAIL, EMAIL_PASSWORD)
            server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print("SMTP error:", e)


def extract_day_name(day_text: str) -> str | None:
    """
    Extract day name from text like 'Tue 12 Jun' or 'Tuesday, June 12'
    Returns abbreviated day name like 'Tue' or None
    """
    days_abbr = {"Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"}
    
    # Try abbreviated first
    for day in days_abbr:
        if day in day_text:
            return day
    
    # Try full names and convert to abbreviated
    day_map = {
        "Monday": "Mon", "Tuesday": "Tue", "Wednesday": "Wed",
        "Thursday": "Thu", "Friday": "Fri", "Saturday": "Sat", "Sunday": "Sun"
    }
    for full, abbr in day_map.items():
        if full in day_text:
            return abbr
    
    return None
