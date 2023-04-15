from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/waybackurls", methods=["POST"])
def waybackurls():
    url = request.form["url"]
    archived_pages = get_archived_pages(url)
    urls = get_wayback_urls(archived_pages)
    return render_template("waybackurls.html", urls=urls)

def get_archived_pages(url):
    api_url = f"https://web.archive.org/cdx/search/cdx?url={url}&output=json"
    response = requests.get(api_url)
    if response.status_code == 200:
        archived_pages = [row[2] for row in response.json()[1:]]
        return archived_pages
    else:
        return []

def get_wayback_urls(archived_pages):
    urls = []
    for page in archived_pages:
        response = requests.get(page)
        if response.status_code == 200:
            page_urls = extract_urls(response.content)
            urls.extend(page_urls)
    return urls

def extract_urls(html):
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a")
    urls = [link.get("href") for link in links]
    return urls

if __name__ == "__main__":
    app.run(debug=True)
