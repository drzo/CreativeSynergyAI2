import random
from collections import defaultdict, deque
import heapq

class AtomSpaceInterface:
    def __init__(self):
        self.user_nodes = defaultdict(lambda: defaultdict(set))
        self.user_edges = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))

    def add_node(self, node, user_id):
        self.user_nodes[user_id][node.lower()].add(node)

    def add_edge(self, node1, node2, user_id):
        self.user_edges[user_id][node1.lower()][node2.lower()].add((node1, node2))
        self.user_edges[user_id][node2.lower()][node1.lower()].add((node2, node1))

    def find_diverse_paths(self, start, end, user_id, num_paths=3, max_depth=5):
        diverse_paths = []
        visited = set()

        def dfs(node, path, depth):
            if node.lower() == end.lower():
                return path
            if depth >= max_depth or node.lower() in visited:
                return None
            visited.add(node.lower())
            for neighbor_lower in self.user_edges[user_id][node.lower()]:
                for neighbor, _ in self.user_edges[user_id][node.lower()][neighbor_lower]:
                    result = dfs(neighbor, path + [neighbor], depth + 1)
                    if result:
                        return result
            visited.remove(node.lower())
            return None

        def bfs():
            queue = deque([(start, [start])])
            visited = set()
            while queue:
                node, path = queue.popleft()
                if node.lower() == end.lower():
                    return path
                if node.lower() in visited:
                    continue
                visited.add(node.lower())
                for neighbor_lower in self.user_edges[user_id][node.lower()]:
                    for neighbor, _ in self.user_edges[user_id][node.lower()][neighbor_lower]:
                        if neighbor.lower() not in visited:
                            queue.append((neighbor, path + [neighbor]))
            return None

        def random_walk():
            path = [start]
            current = start
            visited = set()
            while current.lower() != end.lower() and len(path) <= max_depth:
                visited.add(current.lower())
                neighbors = [neighbor for neighbor_lower in self.user_edges[user_id][current.lower()]
                             for neighbor, _ in self.user_edges[user_id][current.lower()][neighbor_lower]
                             if neighbor.lower() not in visited]
                if not neighbors:
                    break
                current = random.choice(neighbors)
                path.append(current)
            return path if current.lower() == end.lower() else None

        # Collect paths using different methods
        dfs_path = dfs(start, [start], 0)
        if dfs_path:
            diverse_paths.append(dfs_path)

        bfs_path = bfs()
        if bfs_path and (not diverse_paths or bfs_path != diverse_paths[0]):
            diverse_paths.append(bfs_path)

        while len(diverse_paths) < num_paths:
            rw_path = random_walk()
            if rw_path and self._is_diverse(rw_path, diverse_paths):
                diverse_paths.append(rw_path)

        return diverse_paths

    def _is_diverse(self, new_path, existing_paths, threshold=0.5):
        if not existing_paths:
            return True
        for path in existing_paths:
            if self._path_similarity(new_path, path) > threshold:
                return False
        return True

    def _path_similarity(self, path1, path2):
        common = set(node.lower() for node in path1) & set(node.lower() for node in path2)
        return len(common) / max(len(path1), len(path2))

    def get_user_nodes(self, user_id):
        return list({node for nodes in self.user_nodes[user_id].values() for node in nodes})

    def get_user_edges(self, user_id):
        return [(node1, node2) for node1_lower in self.user_edges[user_id]
                for node2_lower in self.user_edges[user_id][node1_lower]
                for node1, node2 in self.user_edges[user_id][node1_lower][node2_lower]]

    def get_user_graph_summary(self, user_id):
        nodes = self.get_user_nodes(user_id)
        edges = self.get_user_edges(user_id)
        return {
            'node_count': len(nodes),
            'edge_count': len(edges),
            'top_nodes': self._get_top_nodes(user_id, 5)
        }

    def _get_top_nodes(self, user_id, n):
        node_connections = defaultdict(int)
        for node1_lower in self.user_edges[user_id]:
            for node2_lower in self.user_edges[user_id][node1_lower]:
                node_connections[node1_lower] += len(self.user_edges[user_id][node1_lower][node2_lower])
                node_connections[node2_lower] += len(self.user_edges[user_id][node1_lower][node2_lower])
        return sorted(node_connections.items(), key=lambda x: x[1], reverse=True)[:n]

    # Add more methods as needed for other graph operations
