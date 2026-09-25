import os
import yt_dlp

DOWNLOAD_DIR = "Downloads"


def create_metadata(info, url, path):
    channel = info.get("uploader") or info.get("channel") or "Unknown"
    platform = info.get("extractor_key") or "Unknown"
    description = info.get("description") or "No description"

    text = f"""📺 Channel Name: {channel}
🌐 Platform: {platform}
🔗 Source Link: {url}

💬 Video Description:
{description}
"""

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def download_media(url, download_video=True, download_thumbnail=True, create_text=True):
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    opts = {
        "outtmpl": os.path.join(DOWNLOAD_DIR, "%(uploader)s_%(title)s_%(id)s.%(ext)s"),
        "format": "bestvideo*+bestaudio/best" if download_video else "best",
        "merge_output_format": "mp4",
        "ignoreerrors": True,
    }

    if download_thumbnail:
        opts["writethumbnail"] = True

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=download_video)

        if info and create_text:
            filename = os.path.join(
                DOWNLOAD_DIR,
                f"{info.get('title','media')}_metadata.txt"
            )
            create_metadata(info, url, filename)

    return True
