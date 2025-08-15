FROM alpine:latest

# התקנת הכלים הנדרשים
RUN apk add --no-cache ffmpeg curl python3 py3-pip bash

# הגדרת תיקיית העבודה
WORKDIR /app

# העתקת הקבצים
COPY . /app

# הפעלה של הסקריפט עם Bash כדי לראות לוגים בזמן אמת
CMD ["bash", "-c", "python3 main.py"]
