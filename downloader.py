# import yt_dlp
# import os
# import time

# def clean_url(url):
#     return url.split("?")[0]

# def detect_platform(url):
#     if "youtube.com" in url or "youtu.be" in url:
#         return "youtube"
#     elif "instagram.com" in url:
#         return "instagram"
#     elif "facebook.com" in url or "fb.watch" in url:
#         return "facebook"
#     return "other"

# def download_media(url, output_path="downloads", audio_only=False):
#     try:
#         os.makedirs(output_path, exist_ok=True)

#         url = clean_url(url)
#         platform = detect_platform(url)

#         ydl_opts = {
#             'outtmpl': f'{output_path}/%(title)s_%(id)s.%(ext)s',
#             'quiet': True,
#         }

#         if platform == "youtube":
#             if audio_only:
#                 ydl_opts['format'] = 'bestaudio'
#             else:
#                 ydl_opts['format'] = 'bestvideo+bestaudio/best'
#                 ydl_opts['merge_output_format'] = 'mp4'
#         else:
#             ydl_opts['format'] = 'best'

#         if os.path.exists("cookies.txt"):
#             ydl_opts['cookiefile'] = "cookies.txt"

#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             info = ydl.extract_info(url, download=True)
#             filename = ydl.prepare_filename(info)

#         return {
#             "status": "success",
#             "file": filename,
#             "platform": platform
#         }

#     except Exception as e:
#         return {"status": "error", "message": str(e)}














# import yt_dlp
# import os
# import time

# def clean_url(url: str) -> str:
#     return url.split("?")[0]

# def detect_platform(url: str) -> str:
#     u = url.lower()
#     if "youtube.com" in u or "youtu.be" in u:
#         return "YouTube"
#     if "instagram.com" in u:
#         return "Instagram"
#     if "facebook.com" in u or "fb.watch" in u:
#         return "Facebook"
#     return "Other"

# def _friendly_reason(e: Exception) -> str:
#     msg = str(e).lower()
#     if "private" in msg or "login" in msg:
#         return "🔒 Private or login required"
#     if "not available" in msg or "does not exist" in msg:
#         return "🚫 Video not available"
#     if "unsupported" in msg:
#         return "⚠️ Unsupported link"
#     if "403" in msg or "forbidden" in msg:
#         return "🚫 Access blocked by platform"
#     return "⚠️ Unable to download"

# def download_media(url, output_path="downloads", audio_only=False):
#     try:
#         os.makedirs(output_path, exist_ok=True)

#         url = clean_url(url)
#         platform = detect_platform(url)

#         # 🔥 Cloud-safe: avoid ffmpeg dependency
#         ydl_opts = {
#             "outtmpl": f"{output_path}/%(title)s_%(id)s.%(ext)s",
#             "quiet": True,
#             "format": "best",          # ← key for Streamlit Cloud
#             "retries": 2,
#             "fragment_retries": 2,
#             "noplaylist": False,
#         }

#         # Best-effort audio-only (works on many YT links; no ffmpeg merge)
#         if audio_only and platform == "YouTube":
#             ydl_opts["format"] = "bestaudio/best"

#         # Optional cookies (won’t usually be used on cloud)
#         if os.path.exists("cookies.txt"):
#             ydl_opts["cookiefile"] = "cookies.txt"

#         # Simple retry loop
#         for _ in range(2):
#             try:
#                 with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                     info = ydl.extract_info(url, download=True)
#                     filename = ydl.prepare_filename(info)
#                 return {
#                     "status": "success",
#                     "file": filename,
#                     "platform": platform,
#                 }
#             except Exception:
#                 time.sleep(1.5)

#         raise Exception("download failed after retry")

#     except Exception as e:
#         return {
#             "status": "error",
#             "message": _friendly_reason(e),
#         }



import yt_dlp
import os
import time


# -------------------------------
# Clean URL
# -------------------------------
def clean_url(url: str) -> str:
    return url.split("?")[0]


# -------------------------------
# Detect Platform
# -------------------------------
def detect_platform(url: str) -> str:

    u = url.lower()

    if "youtube.com" in u or "youtu.be" in u:
        return "YouTube"

    if "instagram.com" in u:
        return "Instagram"

    if "facebook.com" in u or "fb.watch" in u:
        return "Facebook"

    return "Other"


# -------------------------------
# Friendly Error Messages
# -------------------------------
def _friendly_reason(e: Exception) -> str:

    msg = str(e).lower()

    if "private" in msg or "login" in msg:
        return "🔒 Private or login required"

    if "not available" in msg or "does not exist" in msg:
        return "🚫 Video not available"

    if "unsupported" in msg:
        return "⚠️ Unsupported link"

    if "403" in msg or "forbidden" in msg:
        return "🚫 Access blocked by platform"

    if "timed out" in msg:
        return "⏳ Request timed out"

    return "⚠️ Unable to download"


# -------------------------------
# Main Download Function
# -------------------------------
def download_media(url, output_path="/tmp/downloads", audio_only=False):

    try:

        # Create folder
        os.makedirs(output_path, exist_ok=True)

        # Clean URL
        url = clean_url(url)

        # Detect platform
        platform = detect_platform(url)

        # -------------------------------
        # yt-dlp options
        # -------------------------------
        ydl_opts = {

            # Safe filename
            "outtmpl": f"{output_path}/%(title).80s_%(id)s.%(ext)s",

            # Quiet logs
            "quiet": True,

            # Cloud-safe format
            "format": "best",

            # Retry system
            "retries": 2,
            "fragment_retries": 2,

            # SSL fix
            "nocheckcertificate": True,

            # Timeout fix
            "socket_timeout": 15,

            # Avoid playlist issues
            "noplaylist": True,
        }

        # -------------------------------
        # Audio-only mode
        # -------------------------------
        if audio_only and platform == "YouTube":
            ydl_opts["format"] = "bestaudio/best"

        # -------------------------------
        # Optional cookies
        # -------------------------------
        if os.path.exists("cookies.txt"):
            ydl_opts["cookiefile"] = "cookies.txt"

        # -------------------------------
        # Retry loop
        # -------------------------------
        for _ in range(2):

            try:

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:

                    info = ydl.extract_info(url, download=True)

                    filename = ydl.prepare_filename(info)

                return {
                    "status": "success",
                    "file": filename,
                    "platform": platform,
                }

            except Exception:
                time.sleep(2)

        raise Exception("download failed after retry")

    except Exception as e:

        return {
            "status": "error",
            "message": _friendly_reason(e),
        }