import random
# we need to install networkx
import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self, graph):
        self.graph = graph
        self.vertices_count = len(graph)

    def bfs(self, s, t, parent):
        visited = [False] * self.vertices_count
        queue = [s]
        visited[s] = True

        while queue:
            u = queue.pop(0)

            for ind, val in enumerate(self.graph[u]):
                if not visited[ind] and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u

        return visited[t]

    def ford_fulkerson(self, source, sink):
        parent = [-1] * self.vertices_count
        max_flow = 0

        while self.bfs(source, sink, parent):
            path_flow = float("Inf")
            s = sink
            while s != source:
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            max_flow += path_flow
            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]

        return max_flow


def random_graph_generator():
    vertex_collection = random.randint(2, 5)
    weight = random.randint(10, 20)
    graph = [[0] * vertex_collection for _ in range(vertex_collection)]

    for i in range(vertex_collection):
        for j in range(vertex_collection):
            new_weight = random.randint(0, weight)
            graph[i][j] = new_weight

    for i in range(vertex_collection):
        graph[i][i] = 0

    return graph, vertex_collection, weight


def print_graph(graph):
    for row in graph:
        print(row)


random_graph = Graph(random_graph_generator())
source = 0
endpoint = random_graph.vertices_count - 1
print("Min Flow:", random_graph.ford_fulkerson(source, endpoint))


# Visualization
G = nx.DiGraph()
for i in range(len(random_graph)):
    G.add_node(i)

for i in range(len(random_graph)):
    for j in range(len(random_graph[i])):
        if random_graph[i][j] > 0:
            G.add_edge(i, j, capacity=random_graph[i][j])

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue', font_weight='bold', node_size=2000)
edge_labels = {(i, j): G.get_edge_data(i, j)['capacity'] for i, j in G.edges()}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.show()
