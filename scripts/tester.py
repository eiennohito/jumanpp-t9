import sys, subprocess
from conll2t9corpus import mapping


def work(proc):
    for line in sys.stdin:
        line = line.lower().rstrip().replace(' ', '').translate(mapping)
        print(line)
        proc.stdin.write(line.encode('utf-8'))
        proc.stdin.write(b'\n')
        proc.stdin.flush()


if __name__ == '__main__':
    subproc = sys.argv[1]
    modelfile = sys.argv[2]

    with subprocess.Popen([subproc, modelfile], stdin=subprocess.PIPE) as proc:
        work(proc)
