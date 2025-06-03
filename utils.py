def extract_video_id(url_or_id):
    if "youtube.com" in url_or_id or "youtu.be" in url_or_id:
        import re
        match = re.search(r"(?:v=|/)([\w-]{11})", url_or_id)
        return match.group(1) if match else url_or_id
    return url_or_id