#!/usr/bin/env python3
import sys
import os
import shutil
import _thread
from typing import List

DOWNLOAD_LOCK_FILE = "downloaded.lock"
URL = "https://www.youtube.com/playlist?list=PLofht4PTcKYnaH8w5olJCI-wUVxuoMHqM"
THREADS = 30


def download_all():
    os.system(
        f'youtube-dl --continue --ignore-errors --download-archive {DOWNLOAD_LOCK_FILE} --no-post-overwrites --no-overwrites --output "%(playlist_index)s-%(title)s.%(ext)s" --extract-audio --audio-format mp3 --audio-quality 0 {URL}')


def download_force(vids: List[str]):
    if (len(vids) == 0):
        return
    os.system(
        f'youtube-dl --continue --ignore-errors --playlist-items {",".join(vids)} --output "%(playlist_index)s-%(title)s.%(ext)s" --extract-audio --audio-format mp3 --audio-quality 0 {URL}')


# doesn't account for missing last or first videos
def get_missing_vids() -> List[str]:
    print("scanning downloaded videos: ...")
    missing_vids: List[str] = []
    last_id = 0
    files = os.listdir()
    files.sort()
    for file in files:
        print(file)
        file_id = int(file.split("-")[0])
        while True:
            last_id += 1
            if file_id != last_id:
                missing_vids.append(str(last_id))
            else:
                break
    return missing_vids


def main() -> bool:
    os.mkdir("lofi")
    os.chdir("lofi")
    os.mkdir("raw")
    os.chdir("raw")

    # shutil.move(f"../{DOWNLOAD_LOCK_FILE}", DOWNLOAD_LOCK_FILE)

    # third time's the charm
    for i in range(3):
        print(f"download attempt #{i+1}: ...")
        download_all()
        # for _ in range(THREADS):
        #     _thread.start_new_thread(download_all, ())
    shutil.move(DOWNLOAD_LOCK_FILE, f"../{DOWNLOAD_LOCK_FILE}")

    # check if all files have been downloaded
    missing_vids = get_missing_vids()
    if len(missing_vids) == 0:
        print("all videos have been downloaded")
    else:
        print(f"downloading missing videos {', '.join(missing_vids)}: ...")
        download_force(missing_vids)
        missing_vids = get_missing_vids()
        if len(missing_vids) != 0:
            raise ValueError(
                f"These Videos failed to download twice: {', '.join(missing_vids)}")

    os.chdir("..")
    shutil.copytree("raw", "detoxed")
    print("detoxing files: ...")
    os.chdir("detoxed")
    os.system("detox .")

    return True


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
