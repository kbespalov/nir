import os


def generate_graphs(vertex, filename):
    fullgen = './fullgen {vertex} code 8 symm C1 stdout > {fn}.s6 2>/dev/null'
    os.system(fullgen.format(vertex=vertex, fn=filename))


for x in range(20, 50, 2):
    generate_graphs(x, '../sg/%d' % x)
