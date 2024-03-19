

#!/usr/bin/python
from datetime import datetime
from mrjob.job import MRJob
import math
elapsed_time=0

def cos(query, doc):
    if len(query) == 0:
        return 0
    ans = 0
    fenmu1 = 0
    fenmu2 = 0
    for col in doc:
        fenmu2 += doc[col]**2  # Correctly calculate fenmu2 with doc vector
        if col in query:
            ans += query[col] * doc[col]
    for col in query:
        fenmu1 += query[col]**2  # Correctly calculate fenmu1 with query vector
    fenmu1 = math.sqrt(fenmu1)
    fenmu2 = math.sqrt(fenmu2)
    fenmu = fenmu1 * fenmu2
    return ans / fenmu if fenmu else 0

class MRWordFrequencyCount(MRJob):
    elapsed_time = 0
    def configure_args(self):
        super(MRWordFrequencyCount, self).configure_args()
        self.add_passthru_arg("-n", "--query", help="Input query information", type=str, default='{}')

    def mapper(self, _, line):
        single_line = line.rstrip().split("\t")
        for l in single_line:
            row, col, value = l.rstrip().split(",")
            yield row, (col, value)  # Emit document ID and term-frequency tuple

    def reducer(self, key, values):
        s = datetime.now()
        doc_info = {}
        for v in values:
            col, value = int(v[0]), float(v[1])
            doc_info[col] = value
        stems = self.options.query.split('/')
        query = {}
        stems.pop(-1)
        for stem in stems:
            two = stem.split(',')
            query[int(two[0])] = float(two[1])
        res = cos(query, doc_info)
        e = datetime.now()
        self.elapsed_time += (e-s).microseconds
        if res >= 0.001:  # More straightforward comparison
            yield self.elapsed_time, 1

if __name__ == '__main__':
    a = MRWordFrequencyCount()
    a.run()
    print("Execution Time = " + str(elapsed_time)+"ms")
