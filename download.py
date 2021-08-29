import sys
import os
import shutil
import glob


def main() -> bool:
    os.mkdir("lofi_raw")
    os.chdir("lofi_raw")
    os.system('youtube-dl --continue --ignore-errors --download-archive downloaded.lock --no-post-overwrites --no-overwrites --output "%(playlist_index)s-%(title)s.%(ext)s" --extract-audio --audio-format mp3 --audio-quality 0 https://www.youtube.com/playlist?list=PLofht4PTcKYnaH8w5olJCI-wUVxuoMHqM')
    os.mkdir("lofi")
    for file in glob.glob(r"*.mp3"):
        shutil.copy(file, f"lofi/{file}")
    os.chdir("lofi")
    os.system("detox .")
    return True


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
