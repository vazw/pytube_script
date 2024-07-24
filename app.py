import os
import pathlib
from pytubefix import Playlist, YouTube


def youtube_download(url: str, mode: bool):
    playlist = Playlist(f"{url}")
    print("Number of videos in playlist: %s" % len(playlist.video_urls))
    for i, link in enumerate(playlist):
        yt = YouTube(link)
        if mode:
            print(f"Downloading video: {yt.title}")
            d_video = yt.streams.get_highest_resolution()
        else:
            print(f"Downloading audio: {yt.title}")
            d_video = yt.streams.get_audio_only()
        d_video.download("./Downloaded")
        print(i + 1, " Video is Downloaded.")


def vdo_download(url: str):
    yt = YouTube(url)
    (
        yt.streams.filter(progressive=True, file_extension="mp4")
        .first()
        .download("./Downloaded")
    )


def main(mode: int):
    dmode = True if mode == 1 else False
    print(mode)
    if int(mode) != 3:
        while True:
            print("ดาวน์โหลด YouTube Playlist ตัวอย่างลิงค์")
            print("https://www.youtube.com/playlist?list={list-ID}")
            try:
                url = input("Please past youtube playlist url\n: ")
                youtube_download(url, dmode)
            except KeyboardInterrupt:
                print("bye")
                return
    else:
        print("ดาวน์โหลด YouTube Video")
        url = input("Please past youtube url\n: ")
        vdo_download(url)


if __name__ == "__main__":
    if not os.path.exists("./Downloaded"):
        pathlib.Path("./Downloaded").mkdir(parents=True, exist_ok=True)
    print("โปรดเลือกโหมดในการ Download\n1). Playlist Videos\n2). Audios\n3). Video")
    mode = input("(defualt = 1) : ")
    if mode == "":
        mode = 1
    else:
        mode = mode
    main(mode)
