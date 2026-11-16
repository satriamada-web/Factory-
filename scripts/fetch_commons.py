import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = "FACTORYVideoBot/0.1 (GitHub Actions; educational video workflow)"

def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=45) as response:
        return json.loads(response.read().decode("utf-8"))

def allowed_license(name):
    value = (name or "").strip().lower()
    if "non-commercial" in value or "noncommercial" in value or "nc" in value.split():
        return False
    if "no derivatives" in value or "no-derivatives" in value or "nd" in value.split():
        return False
    return (
        value.startswith("cc0")
        or "public domain" in value
        or value.startswith("cc by ")
        or value.startswith("cc by-sa ")
    )

def download(url, destination):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as response:
        destination.write_bytes(response.read())

def main():
    data = json.loads(Path("input/scenes.json").read_text(encoding="utf-8"))
    scenes = data.get("scenes", [])
    if not scenes:
        raise SystemExit("input/scenes.json tidak berisi adegan.")

    Path("output/visuals").mkdir(parents=True, exist_ok=True)
    credits = []

    for index, scene in enumerate(scenes, start=1):
        query = str(scene.get("query", "")).strip()
        if not query:
            raise SystemExit(f"Query visual adegan {index} kosong.")

        params = {
            "action": "query",
            "format": "json",
            "generator": "search",
            "gsrsearch": query,
            "gsrnamespace": 6,
            "gsrlimit": 15,
            "prop": "imageinfo",
            "iiprop": "url|extmetadata",
            "iiurlwidth": 1920,
        }
        url = API + "?" + urllib.parse.urlencode(params)
        payload = fetch_json(url)
        pages = (payload.get("query") or {}).get("pages") or {}
        candidates = sorted(pages.values(), key=lambda p: p.get("title", ""))

        chosen = None
        for page in candidates:
            info_list = page.get("imageinfo") or []
            if not info_list:
                continue
            info = info_list[0]
            meta = info.get("extmetadata") or {}
            license_name = meta.get("LicenseShortName", {}).get("value", "")
            if not allowed_license(license_name):
                continue
            image_url = info.get("thumburl") or info.get("url")
            if image_url:
                chosen = (page, info, meta, license_name, image_url)
                break

        if not chosen:
            raise SystemExit(
                f"Tidak ditemukan gambar berlisensi CC BY/CC BY-SA/CC0/Public Domain untuk query: {query}"
            )

        page, info, meta, license_name, image_url = chosen
        output = Path(f"output/visuals/scene_{index:02d}.jpg")
        download(image_url, output)

        title = page.get("title", "Untitled")
        description = meta.get("ImageDescription", {}).get("value", "")
        artist = meta.get("Artist", {}).get("value", "Unknown author")
        credit = meta.get("Credit", {}).get("value", "")
        license_url = meta.get("LicenseUrl", {}).get("value", "")
        source_page = info.get("descriptionurl", "")

        credits.append(
            f"Scene {index}\n"
            f"Search query: {query}\n"
            f"File: {title}\n"
            f"Author: {artist}\n"
            f"Credit: {credit}\n"
            f"License: {license_name}\n"
            f"License URL: {license_url}\n"
            f"Source page: {source_page}\n"
            f"Description: {description}\n"
        )
        print(f"Scene {index}: downloaded {title} ({license_name})")
        time.sleep(1)

    Path("output/attribution.txt").write_text(
        "\n---\n".join(credits), encoding="utf-8"
    )

if __name__ == "__main__":
    main()
