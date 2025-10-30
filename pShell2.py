import sys

def main():
    a = sys.argv
    s = ""
    for i in range(1, len(a)):
        s = f"{s} " + a[i]
    print(s)


if __name__ == "__main__":
    main()