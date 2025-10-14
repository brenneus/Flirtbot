import os
import re
import requests
from bs4 import BeautifulSoup

# Scrape the transcript from the given URL and extract clean text

# This was created based off of the love is blind transcripts at:
# https://tvshowtranscripts.ourboard.org/viewforum.php?f=1243
def extract_text_from_html_url(url: str) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/113.0.0.0 Safari/537.36"
        )
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    post = soup.find("div", class_="postbody")
    texts = []
    paras = post.find_all("p", recursive=False)
    for p in paras:
        for s in p.find_all("strong"):
            s.decompose()

        txt = p.get_text()

        txt = re.sub(r'\([^)]*\)', '', txt)
        txt = re.sub(r'[^\x00-\x7F]+', '', txt)
        txt = txt.replace(':', '')
        txt = ' '.join(txt.strip().split())

        if txt:
            texts.append(txt)

    return " ".join(texts)

# creates one transcript per episode and stores it in texts
# to use, change the URL and name to the episode you want to scrape
if __name__ == "__main__":
    url = "https://tvshowtranscripts.ourboard.org/viewtopic.php?f=1243&t=51199"
    text = extract_text_from_html_url(url)

    os.makedirs("texts", exist_ok=True)
    # change this as desired
    name = "S1E11.txt"
    out_path = os.path.join("texts", name)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Saved scraped transcript to {out_path}")