from pathlib import Path

import yt_dlp
from PyQt6.QtCore import QStandardPaths
from yt_dlp.utils import sanitize_filename


def get_download_dir():
    """
    Windows/macOS/Linux sisteminde kullanıcının gerçek
    Downloads / İndirilenler klasörünü bulur.
    """

    download_location = QStandardPaths.writableLocation(
        QStandardPaths.StandardLocation.DownloadLocation
    )

    if download_location:
        download_dir = Path(download_location)
    else:
        # QStandardPaths herhangi bir nedenle yol döndüremezse
        # kullanıcının ana klasöründeki Downloads klasörünü kullan.
        download_dir = Path.home() / "Downloads"

    # Klasör mevcut değilse oluştur.
    download_dir.mkdir(parents=True, exist_ok=True)

    return download_dir


DOWNLOAD_DIR = get_download_dir()


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


def download_media(
    url,
    download_video=True,
    download_thumbnail=True,
    create_text=True
):
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

    opts = {
        "outtmpl": str(
            DOWNLOAD_DIR / "%(uploader)s_%(title)s_%(id)s.%(ext)s"
        ),
        "format": (
            "bestvideo*+bestaudio/best"
            if download_video
            else "best"
        ),
        "merge_output_format": "mp4",
        "ignoreerrors": True,
    }

    if download_thumbnail:
        opts["writethumbnail"] = True

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(
            url,
            download=download_video
        )

        if info and create_text:
            title = info.get("title") or "media"

            # Windows'ta dosya adında kullanılamayan
            # :, ?, *, /, \ vb. karakterleri temizler.
            safe_title = sanitize_filename(
                title,
                restricted=False
            )

            metadata_path = (
                DOWNLOAD_DIR / f"{safe_title}_metadata.txt"
            )

            create_metadata(
                info,
                url,
                metadata_path
            )

    return True