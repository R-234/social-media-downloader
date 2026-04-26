import streamlit as st
import os
import shutil

from downloader import download_media, detect_platform
from utils import create_zip, save_to_db

st.set_page_config(page_title="Social Media Downloader", layout="centered")

# -------------------------------
# Header
# -------------------------------
st.title("🚀 Social Media Downloader")
st.caption("Developed by Rakesh Rathod")

# Minimal info
with st.expander("🌐 Platforms"):
    st.write("YouTube ✅ | Instagram ⚠️ | Facebook ⚠️")

# -------------------------------
# Session state
# -------------------------------
if "files" not in st.session_state:
    st.session_state.files = []
if "failed" not in st.session_state:
    st.session_state.failed = []

# -------------------------------
# Inputs
# -------------------------------
mode = st.radio("Choose Input Type", ["Single Link", "Multiple Links"], horizontal=True)

audio_only = st.checkbox("🎧 Audio only (YouTube)")
zip_option = st.checkbox("📦 Download as ZIP")

if mode == "Single Link":
    input_data = st.text_input("Paste link")
else:
    input_data = st.text_area("Paste multiple links (one per line)")

col1, col2 = st.columns(2)
run = col1.button("⬇ Download")
clear = col2.button("❌ Clear")

# -------------------------------
# Clear
# -------------------------------
if clear:
    st.session_state.files = []
    st.session_state.failed = []
    st.experimental_rerun()

# -------------------------------
# Process
# -------------------------------
if run:
    if not input_data.strip():
        st.warning("Enter at least one link")
        st.stop()

    # reset storage
    shutil.rmtree("downloads", ignore_errors=True)
    os.makedirs("downloads", exist_ok=True)
    st.session_state.files = []
    st.session_state.failed = []

    if mode == "Single Link":
        urls = [input_data.strip()]
    else:
        urls = [u.strip() for u in input_data.split("\n") if u.strip()]

    st.subheader("📥 Processing...")

    success = 0

    # Sequential → more stable on cloud (esp. Instagram)
    for url in urls:
        platform = detect_platform(url)
        result = download_media(url, "downloads", audio_only)

        if result["status"] == "success":
            path = result["file"]

            st.session_state.files.append({
                "path": path,
                "url": url,
                "platform": platform
            })

            save_to_db(path, url, platform)
            st.success(f"✅ [{platform}] Downloaded")
            success += 1
        else:
            st.session_state.failed.append({
                "url": url,
                "platform": platform,
                "reason": result["message"]
            })

    total = len(urls)
    st.success(f"🎉 Completed! {success}/{total} successful")

    # Grouped failures
    if st.session_state.failed:
        st.warning(f"⚠️ {len(st.session_state.failed)} link(s) could not be downloaded")
        with st.expander("View failed links"):
            for f in st.session_state.failed:
                st.write(f"❌ [{f['platform']}] {f['url']}")
                st.caption(f"Reason: {f['reason']}")
        st.info("👉 Try another link or ensure the content is public/video.")

# -------------------------------
# Download buttons (persistent)
# -------------------------------
if st.session_state.files:
    st.subheader("⬇ Download Files")

    for f in st.session_state.files:
        path = f["path"]
        if os.path.exists(path):
            with open(path, "rb") as fp:
                st.download_button(
                    label=f"⬇ {os.path.basename(path)}",
                    data=fp,
                    file_name=os.path.basename(path),
                    key=path
                )

# -------------------------------
# ZIP
# -------------------------------
if zip_option and st.session_state.files:
    zip_path = create_zip("downloads")
    with open(zip_path, "rb") as zf:
        st.download_button(
            "⬇ Download ZIP",
            zf,
            file_name="downloads.zip"
        )