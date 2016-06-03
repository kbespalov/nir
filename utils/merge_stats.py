import os
import json

import matplotlib.pyplot as plt
import numpy as np

stats_folder = '../out'


def load_results():
    # X,Y points
    alpha = [[], []]
    diameter = [[], []]
    radius = [[], []]

    for fname in os.listdir(stats_folder):
        # vertex number
        v = int(fname.split('_')[0])
        with open(os.path.join(stats_folder, fname)) as f:
            print fname
            res = json.load(f)

            for a in res['a']:
                alpha[0].append(v)
                alpha[1].append(a)

            for r in res['r']:
                radius[0].append(v)
                radius[1].append(r)

            for d in res['d']:
                diameter[0].append(v)
                diameter[1].append(d)

    return alpha, diameter, radius


alpha, diameter, radius = load_results()
plt.scatter(x=alpha[0], y=alpha[1])
plt.xticks(np.arange(min(alpha[0]), max(alpha[0]) + 1, 2.0))
plt.show()

print sorted(set(alpha[1]))
print sorted(set(diameter[1]))
print sorted(set(radius[1]))
