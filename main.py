import dropbox
import subprocess
import os

# קריאת הטוקן מדרופבוקס (נגדיר אותו ב-Railway)
DROPBOX_TOKEN = os.environ["DROPBOX_TOKEN"]

# נתיבים בקבצי דרופבוקס שלך (תשנה לפי הצורך)
VIDEO_PATH = "/111/Up.Your.Anchor.1985.720p.WEBRip.HIN-ENG.x264-Vegamovies.is.mp4"    # קובץ וידאו בדרופבוקס
SUB_PATH = "/111/Matilda 1996 2160p UHD BluRay TrueHD 7.1 DoVi HDR10 x265-DON.srt"       # קובץ כתוביות בדרופבוקס
OUTPUT_PATH = "/output.mp4"  # קובץ תוצר

dbx = dropbox.Dropbox(DROPBOX_TOKEN)

def download_file(dbx_path, local_path):
    print(f"📥 מוריד {dbx_path} מדרופבוקס...")
    with open(local_path, "wb") as f:
        metadata, res = dbx.files_download(path=dbx_path)
        f.write(res.content)

def upload_file(local_path, dbx_path):
    print(f"📤 מעלה {dbx_path} לדרופבוקס...")
    with open(local_path, "rb") as f:
        dbx.files_upload(f.read(), dbx_path, mode=dropbox.files.WriteMode("overwrite"))

# שלבים
download_file(VIDEO_PATH, "video.mp4")
download_file(SUB_PATH, "subs.srt")

subprocess.run([
    "ffmpeg", "-i", "video.mp4", "-vf", "subtitles=subs.srt",
    "-c:a", "copy", "output.mp4"
], check=True)

upload_file("output.mp4", OUTPUT_PATH)
print("✅ הסתיים בהצלחה")
