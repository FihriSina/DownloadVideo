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
        download_dir = Path.home() / "Downloads"

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

    path.write_text(text, encoding="utf-8")


def get_safe_folder_name(info):
    """
    Her yapıştırılan link için güvenli ve mümkün olduğunca benzersiz
    bir klasör adı üretir.
    """
    title = info.get("title") or info.get("id") or "media"
    media_id = info.get("id") or ""

    raw_name = f"{title} [{media_id}]" if media_id else title
    folder_name = sanitize_filename(raw_name, restricted=False).strip()

    return folder_name or "media"


def get_unique_folder(base_dir, folder_name):
    """
    Aynı isimde klasör zaten varsa üzerine yazmak yerine
    ' (2)', ' (3)' ... ekleyerek yeni klasör oluşturur.
    """
    folder = base_dir / folder_name

    if not folder.exists():
        folder.mkdir(parents=True, exist_ok=False)
        return folder

    counter = 2
    while True:
        candidate = base_dir / f"{folder_name} ({counter})"
        if not candidate.exists():
            candidate.mkdir(parents=True, exist_ok=False)
            return candidate
        counter += 1


def download_media(
    url,
    download_video=True,
    download_thumbnail=True,
    create_text=True,
):
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

    # Önce medya bilgisini alıyoruz. Böylece bu linke özel
    # klasörü indirme başlamadan önce oluşturabiliyoruz.
    probe_opts = {
        "quiet": True,
        "no_warnings": True,
        "ignoreerrors": False,
    }

    with yt_dlp.YoutubeDL(probe_opts) as probe_ydl:
        info = probe_ydl.extract_info(url, download=False)

    if not info:
        raise RuntimeError("Media information could not be retrieved.")

    folder_name = get_safe_folder_name(info)
    media_folder = get_unique_folder(DOWNLOAD_DIR, folder_name)

    # Her linkin bütün çıktıları yalnızca kendi klasörüne gider.
    output_template = str(
        media_folder / "%(uploader)s_%(title)s_%(id)s.%(ext)s"
    )

    opts = {
        "outtmpl": output_template,
        "format": "bestvideo*+bestaudio/best",
        "merge_output_format": "mp4",
        "ignoreerrors": True,
    }

    if download_thumbnail:
        opts["writethumbnail"] = True

    # Video seçili değilse video dosyasını indirme; ancak thumbnail
    # gibi yan dosyaların indirilebilmesi için yt-dlp yine çalışsın.
    if not download_video:
        opts["skip_download"] = True

    # Video veya thumbnail isteniyorsa yt-dlp indirme işlemini çalıştır.
    if download_video or download_thumbnail:
        with yt_dlp.YoutubeDL(opts) as ydl:
            downloaded_info = ydl.extract_info(url, download=True)

            # İndirme sırasında dönen daha güncel bilgi varsa onu kullan.
            if downloaded_info:
                info = downloaded_info

    if create_text:
        title = info.get("title") or info.get("id") or "media"
        safe_title = sanitize_filename(title, restricted=False).strip() or "media"
        metadata_path = media_folder / f"{safe_title}_metadata.txt"
        create_metadata(info, url, metadata_path)

    return True
