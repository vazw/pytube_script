import os
import pathlib
from pytube import Playlist, YouTube


def youtube_download(url: str, mode: bool):
    playlist = Playlist(f"{url}")
    print("Number of videos in playlist: %s" % len(playlist.video_urls))
    for i, link in enumerate(playlist):
        yt = YouTube(link)
        if mode:
            d_video = (
                yt.streams.filter(progressive=True, file_extension="mp4")
                .order_by("resolution")
                .desc()
                .first()
            )
        else:
            d_video = (
                yt.streams.filter(only_audio=True, file_extension="mp4")
                .order_by("abr")
                .desc()
                .first()
            )
        d_video.download("./Downloaded")
        print(i + 1, " Video is Downloaded.")


def main(mode: int = 1):
    print("ดาวน์โหลด YouTube Playlist ตัวอย่างลิงค์")
    print("https://www.youtube.com/playlist?list={list-ID}")
    dmode = True if mode == 1 else False
    while True:
        try:
            url = input("Please past youtube playlist url\n: ")
            youtube_download(url, dmode)
        except KeyboardInterrupt:
            print("bye")
            return


if __name__ == "__main__":
    if not os.path.exists("./Downloaded"):
        pathlib.Path("./Downloaded").mkdir(parents=True, exist_ok=True)
    print("โปรดเลือกโหมดในการ Download\n1). Videos\n2). Audios")
    mode = input("(defualt = 1) : ")
    if mode == "":
        mode = 1
    else:
        mode = mode
    main(mode)
