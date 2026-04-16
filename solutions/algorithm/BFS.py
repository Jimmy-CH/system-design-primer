from collections import deque


class Node(object):

    def __init__(self, value):
        self.value = value
        self.neighbors = []

    def add_neighbor(self, node):
        """添加邻接节点"""
        if node not in self.neighbors:
            self.neighbors.append(node)

    def __repr__(self):
        return f'Node({self.value})'


class BFS(object):

    def __init__(self):
        self.visited = set()
        self.result = []

    def iterative(self, start_node):
        """迭代实现的广度优先搜索（使用队列）

        Args:
            start_node: 起始节点

        Returns:
            BFS 遍历结果的列表
        """
        if start_node is None:
            return []

        self.visited.clear()
        self.result.clear()
        queue = deque([start_node])

        while queue:
            node = queue.popleft()

            if node not in self.visited:
                self.visited.add(node)
                self.result.append(node.value)

                for neighbor in node.neighbors:
                    if neighbor not in self.visited:
                        queue.append(neighbor)

        return self.result

    def level_order(self, start_node):
        """分层实现的广度优先搜索

        Args:
            start_node: 起始节点

        Returns:
            按层级返回的 BFS 遍历结果 [[level1], [level2], ...]
        """
        if start_node is None:
            return []

        self.visited.clear()
        self.result.clear()
        result_by_level = []
        queue = deque([start_node])
        self.visited.add(start_node)

        while queue:
            level_size = len(queue)
            current_level = []

            for _ in range(level_size):
                node = queue.popleft()
                current_level.append(node.value)

                for neighbor in node.neighbors:
                    if neighbor not in self.visited:
                        self.visited.add(neighbor)
                        queue.append(neighbor)

            result_by_level.append(current_level)

        return result_by_level


# 用于图的 BFS 实现（使用邻接表）
class GraphBFS(object):

    def __init__(self):
        self.visited = set()
        self.result = []

    def iterative(self, graph, start):
        """迭代实现的图 BFS

        Args:
            graph: 邻接表表示的图 {node: [neighbors]}
            start: 起始节点

        Returns:
            BFS 遍历结果的列表
        """
        if start not in graph:
            return []

        self.visited.clear()
        self.result.clear()
        queue = deque([start])

        while queue:
            node = queue.popleft()

            if node not in self.visited:
                self.visited.add(node)
                self.result.append(node)

                for neighbor in graph.get(node, []):
                    if neighbor not in self.visited:
                        queue.append(neighbor)

        return self.result


# 用于二叉树的 BFS 实现（层序遍历）
class TreeNode(object):

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def __repr__(self):
        return f'TreeNode({self.value})'


class TreeBFS(object):

    def level_order(self, root):
        """层序遍历（从上到下，从左到右）

        Args:
            root: 树的根节点

        Returns:
            遍历结果的列表
        """
        if root is None:
            return []

        result = []
        queue = deque([root])

        while queue:
            node = queue.popleft()
            result.append(node.value)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        return result

    def level_order_by_levels(self, root):
        """分层返回的层序遍历

        Args:
            root: 树的根节点

        Returns:
            按层级返回的遍历结果 [[level1], [level2], ...]
        """
        if root is None:
            return []

        result = []
        queue = deque([root])

        while queue:
            level_size = len(queue)
            current_level = []

            for _ in range(level_size):
                node = queue.popleft()
                current_level.append(node.value)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            result.append(current_level)

        return result

    def level_order_reverse(self, root):
        """从下到上的层序遍历

        Args:
            root: 树的根节点

        Returns:
            从下到上按层级返回的遍历结果
        """
        if root is None:
            return []

        result = []
        queue = deque([root])

        while queue:
            level_size = len(queue)
            current_level = []

            for _ in range(level_size):
                node = queue.popleft()
                current_level.append(node.value)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            result.insert(0, current_level)

        return result

    def zigzag_level_order(self, root):
        """之字形层序遍历（奇数层从左到右，偶数层从右到左）

        Args:
            root: 树的根节点

        Returns:
            之字形遍历结果
        """
        if root is None:
            return []

        result = []
        queue = deque([root])
        left_to_right = True

        while queue:
            level_size = len(queue)
            current_level = []

            for _ in range(level_size):
                node = queue.popleft()

                if left_to_right:
                    current_level.append(node.value)
                else:
                    current_level.insert(0, node.value)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            result.append(current_level)
            left_to_right = not left_to_right

        return result


# 测试代码
if __name__ == '__main__':
    print('===== 图的 BFS 遍历 =====')
    # 创建图
    #     1
    #    /|\
    #   2 3 4
    #   |   |
    #   5   6
    node1 = Node(1)
    node2 = Node(2)
    node3 = Node(3)
    node4 = Node(4)
    node5 = Node(5)
    node6 = Node(6)

    node1.add_neighbor(node2)
    node1.add_neighbor(node3)
    node1.add_neighbor(node4)
    node2.add_neighbor(node5)
    node4.add_neighbor(node6)

    bfs = BFS()
    print('迭代 BFS:', bfs.iterative(node1))          # [1, 2, 3, 4, 5, 6]
    print('分层 BFS:', bfs.level_order(node1))         # [[1], [2, 3, 4], [5, 6]]

    print('\n===== 二叉树的 BFS 遍历 =====')
    # 创建二叉树
    #      1
    #     / \
    #    2   3
    #   / \   \
    #  4   5   6
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    root.right.right = TreeNode(6)

    tree_bfs = TreeBFS()
    print('层序遍历:', tree_bfs.level_order(root))                # [1, 2, 3, 4, 5, 6]
    print('分层遍历:', tree_bfs.level_order_by_levels(root))       # [[1], [2, 3], [4, 5, 6]]
    print('反向分层:', tree_bfs.level_order_reverse(root))        # [[4, 5, 6], [2, 3], [1]]
    print('之字形遍历:', tree_bfs.zigzag_level_order(root))       # [[1], [3, 2], [4, 5, 6]]
