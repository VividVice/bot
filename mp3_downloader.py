import yt_dlp as youtube_dl
import os

global counter
counter = 1

def downloadVideo(videoInfo, path):
    global counter
    try:
        filename = f"{path}/{counter}.mp3"
        options={
            'format':'bestaudio/best',
            'keepvideo':False,
            'outtmpl': filename,
        }
        print(f"[script] downloading {videoInfo['title']}")

        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([videoInfo['webpage_url']])
            counter += 1
    except:
        print("error occurred with one video")

def get_name_from_link(link):
    video_url = link
    video_info = youtube_dl.YoutubeDL().extract_info(
        url=video_url, download=False
    )
    return video_info['title']

def prepLink(link, path="./music/"):
    if not os.path.exists(path):
        os.makedirs(path)

    video_url = link
    video_info = youtube_dl.YoutubeDL().extract_info(
        url=video_url, download=False
    )

    try:
        for singleVideoInfo in video_info['entries']:
            downloadVideo(singleVideoInfo, path)
    except KeyError:
        downloadVideo(video_info, path)

    print("download complete")