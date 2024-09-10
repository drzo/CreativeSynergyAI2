import random
from collections import defaultdict, deque
import heapq
from datetime import datetime
from sklearn.cluster import KMeans
import numpy as np

class AtomSpaceInterface:
    def __init__(self):
        self.user_nodes = defaultdict(lambda: defaultdict(set))
        self.user_edges = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))
        self.user_node_timestamps = defaultdict(lambda: defaultdict(datetime))
        self.user_edge_timestamps = defaultdict(lambda: defaultdict(lambda: defaultdict(datetime)))

    def add_node(self, node, user_id):
        self.user_nodes[user_id][node.lower()].add(node)
        self.user_node_timestamps[user_id][node.lower()] = datetime.now()

    def add_edge(self, node1, node2, user_id):
        self.user_edges[user_id][node1.lower()][node2.lower()].add((node1, node2))
        self.user_edges[user_id][node2.lower()][node1.lower()].add((node2, node1))
        self.user_edge_timestamps[user_id][node1.lower()][node2.lower()] = datetime.now()
        self.user_edge_timestamps[user_id][node2.lower()][node1.lower()] = datetime.now()

    def get_user_nodes(self, user_id):
        return list({node for nodes in self.user_nodes[user_id].values() for node in nodes})

    def get_user_edges(self, user_id):
        return [(node1, node2) for node1_lower in self.user_edges[user_id]
                for node2_lower in self.user_edges[user_id][node1_lower]
                for node1, node2 in self.user_edges[user_id][node1_lower][node2_lower]]

    def cluster_user_concepts(self, user_id):
        nodes = list(self.user_nodes[user_id].keys())
        if len(nodes) < 2:
            return []

        # Create a simple feature vector based on connections
        feature_vectors = []
        for node in nodes:
            connections = sum(len(self.user_edges[user_id][node][other]) for other in self.user_edges[user_id][node])
            feature_vectors.append([connections])

        # Perform K-means clustering
        n_clusters = min(5, len(nodes))  # Limit to 5 clusters or less
        kmeans = KMeans(n_clusters=n_clusters)
        kmeans.fit(feature_vectors)

        # Create cluster objects
        clusters = []
        for i in range(n_clusters):
            cluster_nodes = [nodes[j] for j in range(len(nodes)) if kmeans.labels_[j] == i]
            clusters.append({
                'id': i,
                'label': f'Cluster {i + 1}',
                'nodes': cluster_nodes
            })

        return clusters

    def generate_story_path(self, user_id, nodes):
        # Find the shortest path between the first and last node
        start = nodes[0]
        end = nodes[-1]
        path = self.find_shortest_path(user_id, start, end)

        # Generate a story based on the path
        story = f"Our journey begins with {start}. "
        for i in range(1, len(path)):
            story += f"From {path[i-1]}, we discover a connection to {path[i]}. "
        story += f"Finally, we reach our destination: {end}."

        return path, story

    def find_shortest_path(self, user_id, start, end):
        queue = deque([(start, [start])])
        visited = set()

        while queue:
            (node, path) = queue.popleft()
            if node not in visited:
                if node.lower() == end.lower():
                    return path
                visited.add(node.lower())
                for neighbor_lower in self.user_edges[user_id][node.lower()]:
                    for neighbor, _ in self.user_edges[user_id][node.lower()][neighbor_lower]:
                        if neighbor.lower() not in visited:
                            queue.append((neighbor, path + [neighbor]))
        return None

    def get_user_graph_for_time(self, user_id, timestamp):
        nodes = [node for node, node_timestamp in self.user_node_timestamps[user_id].items() if node_timestamp <= timestamp]
        edges = []
        for node1 in nodes:
            for node2 in self.user_edges[user_id][node1]:
                if node2 in nodes and self.user_edge_timestamps[user_id][node1][node2] <= timestamp:
                    edges.append((node1, node2))
        return nodes, edges

    def search_user_nodes(self, user_id, search_term):
        search_term = search_term.lower()
        matching_nodes = []
        for node_lower, nodes in self.user_nodes[user_id].items():
            if search_term in node_lower:
                matching_nodes.extend(nodes)
        return matching_nodes
