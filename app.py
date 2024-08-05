import os
import pathlib
from pytubefix import Playlist, YouTube


def youtube_download(url: str, mode: bool):
    playlist = Playlist(url)
    print("Number of videos in playlist: %s" % len(playlist.video_urls))
    for i, link in enumerate(playlist):
        yt = YouTube(link)
        if mode:
            print(f"Downloading video: {yt.title}")
            d_video = yt.streams.get_highest_resolution()
        else:
            print(f"Downloading audio: {yt.title}")
            d_video = yt.streams.get_audio_only()
        result = d_video.download("./Downloaded")
        print(i + 1, f" Downloaded to {result}.")


def vdo_download(url: str):
    yt = YouTube(url)
    print(f"Downloading Video: {yt.title}")
    result = yt.streams.get_highest_resolution().download("./Downloaded")
    print(f"Downloaded Video: {result}")


def audio_download(url: str):
    yt = YouTube(url)
    print(f"Downloading audio: {yt.title}")
    result = yt.streams.get_audio_only().download("./Downloaded")
    print(f"Downloaded Video: {result}")


def main(mode: int):
    dmode = True if mode == 1 else False
    if int(mode) != 3:
        print("ดาวน์โหลด YouTube Playlist ตัวอย่างลิงค์")
        print("https://www.youtube.com/playlist?list={list-ID}")
        url = input("Please past youtube playlist url\n: ")
        youtube_download(url, dmode)
    else:
        print("ดาวน์โหลด YouTube Video ตัวอย่างลิงค์")
        print("https://www.youtube.com/watch?v=8UrwByNA2gk")
        url = input("Please past youtube url\n: ")
        vdo_download(url)


if __name__ == "__main__":
    if not os.path.exists("./Downloaded"):
        pathlib.Path("./Downloaded").mkdir(parents=True, exist_ok=True)
    print(
        "โปรดเลือกโหมดในการ Download\n1). Playlist Videos\n2). Playlist Audios\n3). Video\n4). Audios"
    )
    mode = input("(defualt = 1) : ")
    if mode == "":
        mode = 1
    else:
        mode = mode
    main(mode)
