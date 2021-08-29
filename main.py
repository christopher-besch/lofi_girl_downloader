def main():
    last_int = 0
    with open("test.txt", "r", encoding="utf-8") as file:
        for line in file.readlines():
            while True:
                last_int += 1
                if int(line[:4]) != last_int:
                    print(last_int, end=",")
                else:
                    break


if __name__ == "__main__":
    main()
