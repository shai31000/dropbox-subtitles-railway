FROM python:3.11

# התקנת FFmpeg
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# העתקת קבצים
WORKDIR /app
COPY . /app

# התקנת ספריות פייתון
RUN pip install --no-cache-dir -r requirements.txt

# פקודת ההרצה
CMD ["python", "main.py"]
