import argparse
import os


def generate_graphs(vertex, filename):
    fullgen = './fullgen {vertex} code 8 stdout > {fn}.s6 2>/dev/null'
    os.system(fullgen.format(vertex=vertex, fn=filename))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-from', dest='f', type=int, default=20)
    parser.add_argument('-to', dest='t', type=int, default=20)
    parser.add_argument('-p', dest='path', default='./')
    args = parser.parse_args()
    for x in range(args.f, args.t, 2):
        generate_graphs(x, '../%s/%d' % (args.path, x))
