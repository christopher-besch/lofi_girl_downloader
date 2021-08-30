#!/usr/bin/env python3
import sys
import os
import shutil
from argparse import ArgumentParser
from typing import List

DOWNLOAD_LOCK_FILE = "downloaded.lock"
URL = "https://www.youtube.com/playlist?list=PLofht4PTcKYnaH8w5olJCI-wUVxuoMHqM"

REPLACEMENTS = {
    "mell": "mell_o"
}


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
        file_id = int(file.split("-")[0])
        while True:
            last_id += 1
            if file_id != last_id:
                missing_vids.append(str(last_id))
            else:
                break
    return missing_vids


def sort_folder():
    print("sorting music in folders: ...")
    files = os.listdir()
    files.sort()
    for file in files:
        print(file)
        # remove id
        parts = file.split("-")
        file_id = parts[0]
        interpret = parts[1]

        interpret = interpret.lower()
        interpret = interpret.replace("’", "'")
        interpret = interpret.replace("0", "")
        interpret = interpret.replace("1", "")
        interpret = interpret.replace("2", "")
        interpret = interpret.replace("3", "")
        interpret = interpret.replace("4", "")
        interpret = interpret.replace("5", "")
        interpret = interpret.replace("6", "")
        interpret = interpret.replace("7", "")
        interpret = interpret.replace("8", "")
        interpret = interpret.replace("9", "")

        main_interpret = interpret.split("_x_")[0].strip("_")
        if main_interpret in REPLACEMENTS:
            main_interpret = REPLACEMENTS[main_interpret]

        new_file_name = "-".join(parts[1:])

        if not os.path.exists(main_interpret):
            os.mkdir(main_interpret)
        print(f"{file} -> {main_interpret}/{new_file_name}")
        shutil.move(file, f"{main_interpret}/{new_file_name}")


def main() -> bool:
    parser = ArgumentParser(
        description="Download entire Music Database of Lofi Girl")
    parser.add_argument(
        "-f", "--force", help="use already existent lofi folder", action="store_true")
    parser.add_argument(
        "-s", "--skip", help="skip initial download", action="store_true")
    args = parser.parse_args()

    # create folder structure
    if not os.path.exists("lofi"):
        os.mkdir("lofi")
    else:
        if args.force:
            print("using already existent lofi folder")
        else:
            print("lofi folder already exists; use --force to use it")
            return False
    os.chdir("lofi")
    if not os.path.exists("raw"):
        os.mkdir("raw")
    os.chdir("raw")

    if os.path.exists(f"../{DOWNLOAD_LOCK_FILE}"):
        print("copying existent lock file")
        shutil.move(f"../{DOWNLOAD_LOCK_FILE}", DOWNLOAD_LOCK_FILE)

    if not args.skip:
        # third time's the charm
        for i in range(3):
            print(f"download attempt #{i+1}: ...")
            download_all()
    if os.path.exists(DOWNLOAD_LOCK_FILE):
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

    # detoxing
    os.chdir("..")
    if not os.path.exists("detoxed"):
        print("copying files for detoxification: ...")
        shutil.copytree("raw", "detoxed")
        print("detoxing files: ...")
        os.chdir("detoxed")
        os.system("detox .")
    else:
        print("detoxed folder already found, delete it to redo detoxification")
        os.chdir("detoxed")
    sort_folder()

    return True


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
