import streamlit as st
import os
import shutil

from downloader import download_media, detect_platform
from utils import create_zip, save_to_db

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Pro Downloader", layout="centered")

# -------------------------------
# Title
# -------------------------------
st.title("🚀 Social Media Downloader")
st.caption("Developed by Rakesh Rathod")

# -------------------------------
# Minimal Platform Info
# -------------------------------
with st.expander("🌐 Platforms"):
    st.write("YouTube ✅ | Instagram ⚠️ | Facebook ⚠️")

# -------------------------------
# Session State
# -------------------------------
if "files" not in st.session_state:
    st.session_state.files = []

if "failed_links" not in st.session_state:
    st.session_state.failed_links = []

# -------------------------------
# Input Mode
# -------------------------------
mode = st.radio("Choose Input Type", ["Single Link", "Multiple Links"])

audio_only = st.checkbox("🎧 Audio only (YouTube)")
zip_option = st.checkbox("📦 Download as ZIP")

if mode == "Single Link":
    input_data = st.text_input("Paste link")
else:
    input_data = st.text_area("Paste multiple links")

# -------------------------------
# Buttons
# -------------------------------
col1, col2 = st.columns(2)

download_clicked = col1.button("⬇ Download")
clear_clicked = col2.button("❌ Clear")

# -------------------------------
# Clear
# -------------------------------
if clear_clicked:
    st.session_state.files = []
    st.session_state.failed_links = []
    st.experimental_rerun()

# -------------------------------
# Download Process
# -------------------------------
if download_clicked:

    if not input_data.strip():
        st.warning("Enter at least one link")
        st.stop()

    shutil.rmtree("downloads", ignore_errors=True)
    os.makedirs("downloads", exist_ok=True)

    st.session_state.files = []
    st.session_state.failed_links = []

    if mode == "Single Link":
        url_list = [input_data.strip()]
    else:
        url_list = [u.strip() for u in input_data.split("\n") if u.strip()]

    st.subheader("📥 Processing...")

    success = 0

    for url in url_list:
        platform = detect_platform(url)

        result = download_media(url, "downloads", audio_only)

        if result["status"] == "success":
            file_path = result["file"]

            st.session_state.files.append({
                "path": file_path,
                "url": url,
                "platform": platform
            })

            save_to_db(file_path, url, platform)

            st.success(f"✅ [{platform}] Downloaded")
            success += 1

        else:
            # Store failed link
            st.session_state.failed_links.append({
                "url": url,
                "platform": platform,
                "reason": result["message"]
            })

    # -------------------------------
    # Summary
    # -------------------------------
    total = len(url_list)
    failed_count = len(st.session_state.failed_links)

    st.success(f"🎉 Completed! {success}/{total} successful")

    # -------------------------------
    # Failed Links (Grouped)
    # -------------------------------
    if failed_count > 0:
        st.warning(f"⚠️ {failed_count} link(s) could not be downloaded")

        with st.expander("View failed links"):
            for item in st.session_state.failed_links:
                st.write(f"❌ [{item['platform']}] {item['url']}")
                st.caption(f"Reason: {item['reason']}")

        st.info("👉 Try another link or ensure the content is public/video.")

# -------------------------------
# Show Download Buttons (Persistent)
# -------------------------------
if st.session_state.files:

    st.subheader("⬇ Download Files")

    for file_data in st.session_state.files:
        file_path = file_data["path"]

        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                st.download_button(
                    label=f"⬇ {os.path.basename(file_path)}",
                    data=f,
                    file_name=os.path.basename(file_path),
                    key=file_path
                )

# -------------------------------
# ZIP Download
# -------------------------------
if zip_option and st.session_state.files:
    zip_file = create_zip("downloads")

    with open(zip_file, "rb") as f:
        st.download_button(
            "⬇ Download ZIP",
            f,
            file_name="downloads.zip"
        )