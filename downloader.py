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

















import yt_dlp
import os
import time

def clean_url(url):
    return url.split("?")[0]

def detect_platform(url):
    if "youtube.com" in url or "youtu.be" in url:
        return "YouTube"
    elif "instagram.com" in url:
        return "Instagram"
    elif "facebook.com" in url or "fb.watch" in url:
        return "Facebook"
    return "Other"

def download_media(url, output_path="downloads", audio_only=False):
    try:
        os.makedirs(output_path, exist_ok=True)

        url = clean_url(url)
        platform = detect_platform(url)

        ydl_opts = {
            'outtmpl': f'{output_path}/%(title)s_%(id)s.%(ext)s',
            'quiet': True,
        }

        # Platform-based format
        if platform == "YouTube":
            if audio_only:
                ydl_opts['format'] = 'bestaudio'
            else:
                ydl_opts['format'] = 'bestvideo+bestaudio/best'
                ydl_opts['merge_output_format'] = 'mp4'
        else:
            ydl_opts['format'] = 'best'

        # Cookies support
        if os.path.exists("cookies.txt"):
            ydl_opts['cookiefile'] = "cookies.txt"

        # Retry system
        for _ in range(2):
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)

                return {
                    "status": "success",
                    "file": filename,
                    "platform": platform
                }

            except Exception:
                time.sleep(2)

        raise Exception("Download failed after retry")

    except Exception as e:
        error_msg = str(e).lower()

        if "private" in error_msg or "login" in error_msg:
            reason = "🔒 Private or login required"
        elif "not available" in error_msg:
            reason = "🚫 Video not available"
        elif "unsupported" in error_msg:
            reason = "⚠️ Unsupported link"
        elif "403" in error_msg:
            reason = "🚫 Access blocked"
        else:
            reason = "⚠️ Unable to download"

        return {
            "status": "error",
            "message": reason
        }