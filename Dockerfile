# שימוש בבסיס קל משקל של Alpine Linux
FROM alpine:latest

# התקנת הכלים שנצטרך: FFmpeg, curl, Python
RUN apk add --no-cache ffmpeg curl python3 py3-pip

# הגדרת תיקיית העבודה
WORKDIR /app

# העתקת כל הקבצים מהמאגר הנוכחי לשרת
COPY . /app

# הפקודה שתורץ ברגע שהקונטיינר יעלה
CMD ["python3", "main.py"]
