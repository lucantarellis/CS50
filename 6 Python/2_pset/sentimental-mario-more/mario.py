# TODO


def main():
    while True:
        height = input("Height: ")
        if height.isnumeric():
            height = int(height)
            if height > 0 and height < 9:
                break
    counter = 1
    printmario(height, counter)


def printmario(height, counter):
    if height == 0:
        return
    print(' ' * (height - 1) + '#' * counter + '  ' + '#' * counter)
    printmario(height - 1, counter + 1)


if __name__ == "__main__":
    main()