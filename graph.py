'''
    Generating random Graphs basing on Erdos-Renyi model
    https://en.wikipedia.org/wiki/Erd%C5%91s%E2%80%93R%C3%A9nyi_model
'''
import random


class Graph(object):
    def __init__(self, n, p, w=1):
        '''
            Creates a new `DataStructure` representing a graph
            with `n` vertices (labeled with incremental integers)
            and probability of connection `p`.
            The weight of the edge will be at maximum `w` (uniformly
            distributed).
        '''
        self.n = n

        if p < 0: p = 0
        if p > 1: p = 1

        self.p = p
        self.w = w
        self.data = self._generate(n, p, w)

    def _generate(self, n, p, w):
        '''
            Generates  and returns it the internal representation
        '''
        pass

    def insert(self, edge):
        '''
            Creates and edge (a couple) between
            `edge[0]` and `edge[1]`.
        '''
        pass

    def delete(self, edge):
        '''
            Deletes the edge (if it exists) between
            `edge[0]` and `edge[1]`.
        '''
        pass

    def find(self, edge):
        '''
            Returns if `edge[0]` and `edge[1]` are connected.
        '''
        pass

    def enumerate(self, vertex):
        '''
            Returns the neighbors of `vertex`
        '''
        pass


class AdjMatrixGraph(Graph):
    def __repr__(self):
        r = '\t'
        r += '\t'.join([str(i) for i in xrange(self.n)])
        r += '\n\t'
        r += '\t'.join(['|' for i in xrange(self.n)])
        r += '\n'

        for i, row in enumerate(self.data):
            r += str(i) + ' --\t'
            r += '\t'.join([str(el) for el in row])
            r += '\n'

        return r

    def _generate(self, n, p, w):
        m = [[0 for _ in xrange(n)] for _ in xrange(n)]

        # given that the graph has always to be
        # be connected, we have to create a random
        # path from vertex 0 to n:
        vertices = list(xrange(n))
        fromv = random.choice(vertices)
        vertices.remove(fromv)

        while len(vertices) > 0:
            tov = random.choice(vertices)

            # ensure connection
            m[fromv][tov] = random.randint(1, w)
            m[tov][fromv] = m[fromv][tov]

            fromv = tov
            vertices.remove(fromv)

        # now, we can add connections based
        # on probability
        for i in xrange(n - 1):
            for j in xrange(i + 1, n):
                if not m[i][j] > 0 and random.random() < p:
                    m[i][j] = random.randint(1, w)
                    m[j][i] = m[i][j]

        return m

    def insert(self, edge):
        i = edge[0]
        j = edge[1]
        self.data[i][j] = random.randint(1, self.w)
        self.data[j][i] = self.data[i][j]

    def delete(self, edge):
        i = edge[0]
        j = edge[1]
        self.data[i][j] = 0
        self.data[j][i] = 0

    def find(self, edge):
        i = edge[0]
        j = edge[1]
        return self.data[i][j] > 0

    def enumerate(self, vertex):
        return [(i, v) for i, v in enumerate(self.data[vertex]) if v > 0]

