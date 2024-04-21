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


# Adjacency list for graph from Cormen's book
graph = [[0, 16, 13, 0, 0, 0],
         [0, 0, 10, 12, 0, 0],
         [0, 4, 0, 0, 14, 0],
         [0, 0, 9, 0, 0, 20],
         [0, 0, 0, 7, 0, 4],
         [0, 0, 0, 0, 0, 0]]

g = Graph(graph)
source = 0
sink = 5

print("Max Flow:", g.ford_fulkerson(source, sink))


# Visualization
G = nx.DiGraph()
for i in range(len(graph)):
    G.add_node(i)

for i in range(len(graph)):
    for j in range(len(graph[i])):
        if graph[i][j] > 0:
            G.add_edge(i, j, capacity=graph[i][j])

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue', font_weight='bold', node_size=2000)
edge_labels = {(i, j): G.get_edge_data(i, j)['capacity'] for i, j in G.edges()}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.show()
