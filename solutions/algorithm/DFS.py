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


class DFS(object):

    def __init__(self):
        self.visited = set()
        self.result = []

    def recursive(self, start_node):
        """递归实现的深度优先搜索

        Args:
            start_node: 起始节点

        Returns:
            DFS 遍历结果的列表
        """
        self.visited.clear()
        self.result.clear()
        self._recursive_helper(start_node)
        return self.result

    def _recursive_helper(self, node):
        """递归辅助函数"""
        if node is None:
            return

        self.visited.add(node)
        self.result.append(node.value)

        for neighbor in node.neighbors:
            if neighbor not in self.visited:
                self._recursive_helper(neighbor)

    def iterative(self, start_node):
        """迭代实现的深度优先搜索（使用栈）

        Args:
            start_node: 起始节点

        Returns:
            DFS 遍历结果的列表
        """
        if start_node is None:
            return []

        self.visited.clear()
        self.result.clear()
        stack = [start_node]

        while stack:
            node = stack.pop()

            if node not in self.visited:
                self.visited.add(node)
                self.result.append(node.value)

                # 将邻接节点按逆序入栈，保证按顺序访问
                for neighbor in reversed(node.neighbors):
                    if neighbor not in self.visited:
                        stack.append(neighbor)

        return self.result


# 用于图的 DFS 实现（使用邻接表）
class GraphDFS(object):

    def __init__(self):
        self.visited = set()
        self.result = []

    def recursive(self, graph, start):
        """递归实现的图 DFS

        Args:
            graph: 邻接表表示的图 {node: [neighbors]}
            start: 起始节点

        Returns:
            DFS 遍历结果的列表
        """
        self.visited.clear()
        self.result.clear()
        self._graph_recursive_helper(graph, start)
        return self.result

    def _graph_recursive_helper(self, graph, node):
        """递归辅助函数"""
        if node not in self.visited:
            self.visited.add(node)
            self.result.append(node)

            for neighbor in graph.get(node, []):
                self._graph_recursive_helper(graph, neighbor)

    def iterative(self, graph, start):
        """迭代实现的图 DFS

        Args:
            graph: 邻接表表示的图 {node: [neighbors]}
            start: 起始节点

        Returns:
            DFS 遍历结果的列表
        """
        if start not in graph:
            return []

        self.visited.clear()
        self.result.clear()
        stack = [start]

        while stack:
            node = stack.pop()

            if node not in self.visited:
                self.visited.add(node)
                self.result.append(node)

                # 将邻接节点按逆序入栈
                for neighbor in reversed(graph.get(node, [])):
                    if neighbor not in self.visited:
                        stack.append(neighbor)

        return self.result


# 用于二叉树的 DFS 实现
class TreeNode(object):

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def __repr__(self):
        return f'TreeNode({self.value})'


class TreeDFS(object):

    def preorder(self, root):
        """前序遍历（根-左-右）

        Args:
            root: 树的根节点

        Returns:
            遍历结果的列表
        """
        result = []
        self._preorder_helper(root, result)
        return result

    def _preorder_helper(self, node, result):
        if node is None:
            return
        result.append(node.value)
        self._preorder_helper(node.left, result)
        self._preorder_helper(node.right, result)

    def inorder(self, root):
        """中序遍历（左-根-右）

        Args:
            root: 树的根节点

        Returns:
            遍历结果的列表
        """
        result = []
        self._inorder_helper(root, result)
        return result

    def _inorder_helper(self, node, result):
        if node is None:
            return
        self._inorder_helper(node.left, result)
        result.append(node.value)
        self._inorder_helper(node.right, result)

    def postorder(self, root):
        """后序遍历（左-右-根）

        Args:
            root: 树的根节点

        Returns:
            遍历结果的列表
        """
        result = []
        self._postorder_helper(root, result)
        return result

    def _postorder_helper(self, node, result):
        if node is None:
            return
        self._postorder_helper(node.left, result)
        self._postorder_helper(node.right, result)
        result.append(node.value)


# 测试代码
if __name__ == '__main__':
    print('===== 图的 DFS 遍历 =====')
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

    dfs = DFS()
    print('递归 DFS:', dfs.recursive(node1))  # [1, 2, 5, 3, 4, 6]
    print('迭代 DFS:', dfs.iterative(node1))  # [1, 2, 5, 3, 4, 6]

    print('\n===== 二叉树的 DFS 遍历 =====')
    # 创建二叉树
    #      1
    #     / \
    #    2   3
    #   / \
    #  4   5
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)

    tree_dfs = TreeDFS()
    print('前序遍历:', tree_dfs.preorder(root))    # [1, 2, 4, 5, 3]
    print('中序遍历:', tree_dfs.inorder(root))     # [4, 2, 5, 1, 3]
    print('后序遍历:', tree_dfs.postorder(root))   # [4, 5, 2, 3, 1]
