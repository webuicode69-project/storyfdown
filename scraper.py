import cloudscraper
import re

scraper = cloudscraper.create_scraper(browser='chrome')

API_URL = "https://fbdown.to/api/ajaxSearch"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Origin": "https://fbdown.to",
    "Referer": "https://fbdown.to/",
    "X-Requested-With": "XMLHttpRequest"
}

def get_video_url(url):
    try:
        data = {
            "q": url,
            "p": "home",
            "lang": "en",
            "v": "v2",
            "w": ""
        }

        res = scraper.post(API_URL, data=data, headers=HEADERS)
        result = res.json()

        print("API:", result)

        html = result.get("data", "")

        links = re.findall(r'href="(https://dl\.snapcdn\.app/download\?token=.*?)"', html)

        if links:
            return {
                "sd": links[0] if len(links) > 0 else None,
                "hd": links[1] if len(links) > 1 else None
            }

        return None

    except Exception as e:
        print("ERROR:", e)
        return None