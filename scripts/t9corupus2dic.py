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
        parts = x.split(',')
        if len(parts) == 7:
            data.append([(parts[5], parts[6], parts[1]), x])
        else:
            data.append([("", "", x), x])

    print("0,UNK,UNK,X,X,XX,_")
    for o in sorted(data, key=lambda z: z[0]):
        print(o[1])


if __name__ == '__main__':
    main(sys.argv[1:])
