import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from urllib.parse import urljoin
from common import HEADERS, BASE_URL, send_email, extract_day_name
COURTS_URL = "https://tennistowerhamlets.com/book/courts/poplar-rec-ground"

# Interested days and times
INTERESTED_DAYS = {"Mon", "Tue", "Thu", "Fri", "Sat", "Sun"}
INTERESTED_TIMES = {7, 11, 19, 20, 21}  # 7pm, 8pm, 9pm (24-hour format)

# ===============================
# Scraper helpers
# ===============================
def _parse_hour(time_str: str) -> int | None:
    """Parse time string like '7:00pm' to hour (19 for 7pm)"""
    try:
        return datetime.strptime(time_str.strip(), "%I:%M%p").hour
    except ValueError:
        return None

def _get_day_links() -> list[tuple[str, str]]:
    """
    Fetch the main courts page and extract day links from the day picker.
    Returns list of tuples (day_name, day_url)
    """
    res = requests.get(COURTS_URL, headers=HEADERS, verify=False)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    
    day_links = []
    
    # Try to find day picker container (different possible selectors)
    day_picker = soup.find("div", class_="day-picker")
    if not day_picker:
        # Alternative: look for nav with day links
        day_picker = soup.find("nav", class_=re.compile(r"day|pick|date", re.I))
    
    if not day_picker:
        # If no specific container, look for links near the main heading or in the page
        # The links appear to be near the page title with format like "Today", "Tomorrow", "Wed", etc.
        # We'll extract all links that point to the same base URL with date parameters
        pattern = re.compile(r"poplar-rec-ground/\d{4}-\d{2}-\d{2}")
        all_links = soup.find_all("a", href=pattern)
        
        for link in all_links:
            href = link.get("href")
            day_text = link.get_text(strip=True)
            if href:
                full_url = urljoin(BASE_URL, href)
                day_links.append((day_text, full_url))
        
        return day_links
    
    # If we found a day picker container, get links from it
    for link in day_picker.find_all("a"):
        href = link.get("href")
        day_text = link.get_text(strip=True)
        if href:
            full_url = urljoin(BASE_URL, href)
            day_links.append((day_text, full_url))
    
    return day_links

def _check_court_availability(day_url: str, day_name: str) -> list[dict]:
    """
    Check a specific day's page for available courts at interested times.
    Returns list of dicts with 'slot', 'url' keys.
    """
    res = requests.get(day_url, headers=HEADERS, verify=False)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    
    available_slots = []
    
    # Find the booking table
    table = soup.find("table")
    if not table:
        print(f"  No booking table found for {day_name}")
        return []
    
    # Process each row in the table
    rows = table.find_all("tr")
    for row in rows:
        # Get the time from the <th> header
        th = row.find("th")
        if not th:
            continue
        
        time_cell = th.get_text(strip=True)
        
        # Look for time in format like "7am", "8pm", etc.
        time_match = re.search(r"(\d{1,2})\s*(am|pm)", time_cell, re.I)
        if not time_match:
            continue
        
        hour = int(time_match.group(1))
        ampm = time_match.group(2).lower()
        
        # Convert to 24-hour format
        if ampm == "pm" and hour != 12:
            hour += 12
        elif ampm == "am" and hour == 12:
            hour = 0
        
        # Check if this is a time we're interested in
        if hour not in INTERESTED_TIMES:
            continue
        
        # Get the court data from <td>
        td = row.find("td")
        if not td:
            continue
        
        cell_text = td.get_text(strip=True).lower()
        
        # If the cell doesn't contain "booked" for all courts, there's availability
        # The td contains something like "Court 1£5Court 2booked" or "Court 1bookedCourt 2booked"
        # If we see a price (£) or no "booked" after a court, it's available
        has_available = "booked" not in cell_text or "£" in cell_text
        
        if has_available:
            available_slots.append({
                "slot": f"{day_name} at {hour:02d}:00",
                "url": day_url
            })
    
    return available_slots

def find_available_courts() -> list[dict]:
    """
    Find all available courts at interested times.
    Returns list of dicts with 'slot', 'url' keys.
    """
    print("Fetching day links from main courts page...")
    day_links = _get_day_links()
    
    if not day_links:
        print("No day links found")
        return []
    
    all_available = []
    
    for day_text, day_url in day_links:
        day_name = extract_day_name(day_text)
        
        # Check if this is a day we're interested in
        if not day_name or day_name not in INTERESTED_DAYS:
            continue
        
        print(f"Checking {day_name}...")
        available = _check_court_availability(day_url, day_name)
        all_available.extend(available)
    
    return all_available

# ===============================
# Main
# ===============================
if __name__ == "__main__":
    available_courts = find_available_courts()
    
    if not available_courts:
        print("No available courts at interested times")
    else:
        print("Available courts found:")
        for item in available_courts:
            print("-", item["slot"])
        
        body = "<h2>Available Courts at Poplar Rec Ground</h2>"
        body += "<ul>"
        for item in available_courts:
            body += f"<li><a href='{item['url']}'>{item['slot']}</a></li>"
        body += "</ul>"
        
        send_email("Tennis Courts Available!", body)
