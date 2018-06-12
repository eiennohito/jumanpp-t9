#!/usr/bin/env python3

import sys
from conll2t9corpus import mapping


def mb_escape(s):
    if '"' in s or ',' in s:
        replaced = s.replace('"', '""')
        return f'"{replaced}"'
    return s


def process(fd):
    for line in fd:
        line = line.rstrip('\n\r')
        if line.startswith("#"):
            pass  # skip comments
        elif line == "":
            print("EOS")
        else:
            parts = line.split('\t')
            if len(parts) < 5:
                continue

            surf = parts[1].lower()
            numbers = surf.translate(mapping)
            print(",".join(mb_escape(x) for x in [numbers, surf]))


def main(files):
    for fname in files:
        with open(fname, 'rt', encoding='utf-8') as inf:
            process(inf)


if __name__ == '__main__':
    main(sys.argv[1:])
