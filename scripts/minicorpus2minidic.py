import os, sys


dic = set()


def process(fd):
    for line in fd:
        line = line.strip("\n\r")
        if line != "EOS" and not line.startswith("# "):
            dic.add(line)


def main(files):
    for fname in files:
        with open(fname, 'rt', encoding='utf-8') as inf:
            process(inf)

    data = []
    for x in dic:
        parts = x.split(',', 2)
        data.append((parts[1], x))

    # print("0,0")
    for o in sorted(data, key=lambda z: z[0]):
        print(o[1])


if __name__ == '__main__':
    main(sys.argv[1:])
