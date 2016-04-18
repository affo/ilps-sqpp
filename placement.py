import random, time

from pulp import *
from graph import AdjMatrixGraph as Graph
from dijkstra import run as dj

NETWORK_SIZE = 50
MAX_LATENCY = 5
MAX_NODE_CAPACITY = 8

# the DAG is like a rombus:
#  - the source
#  - numerator on top
#  - denominator on bottom
#  - merge on a divisor
#  - eventually, rank
# We add parallelism:
#  - 1 source
#  - 10 num
#  - 10 den
#  - 20 div
#  - 1 rank
# 42 operators
ops = list(xrange(42))

op_c = [1, ]
op_c.extend([1 for _ in xrange(10)])
op_c.extend([3 for _ in xrange(10)])
op_c.extend([2 for _ in xrange(20)])
op_c.append(5)

# building adjacency matrix
dag_am = []
dag_am.append([0] + [1] * (10 + 10) + [0] * 20 + [0])
nd_row = [0] + [0] * (10 + 10) + [1] * 20 + [0]
for _ in xrange(10 + 10):
    dag_am.append(nd_row)
div_row = [0] + [0] * (10 + 10) + [0] * 20 + [1]
for _ in xrange(20):
    dag_am.append(div_row)
dag_am.append([0] * len(ops))

# adjust capacities basing on the number of outgoing links
dag = Graph(5, 0)
# override graph data
dag.data = dag_am
for op in ops:
    outgoing = len(dag.enumerate(op))
    new_val = float(op_c[op])
    if outgoing > 0:
        new_val /= outgoing
    op_c[op] = new_val


# randomly generate hosting network
nodes = list(xrange(NETWORK_SIZE))
node_c = [random.randint(1, MAX_NODE_CAPACITY) for _ in xrange(NETWORK_SIZE)]
# adjust latencies making them minimum latencies (dijkstra)
network = Graph(NETWORK_SIZE, 0.5, MAX_LATENCY)
latencies = [dj(network, node) for node in nodes]

print '>>> Data correctly computed, instantiating problem...'
_start_p = time.time()

problem = LpProblem('Single-query Operator Placement', LpMinimize)
print '>>> Instantiating', problem.name, 'problem'
x = LpVariable.dicts('placement', (ops, ops, nodes, nodes), 0, 1, LpInteger)

# We should also
#    * tuple_flow[i][j]
# But, to make code less verbose, we remove it here.
# The tuple flow is needed only to get a more realistic solution
problem += lpSum([dag_am[i][j] * latencies[h][k] * x[i][j][h][k] \
        for i in ops for j in ops \
        for h in nodes for k in nodes]), 'The objective function'

# Every link in the dag is represented exactly once in the solution
for i in ops:
    for j in ops:
        problem += lpSum([x[i][j][h][k] for h in nodes for k in nodes]) == dag_am[i][j], ''

# Capacity exceeding limit
for h in nodes:
    problem += lpSum([x[i][j][h][k] * op_c[i] for i in ops for j in ops for k in nodes]) <= node_c[h], ''

_end_p = time.time()

print '>>> Solving', problem.name, 'problem'
print '>>> Network size:', NETWORK_SIZE
print '>>> Query size:', len(ops)
print '>>> #Variables:', problem.numVariables()
print '>>> #Constraints:', problem.numConstraints()
_start_s = time.time()
problem.solve()
_end_s = time.time()

# for v in problem.variables():
#     val = v.value()
#     if val > 0:
#         print v.name + ':', v.value()

print '>>> Finished'
print '>>> Status:', LpStatus[problem.status]
print '>>> Elapsed time for problem instantiation:', _end_p - _start_p, 'seconds'
print '>>> Elapsed time for problem solving:', _end_s - _start_s, 'seconds'
