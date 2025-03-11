import sys
import os
import pathlib
from pytubefix import Playlist, YouTube


def youtube_download(url: str, mode: bool):
    """
    Mode: boolean True=Video, False=Audio
    """
    playlist = Playlist(url)
    print("Number of videos in playlist: %s" % len(playlist.video_urls))
    for i, link in enumerate(playlist):
        yt = YouTube(link)
        d_video = None
        while d_video is None:
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
    reso = input("Please provide resolution: ")
    # print(f"Data: {yt.streams.get_by_resolution(reso)}")
    video = yt.streams.get_by_resolution(reso)
    while video is None:
        print("resolution not found")
        reso = input("Please provide resolution: ")
        video = yt.streams.get_by_resolution(reso)
    result = video.download("./Downloaded")
    print(f"Downloaded Video: {result}")


def audio_download(url: str):
    yt = YouTube(url)
    print(f"Downloading audio: {yt.title}")
    audio = yt.streams.get_audio_only()
    if audio is not None:
        result = audio.download("./Downloaded")
        print(f"Downloaded Video: {result}")
    else:
        print("resolution not found")
        print("Abort!!")


def main(mode: int):
    if int(mode) == 1:
        print("Video Playlist Mode")
        print("ดาวน์โหลด YouTube Playlist ตัวอย่างลิงค์")
        print("https://www.youtube.com/playlist?list={list-ID}")
        url = input("Please past youtube playlist url\n: ")
        youtube_download(url, True)
    elif int(mode) == 2:
        print("Audio Playlist Mode")
        print("ดาวน์โหลด YouTube Playlist ตัวอย่างลิงค์")
        print("https://www.youtube.com/watch?v=8UrwByNA2gk")
        url = input("Please past youtube url\n: ")
        youtube_download(url, False)
    elif int(mode) == 3:
        print("Single Video Mode")
        print("ดาวน์โหลด YouTube ตัวอย่างลิงค์")
        print("https://www.youtube.com/watch?v=8UrwByNA2gk")
        url = input("Please past youtube url\n: ")
        vdo_download(url)
    else:
        print("Single Audio Mode")
        print("ดาวน์โหลด YouTube ตัวอย่างลิงค์")
        print("https://www.youtube.com/watch?v=8UrwByNA2gk")
        url = input("Please past youtube url\n: ")
        audio_download(url)


if __name__ == "__main__":
    if not os.path.exists("./Downloaded"):
        pathlib.Path("./Downloaded").mkdir(parents=True, exist_ok=True)
    args = sys.argv
    if args.__len__() > 1 and (args[1] == "--help" or "-h"):
        print(
            """
Pytube Downloader by Vaz
        """
        )
        os._exit(0)
    print(
        "โปรดเลือกโหมดในการ Download\n1). Playlist Videos\n2). Playlist Audios\n3). Video\n4). Audios"
    )
    mode = input("(defualt = 1) : ")
    if mode == "":
        mode = 1
    else:
        mode = int(mode)
    main(mode)
