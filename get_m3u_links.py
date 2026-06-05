import requests
import json
import base64
import os
from datetime import datetime, timezone, timedelta

TZ_VN = timezone(timedelta(hours=7))

# ====== CẤU HÌNH GITHUB ======
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "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")
REPO_NAME    = "Vipdt5k49/linh_tinh"
FILE_PATH    = "xaycontv.m3u"
BRANCH       = "main"

# ====== CẤU HÌNH M3U ======
M3U_REFERRER   = "https://sv2.xaycon.live/"
M3U_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"


# ------------------------------------------------------------------
# 1. Lấy danh sách fixture từ API
# ------------------------------------------------------------------
def fetch_fixtures():
    url = "https://sv.xaycontv.xyz/api/v1/external/fixtures/unfinished"
    headers = {
        "authority": "sv.xaycontv.xyz",
        "accept": "application/json, text/plain, */*",
        "accept-language": "vi-VN,vi;q=0.9,en-GB;q=0.8,en;q=0.7,fr-FR;q=0.6,fr;q=0.5,en-US;q=0.4",
        "origin": "https://sv2.xaycon3.live",
        "referer": "https://sv2.xaycon3.live/",
        "sec-ch-ua": '"Chromium";v="139", "Not;A=Brand";v="99"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()


# ------------------------------------------------------------------
# 2. Trích xuất từng stream trong fixtureCommentators
# ------------------------------------------------------------------
def parse_start_time(raw: str) -> str:
    try:
        dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        dt_vn = dt.astimezone(TZ_VN)
        return dt_vn.strftime("%H:%M %d/%m/%Y")
    except Exception:
        return raw


def parse_entries(data):
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        for key in ("data", "fixtures", "results", "items"):
            if key in data and isinstance(data[key], list):
                items = data[key]
                break
        else:
            items = [data]
    else:
        items = []

    entries = []
    for item in items:
        if not isinstance(item, dict):
            continue

        match_title = item.get("title", "Unknown").strip()
        start_time  = parse_start_time(item.get("startTime", ""))

        for fc in item.get("fixtureCommentators", []):
            commentator = fc.get("commentator", {})
            nickname = (
                commentator.get("nickname") or
                commentator.get("name") or
                commentator.get("username") or
                "Unknown"
            )

            for stream in commentator.get("streams", []):
                quality = stream.get("name", "")
                url     = stream.get("sourceUrl", "")
                if not url or quality.upper() != "FHD":
                    continue
                title = f"{start_time} | {match_title} | {nickname} | {quality}"
                entries.append({"title": title, "url": url})

    return entries


# ------------------------------------------------------------------
# 3. Tạo nội dung file .m3u
# ------------------------------------------------------------------
def build_m3u(entries):
    lines = ["#EXTM3U"]
    for entry in entries:
        lines.append(f"#EXTVLCOPT:http-referrer={M3U_REFERRER}")
        lines.append(f"#EXTVLCOPT:http-user-agent={M3U_USER_AGENT}")
        lines.append(f"#EXTINF:-1 , {entry['title']}")
        lines.append(entry["url"])
        lines.append("")
    return "\n".join(lines)


# ------------------------------------------------------------------
# 4. Upload lên GitHub
# ------------------------------------------------------------------
def upload_to_github(content: str):
    api_url = f"https://api.github.com/repos/{REPO_NAME}/contents/{FILE_PATH}"
    gh_headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
    }

    sha = None
    check = requests.get(api_url, headers=gh_headers, params={"ref": BRANCH})
    if check.status_code == 200:
        sha = check.json().get("sha")
        print(f"File đã tồn tại, sẽ cập nhật (sha={sha[:7]}...)")
    elif check.status_code == 404:
        print("File chưa tồn tại, sẽ tạo mới.")
    else:
        check.raise_for_status()

    payload = {
        "message": f"Update xaycontv.m3u via script [{datetime.now(TZ_VN).strftime('%H:%M %d/%m/%Y')}]",
        "content": base64.b64encode(content.encode("utf-8")).decode("utf-8"),
        "branch": BRANCH,
    }
    if sha:
        payload["sha"] = sha

    resp = requests.put(api_url, headers=gh_headers, json=payload)
    resp.raise_for_status()
    info = resp.json()
    print(f"✅ Upload thành công: {info['content']['html_url']}")
    return info["content"]["html_url"]


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------
def main():
    print("📡 Đang lấy dữ liệu từ API...")
    data = fetch_fixtures()

    entries = parse_entries(data)
    print(f"🔗 Tìm thấy {len(entries)} stream:")
    for i, e in enumerate(entries, 1):
        print(f"  {i}. [{e['title']}]\n     {e['url']}")

    if not entries:
        print("⚠️  Không tìm thấy stream nào.")
        return

    m3u_content = build_m3u(entries)

    print("\n☁️  Đang upload lên GitHub...")
    upload_to_github(m3u_content)


if __name__ == "__main__":
    main()
