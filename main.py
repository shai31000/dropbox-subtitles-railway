import dropbox
import subprocess
import os

# קבל את הטוקן מ־Environment Variable
DROPBOX_TOKEN = os.getenv("DROPBOX_TOKEN")

# נתיבים ב־Dropbox
VIDEO_PATH = "/111/Up.Your.Anchor.1985.720p.WEBRip.HIN-ENG.x264-Vegamovies.is.mp4"      # שנה לפי הנתיב שלך
SUB_PATH = "/111/Matilda 1996 2160p UHD BluRay TrueHD 7.1 DoVi HDR10 x265-DON.srt"         # שנה לפי הנתיב שלך
OUTPUT_PATH = "/111/output.mp4"    # שם הקובץ לאחר כתוביות

CHUNK_SIZE = 50 * 1024 * 1024  # גודל chunk = 50MB

dbx = dropbox.Dropbox(DROPBOX_TOKEN)

def download_file(dropbox_path, local_path):
    meta = dbx.files_get_metadata(dropbox_path)
    size = meta.size
    with open(local_path, "wb") as f:
        for start in range(0, size, CHUNK_SIZE):
            end = min(start + CHUNK_SIZE - 1, size - 1)
            _, res = dbx.files_download_range(dropbox_path, start=start, end=end)
            f.write(res.content)
    print(f"✅ הורדה של {local_path} הסתיימה")

def upload_file(local_path, dropbox_path):
    size = os.path.getsize(local_path)
    with open(local_path, "rb") as f:
        if size <= CHUNK_SIZE:
            dbx.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode("overwrite"))
        else:
            upload_session_start_result = dbx.files_upload_session_start(f.read(CHUNK_SIZE))
            cursor = dropbox.files.UploadSessionCursor(session_id=upload_session_start_result.session_id,
                                                       offset=f.tell())
            commit = dropbox.files.CommitInfo(path=dropbox_path, mode=dropbox.files.WriteMode("overwrite"))
            while f.tell() < size:
                if (size - f.tell()) <= CHUNK_SIZE:
                    dbx.files_upload_session_finish(f.read(CHUNK_SIZE), cursor, commit)
                else:
                    dbx.files_upload_session_append_v2(f.read(CHUNK_SIZE), cursor)
                    cursor.offset = f.tell()
    print(f"✅ העלאה של {dropbox_path} הסתיימה")

# שלבים
download_file(VIDEO_PATH, "video.mp4")
download_file(SUB_PATH, "subs.srt")

# צריבת כתוביות עם ffmpeg
subprocess.run([
    "ffmpeg", "-i", "video.mp4", "-vf", "subtitles=subs.srt",
    "-c:a", "copy", "output.mp4"
], check=True)

upload_file("output.mp4", OUTPUT_PATH)
print("✅ הסתיים בהצלחה")
