import argparse
import igraph
import networkx as nx
import os
import worker
from multiprocessing import Process, Queue


def graphs_flow(dirname):
    g_files = [str(z) + ".s6" for z in
               sorted([int(x.split('.')[0]) for x in os.listdir(dirname)])]
    for f in g_files:
        with open(os.path.join(dirname, f), 'rb') as s6:
            for encoded_graph in s6:
                g = nx.parse_sparse6(encoded_graph.strip())
                yield igraph.Graph(edges=g.edges())


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', dest='workers', type=int, default=4)
    parser.add_argument('-i', dest='input_path')
    parser.add_argument('-o', dest='output_path')
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    queue = Queue(100)
    workers = []
    process = []

    for x in range(args.workers):
        gp = worker.GraphProcessor(queue=queue, output=args.output_path)
        p = Process(target=gp.run)
        p.daemon = True
        workers.append(gp)
        process.append(p)
        p.start()
    for g in graphs_flow(args.input_path):
        queue.put(g)


main()
