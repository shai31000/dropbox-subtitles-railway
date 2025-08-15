import os
import subprocess

# קישורי הורדה ישירים מה-Dropbox (נחליף בהמשך)
video_url = "https://www.dropbox.com/scl/fi/nb36c64ogxylnq8s8sp2i/Up.Your.Anchor.1985.720p.WEBRip.HIN-ENG.x264-Vegamovies.is.mp4?rlkey=apdxs5tatrc75x7im4funoqzp&st=cmr4b3ya&dl=1"
subs_url = "https://www.dropbox.com/scl/fi/6df0zegjtcgfh19c0jkfx/Matilda-1996-2160p-UHD-BluRay-TrueHD-7.1-DoVi-HDR10-x265-DON.srt?rlkey=70jcjo0bwm4paopksvdpzijze&st=uwgh8i4n&dl=1"

# שמות הקבצים המקומיים
video_file = "video.mp4"
subs_file = "subs.srt"
output_file = "video_with_subs.mp4"

# הורדת הווידאו
subprocess.run(["curl", "-L", video_url, "-o", video_file], check=True)

# הורדת הכתוביות
subprocess.run(["curl", "-L", subs_url, "-o", subs_file], check=True)

# הפעלת FFmpeg לצריבת כתוביות
subprocess.run([
    "ffmpeg", "-i", video_file, "-vf", f"subtitles={subs_file}",
    "-c:a", "copy", output_file
], check=True)

print("סיום! הווידאו עם הכתוביות נוצר בשם", output_file)
