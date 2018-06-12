import os, sys
import collections

IdHeaderLen = len("# sent_id = ")

mapping = collections.defaultdict(lambda: ord('0'), {
    # punctuation
    ord('.'): ord('1'),
    ord(','): ord('1'),
    ord('!'): ord('1'),
    ord('?'): ord('1'),
    ord('*'): ord('1'),
    ord('\''): ord('1'),
    ord('"'): ord('1'),
    ord('/'): ord('1'),
    ord('\\'): ord('1'),
    ord(':'): ord('1'),
    ord(';'): ord('1'),
    ord('%'): ord('1'),
    ord('&'): ord('1'),
    ord('$'): ord('1'),
    ord('#'): ord('1'),
    ord('-'): ord('1'),
    ord('+'): ord('1'),
    ord('='): ord('1'),
    ord('~'): ord('1'),
    ord('^'): ord('1'),
    ord('|'): ord('1'),
    ord('”'): ord('1'),
    ord('“'): ord('1'),
    ord('('): ord('1'),
    ord(')'): ord('1'),
    ord('['): ord('1'),
    ord(']'): ord('1'),
    # alphabet
    ord('a'): ord('2'),
    ord('b'): ord('2'),
    ord('c'): ord('2'),
    ord('d'): ord('3'),
    ord('e'): ord('3'),
    ord('f'): ord('3'),
    ord('g'): ord('4'),
    ord('h'): ord('4'),
    ord('i'): ord('4'),
    ord('j'): ord('5'),
    ord('k'): ord('5'),
    ord('l'): ord('5'),
    ord('m'): ord('6'),
    ord('n'): ord('6'),
    ord('o'): ord('6'),
    ord('p'): ord('7'),
    ord('q'): ord('7'),
    ord('r'): ord('7'),
    ord('s'): ord('7'),
    ord('t'): ord('8'),
    ord('u'): ord('8'),
    ord('v'): ord('8'),
    ord('w'): ord('9'),
    ord('x'): ord('9'),
    ord('y'): ord('9'),
    ord('z'): ord('9'),
    # numbers
    ord('0'): ord('0'),
    ord('1'): ord('1'),
    ord('2'): ord('2'),
    ord('3'): ord('3'),
    ord('4'): ord('4'),
    ord('5'): ord('5'),
    ord('6'): ord('6'),
    ord('7'): ord('7'),
    ord('8'): ord('8'),
    ord('9'): ord('9'),
})


def mb_escape(s):
    if '"' in s or ',' in s:
        replaced = s.replace('"', '""')
        return f'"{replaced}"'
    return s


def process(fd):
    for line in fd:
        line = line.strip('\n\r')
        if line.startswith("# sent_id = "):
            print(f"# S-ID: {line[IdHeaderLen:]}")
        elif line == "":
            print("EOS")
        else:
            parts = line.split('\t')
            if len(parts) < 5:
                continue

            surf = parts[1].lower()
            lemma = parts[2].lower()
            ud_pos = parts[3]
            ptb_pos = parts[4]
            numbers = surf.translate(mapping)
            if len(ptb_pos) >= 3:
                ptb_cnj = ptb_pos
            else:
                ptb_cnj = "_"
            print(",".join(mb_escape(x) for x in [numbers, surf, lemma, ud_pos, ptb_pos[0], ptb_pos[0:2], ptb_cnj]))


def main(files):
    for fname in files:
        with open(fname, 'rt', encoding='utf-8') as inf:
            process(inf)


if __name__ == '__main__':
    main(sys.argv[1:])
