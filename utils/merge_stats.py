import argparse
import csv
import os
import json

import matplotlib.pyplot as plt
import numpy as np

from tabulate import tabulate


def load(stats_folder):
    results = {}
    for fname in os.listdir(stats_folder):
        # vertex number
        v = int(fname.split('_')[0])
        if v not in results:
            results[v] = {'a': [],
                          'r': [],
                          'd': []}
        with open(os.path.join(stats_folder, fname)) as f:
            res = json.load(f)
            for invariant in res:
                for z in res[invariant]:
                    results[v][invariant].append(z)

    # print "results merged..."
    return results


def print_shifts(results, key, upper_bound, max_size):
    table = {}
    for vertex_number in results:
        shifts = [0] * max_size
        for value in results[vertex_number][key]:
            if value != 0:
                shifts[upper_bound(vertex_number) - value] += 1
        table[vertex_number] = shifts
    print tabulate([[x] + y for x, y in table.items()])


def dump_as_csv(zipped, filename):
    with open(filename, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile,
                                delimiter=',',
                                quotechar='|',
                                quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["x", "y"])
        for x, y in zipped:
            spamwriter.writerow([x, y])


def plot_distribution(results):

    alpha = [[], []]
    diameter = [[], []]
    radius = [[], []]

    def plot(x, y, label):
        if not x:
            return
        plt.scatter(x=x, y=y, label=label)
        plt.yticks(np.arange(min(y), max(y) + 1, 1))
        plt.xticks(np.arange(min(x), max(x) + 1, 2.0))
        plt.show()
        plt.savefig(label + ".png")
        plt.close()

    for vertex_number in results:
        for invariant in results[vertex_number]:
            values = results[vertex_number][invariant]
            if invariant == 'a':
                dest = alpha
            if invariant == 'd':
                dest = diameter
            if invariant == 'r':
                dest = radius
            setted = set(values)
            dest[0].extend([vertex_number] * len(setted))
            dest[1].extend(setted)

    print "alpha distibution:"
    for vertex_number in results:
        print vertex_number, ' '.join(
            str(x) for x in sorted(set(results[vertex_number]['a'])))

    print "alpha shifts:"
    print_shifts(results, 'a', lambda n: n / 2 - 2, 7)

    print "radius distibution:"
    for vertex_number in results:
        print vertex_number, ' '.join(
            str(x) for x in sorted(set(results[vertex_number]['r'])))

    print "diameter distibution:"
    for vertex_number in results:
        print vertex_number, ' '.join(
            str(x) for x in sorted(set(results[vertex_number]['d'])))

    print "diameter shifts:"
    print_shifts(results, 'd', lambda n: (n - 20) / 6 + 5, 9)

    plot(alpha[0], alpha[1], "alpha")
    plot(radius[0], radius[1], "radius")
    plot(diameter[0], diameter[1], "diameter")

    dump_as_csv(zip(alpha[0], alpha[1]), "alpha.csv")
    dump_as_csv(zip(radius[0], radius[1]), "radius.csv")
    dump_as_csv(zip(diameter[0], diameter[1]), "diameter.csv")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-from', dest='f', default='./out')
    parser.add_argument('-out', dest='out', default='out.json')

    args = parser.parse_args()
    with open(args.out, 'wb') as f:
        r = load(args.f)
        json.dump(r, f)
        plot_distribution(r)


main()
