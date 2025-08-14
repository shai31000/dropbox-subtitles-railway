import os
import requests
from ffmpeg import input as ffmpeg_input

DROPBOX_TOKEN = os.environ.get("DROPBOX_TOKEN")
VIDEO_PATH = os.environ.get("VIDEO_PATH")  # למשל: "/video.mp4"
SUB_PATH = os.environ.get("SUB_PATH")      # למשל: "/sub.srt"
OUTPUT_PATH = "/output.mp4"

CHUNK_SIZE = 10 * 1024 * 1024  # 10MB

def download_from_dropbox(path, local_filename):
    print(f"⬇️ Downloading {path} → {local_filename}")
    url = "https://content.dropboxapi.com/2/files/download"
    headers = {
        "Authorization": f"Bearer {DROPBOX_TOKEN}",
        "Dropbox-API-Arg": f'{{"path": "{path}"}}',
    }
    with requests.post(url, headers=headers, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)
    print("✅ Download complete")

def upload_to_dropbox(local_filename, dropbox_path):
    print(f"⬆️ Uploading {local_filename} → {dropbox_path}")
    file_size = os.path.getsize(local_filename)
    if file_size <= 150 * 1024 * 1024:
        # Small file — simple upload
        url = "https://content.dropboxapi.com/2/files/upload"
        headers = {
            "Authorization": f"Bearer {DROPBOX_TOKEN}",
            "Dropbox-API-Arg": f'{{"path": "{dropbox_path}", "mode": "add", "autorename": true}}',
            "Content-Type": "application/octet-stream",
        }
        with open(local_filename, "rb") as f:
            data = f.read()
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
    else:
        # Large file — upload session
        with open(local_filename, "rb") as f:
            url_start = "https://content.dropboxapi.com/2/files/upload_session/start"
            headers = {
                "Authorization": f"Bearer {DROPBOX_TOKEN}",
                "Content-Type": "application/octet-stream",
                "Dropbox-API-Arg": '{"close": false}',
            }
            response = requests.post(url_start, headers=headers, data=f.read(CHUNK_SIZE))
            response.raise_for_status()
            session_id = response.json()["session_id"]

            cursor = {"session_id": session_id, "offset": f.tell()}
            while True:
                chunk = f.read(CHUNK_SIZE)
                if not chunk:
                    break
                url_append = "https://content.dropboxapi.com/2/files/upload_session/append_v2"
                headers = {
                    "Authorization": f"Bearer {DROPBOX_TOKEN}",
                    "Content-Type": "application/octet-stream",
                    "Dropbox-API-Arg": f'{{"cursor": {cursor}, "close": false}}',
                }
                requests.post(url_append, headers=headers, data=chunk)
                cursor["offset"] += len(chunk)

            url_finish = "https://content.dropboxapi.com/2/files/upload_session/finish"
            headers = {
                "Authorization": f"Bearer {DROPBOX_TOKEN}",
                "Content-Type": "application/octet-stream",
                "Dropbox-API-Arg": f'''{{
                    "cursor": {cursor},
                    "commit": {{
                        "path": "{dropbox_path}",
                        "mode": "add",
                        "autorename": true
                    }}
                }}''',
            }
            requests.post(url_finish, headers=headers, data=b"")

    print("✅ Upload complete")

def burn_subtitles(video_file, subtitles_file, output_file):
    print("🔥 Burning subtitles...")
    (
        ffmpeg_input(video_file)
        .output(output_file, vf=f"subtitles={subtitles_file}")
        .run(overwrite_output=True)
    )
    print("🎉 Subtitles burned successfully!")

# === Main run ===
download_from_dropbox(VIDEO_PATH, "video.mp4")
download_from_dropbox(SUB_PATH, "sub.srt")

burn_subtitles("video.mp4", "sub.srt", OUTPUT_PATH)

upload_to_dropbox(OUTPUT_PATH, "/output.mp4")
