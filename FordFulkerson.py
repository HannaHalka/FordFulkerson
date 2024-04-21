import random
# we need to install networkx and matplotlib
import networkx as nx
import matplotlib.pyplot as plt
import time
from google.oauth2 import service_account
import googleapiclient.discovery


#SCOPES = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
#SERVICE_ACCOUNT_FILE = # code was deleted because of id and other confidential keys for google sheets

#credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
#service = googleapiclient.discovery.build('sheets', 'v4', credentials=credentials)
#creds_with_scope = credentials.with_scopes(SCOPES)

class FordFulkersonImpl:
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
    #vertex_collection = random.randint(50, 100)
    vertex_collection = 5
    #weight = random.randint(20, 30)  # max weight
    weight = 30

    #density = random.randint(40, 100) / 100
    density = 0.75
    edges = int((vertex_collection * (vertex_collection - 1) * density) / 2)

    graph = [[0] * vertex_collection for _ in range(vertex_collection)]
    edges_collection = set()

    for _ in range(edges):
        i, j = random.sample(range(vertex_collection), 2) # takes 2 v and creates edge
        if (i, j) not in edges_collection:
            new_weight = random.randint(1, weight)
            graph[i][j] = new_weight
            edges_collection.add((i, j))

    for i in range(vertex_collection):
        graph[i][i] = 0

    return graph, vertex_collection


def print_graph(graph):
    for row in graph:
        print(row)


#def write_to_sheet(data):
    # code was deleted because of id and other confidential keys for google sheets


NUM_RUNS = 1

for _ in range(NUM_RUNS):
    random_graph, vertex_count = random_graph_generator()
    ff = FordFulkersonImpl(random_graph)

    #######################################
    start_time = time.time()
    #######################################

    source = 0
    endpoint = vertex_count - 1
    max_flow = ff.ford_fulkerson(source, endpoint)

    #######################################
    elapsed_time = time.time() - start_time
    #######################################

    print("Max Flow:", max_flow, "Time: ", elapsed_time)
    #write_to_sheet(elapsed_time)

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

