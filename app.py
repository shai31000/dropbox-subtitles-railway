import os
import dropbox
import subprocess
import sys

# Replace with your Dropbox access token
DROPBOX_ACCESS_TOKEN = os.environ.get("DROPBOX_ACCESS_TOKEN")

# Replace with the paths to your video and subtitle files in Dropbox
VIDEO_PATH = os.environ.get("VIDEO_PATH")
SUBTITLE_PATH = os.environ.get("SUBTITLE_PATH")

# The path where you want to save the new video
OUTPUT_PATH = os.environ.get("OUTPUT_PATH")

def download_file(dbx, dbx_path, local_path):
    print(f"Downloading {dbx_path}...")
    dbx.files_download_to_file(local_path, dbx_path)
    print(f"Downloaded {local_path}.")

def upload_file(dbx, local_path, dbx_path):
    print(f"Uploading {local_path}...")
    with open(local_path, "rb") as f:
        dbx.files_upload(f.read(), dbx_path, mode=dropbox.files.WriteMode('overwrite'))
    print(f"Uploaded {local_path} to {dbx_path}.")

def burn_subtitles(video_file, subtitle_file, output_file):
    print("Burning subtitles...")
    command = [
        "ffmpeg",
        "-y",  # Overwrite output file without asking
        "-i", video_file,
        "-vf", f"subtitles={subtitle_file}",
        "-c:a", "copy",
        output_file
    ]
    try:
        subprocess.run(command, check=True)
        print("Subtitles burned successfully!")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

def main():
    if not all([DROPBOX_ACCESS_TOKEN, VIDEO_PATH, SUBTITLE_PATH, OUTPUT_PATH]):
        print("Error: Missing one or more environment variables.")
        sys.exit(1)

    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

    video_local_path = os.path.basename(VIDEO_PATH)
    subtitle_local_path = os.path.basename(SUBTITLE_PATH)
    output_local_path = os.path.basename(OUTPUT_PATH)

    download_file(dbx, VIDEO_PATH, video_local_path)
    download_file(dbx, SUBTITLE_PATH, subtitle_local_path)

    burn_subtitles(video_local_path, subtitle_local_path, output_local_path)

    upload_file(dbx, output_local_path, OUTPUT_PATH)

if __name__ == "__main__":
    main()
