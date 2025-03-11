#!.venv/bin/python
import sys
import os
import pathlib
import subprocess
from pytubefix import Playlist, YouTube

if not os.path.exists("./Downloaded"):
    pathlib.Path("./Downloaded").mkdir(parents=True, exist_ok=True)
if not os.path.exists("./Tmp"):
    pathlib.Path("./Tmp").mkdir(parents=True, exist_ok=True)


def youtube_download(url: str, mode: bool):
    """
    Mode: boolean True=Video, False=Audio
    """
    playlist = Playlist(url)
    print("Number of videos in playlist: %s" % len(playlist.video_urls))
    for i, link in enumerate(playlist):
        print(
            i + 1,
            f" Downloaded to {vdo_download(link) if mode else audio_download(link)}",
        )


def vdo_download(url: str) -> str:
    tries = 0
    yt = YouTube(url)
    print(f"Downloading Video: {yt.title}")
    video, audio = None, None

    while video is None or audio is None:
        if tries > 10:
            yt = YouTube(url)
            tries = 0
        video = yt.streams.get_highest_resolution(progressive=False)
        audio = yt.streams.get_audio_only()
        tries += 1
    print(
        f"""
Video:
    Resolution : {video.resolution}
Audio:
    BitRate : {audio.abr}
    """
    )
    video_path = video.download("./Tmp", filename_prefix="tmp_")
    print(f"Downloaded Video to {video_path}")
    audio_path = audio.download("./Tmp", filename_prefix="tmp_")
    print(f"Downloaded Audio to {audio_path}")

    ## Skip if file already exists
    if os.path.exists(f"./Downloaded/{yt.title}.mp4"):
        print("Skip Completed Download file")
        return f"./Downloaded/{yt.title}.mp4"
    ## Enable Hardware Acceleration
    # cmd = f'ffmpeg -y -init_hw_device vaapi:/dev/dri/renderD128 -i "{audio_path}" -r 30 -i "{video_path}" -af \'aresample=async=1\' -c:a libopus -c:v copy  "./Downloaded/{yt.title}.mp4"'
    cmd = f'ffmpeg -y -i "{audio_path}" -r 30 -i "{video_path}" -af \'aresample=async=1\' -c:a libopus -c:v copy  "./Downloaded/{yt.title}.mp4"'
    print(f"Spawning {cmd}")
    subprocess.call(cmd, shell=True)
    print("Done")
    return f"./Downloaded/{yt.title}.mp4"


def audio_download(url: str) -> str | None:
    yt = YouTube(url)
    print(f"Downloading audio: {yt.title}")
    audio = None
    while audio is None:
        audio = yt.streams.get_audio_only()
    audio_path = audio.download("./Downloaded")
    return audio_path


def main(mode: int):
    match mode:
        case 1:
            print("Video Playlist Mode")
            print("ดาวน์โหลด YouTube Playlist ตัวอย่างลิงค์")
            print("https://www.youtube.com/playlist?list={list-ID}")
            url = input("Please past youtube playlist url\n: ")
            youtube_download(url, True)
        case 2:
            print("Audio Playlist Mode")
            print("ดาวน์โหลด YouTube Playlist ตัวอย่างลิงค์")
            print("https://www.youtube.com/playlist?list={list-ID}")
            url = input("Please past youtube url\n: ")
            youtube_download(url, False)
        case 3:
            print("Single Video Mode")
            print("ดาวน์โหลด YouTube ตัวอย่างลิงค์")
            print("https://www.youtube.com/watch?v=8UrwByNA2gk")
            url = input("Please past youtube url\n: ")
            print(vdo_download(url))
        case 4:
            print("Single Audio Mode")
            print("ดาวน์โหลด YouTube ตัวอย่างลิงค์")
            print("https://www.youtube.com/watch?v=8UrwByNA2gk")
            url = input("Please past youtube url\n: ")
            print(audio_download(url))


if __name__ == "__main__":
    args = sys.argv
    if not args.__len__() > 1:
        print(
            "โปรดเลือกโหมดในการ Download\n1). Playlist Videos\n2). Playlist Audios\n3). Video\n4). Audios"
        )
        mode = input("(defualt = 1) : ")
        if mode == "":
            mode = 1
        else:
            mode = int(mode)
        main(mode)
    else:
        match args[1]:
            case "-h" | "--help":
                print(
                    """
Pytube Downloader by Vaz

-h | --help : show this menu 
-c | --clean : Clean up Downloader and Tmp
                """
                )
            case "-c" | "--clean":
                cmd = "rm ./Downloaded/*"
                subprocess.call(cmd, shell=True)
                cmd = "rm ./Tmp/*"
                subprocess.call(cmd, shell=True)
