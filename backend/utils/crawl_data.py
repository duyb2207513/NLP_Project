import requests
from bs4 import BeautifulSoup
import re

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Linux)'})

def preprocessText(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    return ' '.join(text.split())


def extract_main_text(link, min_length=150):
    try:
        print("Hello tôi đang cào dữ liệu nè")
        resp = session.get(link, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, 'lxml')
        paragraphs = soup.find_all('p')
        main_text = ' '.join(p.get_text(strip=True) for p in paragraphs)
        print(main_text)
        return preprocessText(main_text) if len(main_text) >= min_length else ''
    except Exception as e:
        print(f"[!] Lỗi link {link}: {e}")
        return ''
    