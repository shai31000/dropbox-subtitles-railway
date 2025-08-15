FROM alpine:latest
RUN apk add --no-cache ffmpeg curl
WORKDIR /app
COPY . /app
CMD ["sleep", "infinity"]
