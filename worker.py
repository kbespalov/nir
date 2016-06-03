import json
import os

import signal
import uuid


class GraphProcessor(object):
    def __init__(self, queue, output):
        self.name = str(uuid.uuid4())
        self.results = {}
        self.queue = queue
        self.output_path = output
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

    def run(self):
        import sys
        import os
        file_name = os.path.basename(sys.argv[0])
        print file_name
        signal.signal(signal.SIGINT, self.signal_handler)
        while True:
            graph = self.queue.get()
            self.calculate_invariants(graph)

    def signal_handler(self, sig, frame):
        print 'SIGNAL HANDLED'
        self.dump()

    def dump(self):
        for k in self.results:
            dfile = os.path.join(self.output_path, str(k) + "_" + self.name)
            with open(dfile, 'wb') as result_file:
                json.dump(self.results[k], result_file)
        self.results.clear()

    def calculate_invariants(self, g):
        if g.vcount() not in self.results:
            self.dump()
            self.results[g.vcount()] = {'a': [], 'd': [], 'r': []}
        vdb = self.results[g.vcount()]
        vdb['a'].append(g.alpha())
        vdb['d'].append(g.diameter())
        vdb['r'].append(g.radius())
        print 'Processed %s' % str(g.vcount())
