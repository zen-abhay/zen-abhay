import sys
import json
import requests
from bs4 import BeautifulSoup

def fetch_contributions(username):
    print(f"Fetching contribution data for {username}...")
    url = f"https://github.com/users/{username}/contributions"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: Failed to fetch data. Status code: {response.status_code}")
        sys.exit(1)
        
    soup = BeautifulSoup(response.text, "html.parser")
    days = []
    
    # Extract each contribution cell from GitHub's calendar
    for cell in soup.find_all("td", class_="ContributionCalendar-day"):
        date = cell.get("data-date")
        level = cell.get("data-level", "0")
        if date:
            days.append({"date": date, "level": int(level)})
            
    data = {"username": username, "days": days}
    
    # Save output to data/contributions.json
    with open("data/contributions.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        
    print(f"Success! Saved {len(days)} days of contribution data to data/contributions.json")

if __name__ == "__main__":
    fetch_contributions("zen-abhay")
    