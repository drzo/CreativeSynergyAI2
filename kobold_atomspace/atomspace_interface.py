import random
from collections import defaultdict, deque
import heapq

class AtomSpaceInterface:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(set)

    # ... (keep existing methods)

    def find_diverse_paths(self, start, end, num_paths=3, max_depth=5):
        diverse_paths = []
        visited = set()

        def dfs(node, path, depth):
            if node == end:
                return path
            if depth >= max_depth or node in visited:
                return None
            visited.add(node)
            for neighbor in self.edges[node]:
                result = dfs(neighbor, path + [neighbor], depth + 1)
                if result:
                    return result
            visited.remove(node)
            return None

        def bfs():
            queue = deque([(start, [start])])
            while queue:
                node, path = queue.popleft()
                if node == end:
                    return path
                for neighbor in self.edges[node]:
                    if neighbor not in path:
                        queue.append((neighbor, path + [neighbor]))
            return None

        def random_walk():
            path = [start]
            current = start
            while current != end and len(path) <= max_depth:
                if not self.edges[current]:
                    break
                current = random.choice(list(self.edges[current]))
                path.append(current)
            return path if current == end else None

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
        common = set(path1) & set(path2)
        return len(common) / max(len(path1), len(path2))

    # ... (keep other existing methods)
