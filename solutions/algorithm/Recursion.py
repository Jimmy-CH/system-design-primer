"""
递归算法实现
包含多种经典的递归问题解决方案
"""


class Recursion(object):

    # ====== 基础递归示例 ======

    @staticmethod
    def factorial(n):
        """计算阶乘 n!

        Args:
            n: 正整数

        Returns:
            n! 的值

        Raises:
            ValueError: 当 n 为负数时
        """
        if n < 0:
            raise ValueError('n must be non-negative')
        if n <= 1:
            return 1
        return n * Recursion.factorial(n - 1)

    @staticmethod
    def fibonacci(n):
        """计算斐波那契数列第 n 项

        Args:
            n: 正整数（从0开始）

        Returns:
            斐波那契数列第 n 项
        """
        if n <= 0:
            return 0
        if n == 1:
            return 1
        return Recursion.fibonacci(n - 1) + Recursion.fibonacci(n - 2)

    @staticmethod
    def fibonacci_optimized(n, memo=None):
        """优化的斐波那契数列（记忆化搜索）

        Args:
            n: 正整数
            memo: 记忆化字典

        Returns:
            斐波那契数列第 n 项
        """
        if memo is None:
            memo = {}
        if n in memo:
            return memo[n]
        if n <= 0:
            return 0
        if n == 1:
            return 1
        memo[n] = Recursion.fibonacci_optimized(n - 1, memo) + Recursion.fibonacci_optimized(n - 2, memo)
        return memo[n]

    # ====== 字符串递归 ======

    @staticmethod
    def reverse_string(s):
        """递归反转字符串

        Args:
            s: 字符串

        Returns:
            反转后的字符串
        """
        if len(s) <= 1:
            return s
        return Recursion.reverse_string(s[1:]) + s[0]

    @staticmethod
    def is_palindrome(s):
        """递归判断字符串是否为回文

        Args:
            s: 字符串

        Returns:
            True 如果是回文，否则 False
        """
        s = s.lower().replace(' ', '')
        if len(s) <= 1:
            return True
        if s[0] != s[-1]:
            return False
        return Recursion.is_palindrome(s[1:-1])

    # ====== 数组/列表递归 ======

    @staticmethod
    def binary_search(arr, target, left=0, right=None):
        """递归二分查找

        Args:
            arr: 已排序的数组
            target: 目标值
            left: 左边界
            right: 右边界

        Returns:
            目标值的索引，如果未找到返回 -1
        """
        if right is None:
            right = len(arr) - 1

        if left > right:
            return -1

        mid = (left + right) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] > target:
            return Recursion.binary_search(arr, target, left, mid - 1)
        else:
            return Recursion.binary_search(arr, target, mid + 1, right)

    @staticmethod
    def sum_array(arr, index=0):
        """递归计算数组元素和

        Args:
            arr: 数组
            index: 当前索引

        Returns:
            数组元素和
        """
        if index >= len(arr):
            return 0
        return arr[index] + Recursion.sum_array(arr, index + 1)

    @staticmethod
    def find_max(arr, index=0):
        """递归查找数组最大值

        Args:
            arr: 数组
            index: 当前索引

        Returns:
            数组最大值
        """
        if index == len(arr) - 1:
            return arr[index]
        sub_max = Recursion.find_max(arr, index + 1)
        return arr[index] if arr[index] > sub_max else sub_max

    @staticmethod
    def quick_sort(arr):
        """递归快速排序

        Args:
            arr: 待排序数组

        Returns:
            排序后的数组
        """
        if len(arr) <= 1:
            return arr

        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]

        return Recursion.quick_sort(left) + middle + Recursion.quick_sort(right)

    @staticmethod
    def merge_sort(arr):
        """递归归并排序

        Args:
            arr: 待排序数组

        Returns:
            排序后的数组
        """
        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        left = Recursion.merge_sort(arr[:mid])
        right = Recursion.merge_sort(arr[mid:])

        return Recursion._merge(left, right)

    @staticmethod
    def _merge(left, right):
        """归并两个有序数组"""
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result

    # ====== 数学递归 ======

    @staticmethod
    def power(base, exponent):
        """递归计算幂运算

        Args:
            base: 底数
            exponent: 指数

        Returns:
            base^exponent
        """
        if exponent == 0:
            return 1
        if exponent < 0:
            return 1 / Recursion.power(base, -exponent)
        if exponent % 2 == 0:
            half = Recursion.power(base, exponent // 2)
            return half * half
        else:
            return base * Recursion.power(base, exponent - 1)

    @staticmethod
    def gcd(a, b):
        """递归计算最大公约数（欧几里得算法）

        Args:
            a: 第一个数
            b: 第二个数

        Returns:
            a 和 b 的最大公约数
        """
        if b == 0:
            return a
        return Recursion.gcd(b, a % b)

    @staticmethod
    def hanoi(n, source, auxiliary, target, moves=None):
        """汉诺塔问题

        Args:
            n: 圆盘数量
            source: 源柱子
            auxiliary: 辅助柱子
            target: 目标柱子
            moves: 移动步骤列表

        Returns:
            移动步骤列表
        """
        if moves is None:
            moves = []

        if n == 1:
            moves.append(f'{source} -> {target}')
            return moves

        # 将 n-1 个圆盘从源柱子移到辅助柱子
        Recursion.hanoi(n - 1, source, target, auxiliary, moves)
        # 将第 n 个圆盘从源柱子移到目标柱子
        moves.append(f'{source} -> {target}')
        # 将 n-1 个圆盘从辅助柱子移到目标柱子
        Recursion.hanoi(n - 1, auxiliary, source, target, moves)

        return moves

    # ====== 树的递归 ======

    @staticmethod
    def tree_height(root):
        """递归计算二叉树高度

        Args:
            root: 二叉树根节点

        Returns:
            树的高度
        """
        if root is None:
            return 0
        left_height = Recursion.tree_height(root.left)
        right_height = Recursion.tree_height(root.right)
        return max(left_height, right_height) + 1

    @staticmethod
    def tree_size(root):
        """递归计算二叉树节点数

        Args:
            root: 二叉树根节点

        Returns:
            节点总数
        """
        if root is None:
            return 0
        return 1 + Recursion.tree_size(root.left) + Recursion.tree_size(root.right)

    @staticmethod
    def tree_mirror(root):
        """递归翻转二叉树

        Args:
            root: 二叉树根节点

        Returns:
            翻转后的二叉树根节点
        """
        if root is None:
            return None

        # 交换左右子树
        root.left, root.right = root.right, root.left

        # 递归翻转左右子树
        Recursion.tree_mirror(root.left)
        Recursion.tree_mirror(root.right)

        return root

    @staticmethod
    def same_tree(p, q):
        """递归判断两棵二叉树是否相同

        Args:
            p: 第一棵树的根节点
            q: 第二棵树的根节点

        Returns:
            True 如果两棵树相同，否则 False
        """
        if p is None and q is None:
            return True
        if p is None or q is None:
            return False
        if p.value != q.value:
            return False
        return Recursion.same_tree(p.left, q.left) and Recursion.same_tree(p.right, q.right)

    @staticmethod
    def is_valid_bst(root, min_val=float('-inf'), max_val=float('inf')):
        """递归判断是否为有效的二叉搜索树

        Args:
            root: 二叉树根节点
            min_val: 最小值边界
            max_val: 最大值边界

        Returns:
            True 如果是有效的 BST，否则 False
        """
        if root is None:
            return True

        if root.value <= min_val or root.value >= max_val:
            return False

        return (Recursion.is_valid_bst(root.left, min_val, root.value) and
                Recursion.is_valid_bst(root.right, root.value, max_val))

    # ====== 回溯算法 ======

    @staticmethod
    def permutations(nums):
        """生成全排列

        Args:
            nums: 数字列表

        Returns:
            所有可能的排列
        """
        result = []

        def backtrack(path, remaining):
            if not remaining:
                result.append(path[:])
                return

            for i, num in enumerate(remaining):
                path.append(num)
                backtrack(path, remaining[:i] + remaining[i + 1:])
                path.pop()

        backtrack([], nums)
        return result

    @staticmethod
    def subsets(nums):
        """生成所有子集

        Args:
            nums: 数字列表

        Returns:
            所有可能的子集
        """
        result = []

        def backtrack(index, current):
            result.append(current[:])

            for i in range(index, len(nums)):
                current.append(nums[i])
                backtrack(i + 1, current)
                current.pop()

        backtrack(0, [])
        return result

    @staticmethod
    def generate_parentheses(n):
        """生成有效的括号组合

        Args:
            n: 括号对数

        Returns:
            所有可能的括号组合
        """
        result = []

        def backtrack(current, open_count, close_count):
            if len(current) == 2 * n:
                result.append(current)
                return

            if open_count < n:
                backtrack(current + '(', open_count + 1, close_count)

            if close_count < open_count:
                backtrack(current + ')', open_count, close_count + 1)

        backtrack('', 0, 0)
        return result


class TreeNode(object):
    """二叉树节点"""

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def __repr__(self):
        return f'TreeNode({self.value})'


# 测试代码
if __name__ == '__main__':
    print('===== 基础递归 =====')
    print('5! =', Recursion.factorial(5))  # 120
    print('Fibonacci(10) =', Recursion.fibonacci(10))  # 55
    print('Fibonacci优化(10) =', Recursion.fibonacci_optimized(10))  # 55

    print('\n===== 字符串递归 =====')
    print('反转 "hello" =', Recursion.reverse_string('hello'))  # olleh
    print('回文 "racecar" =', Recursion.is_palindrome('racecar'))  # True
    print('回文 "hello" =', Recursion.is_palindrome('hello'))  # False

    print('\n===== 数组递归 =====')
    arr = [1, 3, 5, 7, 9]
    print('二分查找 5:', Recursion.binary_search(arr, 5))  # 2
    print('数组求和 [1,2,3,4,5]:', Recursion.sum_array([1, 2, 3, 4, 5]))  # 15
    print('查找最大值 [3,1,4,1,5,9]:', Recursion.find_max([3, 1, 4, 1, 5, 9]))  # 9
    print('快速排序 [3,1,4,1,5,9]:', Recursion.quick_sort([3, 1, 4, 1, 5, 9]))  # [1,1,3,4,5,9]

    print('\n===== 数学递归 =====')
    print('2^10 =', Recursion.power(2, 10))  # 1024
    print('GCD(48, 18) =', Recursion.gcd(48, 18))  # 6
    print('汉诺塔(3):', Recursion.hanoi(3, 'A', 'B', 'C'))

    print('\n===== 树的递归 =====')
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

    print('树高度:', Recursion.tree_height(root))  # 3
    print('树节点数:', Recursion.tree_size(root))  # 5

    print('\n===== 回溯算法 =====')
    print('全排列 [1,2,3]:', Recursion.permutations([1, 2, 3]))
    print('子集 [1,2]:', Recursion.subsets([1, 2]))
    print('括号组合(2):', Recursion.generate_parentheses(2))  # ['(())', '()()']
