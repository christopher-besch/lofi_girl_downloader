import os
import shutil


def main():
    for orig_filename_raw in os.scandir("lofi"):
        if not orig_filename_raw.is_file():
            continue
        orig_filename = orig_filename_raw.name
        new_filename = orig_filename.replace("   ", " – ")
        new_filename = new_filename.replace(" - ", " – ")
        new_filename = new_filename.replace(" — ", " – ")
        new_filename = new_filename.replace(" - ", " – ")
        new_filename = new_filename.replace(" — ", " – ")
        new_filename = new_filename.replace(" - ", " – ")
        new_filename = new_filename.replace(" — ", " – ")
        print(new_filename)
        play_id = new_filename[:4]
        interpret = new_filename[5:-4].split(" – ")[0]
        if " x " in interpret:
            interpret = interpret.split(" x ")[0]
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
        interpret = interpret.replace("9", "").strip()
        name = new_filename[5:-4].split(" – ")[1]
        new_path = os.path.join("lofi", interpret)
        if not os.path.exists(new_path):
            os.mkdir(new_path)
        shutil.move(os.path.join("lofi", orig_filename),
                    os.path.join(new_path, new_filename))


if __name__ == "__main__":
    main()
