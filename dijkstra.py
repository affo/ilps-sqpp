INF = float('inf')

def run(graph, vertex):
    res = [INF for _ in xrange(graph.n)]
    is_shortest = [False for _ in xrange(graph.n)]

    res[vertex] = 0

    while not all(is_shortest):
        not_sure_distances = [
                res[i]
                if not is_shortest[i] else INF
                for i in xrange(graph.n)
        ]

        nearest_d = min(not_sure_distances)
        nearest = not_sure_distances.index(nearest_d)
        is_shortest[nearest] = True

        neighbors = graph.enumerate(nearest)

        for n, w in neighbors:
            new_distance = nearest_d + w
            if new_distance < res[n]:
                res[n] = new_distance

    return res
