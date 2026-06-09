import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from urllib.parse import urljoin
from common import HEADERS, BASE_URL, send_email, extract_day_name
from state_tracker import has_changes, save_state, get_changes_summary
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
        (weekday in ["Mon","Tue","Wed","Thu","Fri"] and hour >= 18) or weekday == "Sun"
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
# Main
# ===============================
if __name__ == "__main__":
    classes = find_beginner_not_sold_classes()
    
    # Check if there are changes compared to previous state
    if has_changes("coaching", classes):
        changes = get_changes_summary("coaching", classes)
        print(f"Changes detected! Total: {changes['total']}")
        print(f"  New: {len(changes['new'])}")
        print(f"  Removed: {len(changes['removed'])}")
        
        if classes:
            print("Available beginner classes:")
            for c in classes:
                print("-", c)
            
            # Build email body with change summary
            body = "<h2>Beginner Tennis Classes - Status Update</h2>"
            
            if changes['new']:
                body += "<h3>🆕 New Classes Available</h3><ul>"
                for item in changes['new']:
                    body += f"<li>{item}</li>"
                body += "</ul>"
            
            if changes['unchanged']:
                body += f"<h3>Still Available</h3><p>{len(changes['unchanged'])} sessions still available</p>"
            
            send_email("Beginner Tennis Classes - Availability Update!", body)
        else:
            send_email("Beginner Tennis Classes - All Booked Out!", 
                      "<p>All beginner classes are now fully booked.</p>")
        
        # Save new state
        save_state("coaching", classes)
    else:
        print("No changes in coaching availability")
