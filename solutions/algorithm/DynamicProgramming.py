"""
动态规划算法实现
包含多种经典的动态规划问题解决方案
"""


class DynamicProgramming(object):

    # ====== 基础动态规划 ======

    @staticmethod
    def fibonacci(n):
        """动态规划求解斐波那契数列

        Args:
            n: 正整数

        Returns:
            斐波那契数列第 n 项
        """
        if n <= 0:
            return 0
        if n == 1:
            return 1

        dp = [0] * (n + 1)
        dp[0] = 0
        dp[1] = 1

        for i in range(2, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]

        return dp[n]

    @staticmethod
    def fibonacci_optimized(n):
        """空间优化的斐波那契数列

        Args:
            n: 正整数

        Returns:
            斐波那契数列第 n 项
        """
        if n <= 0:
            return 0
        if n == 1:
            return 1

        prev2, prev1 = 0, 1

        for _ in range(2, n + 1):
            current = prev1 + prev2
            prev2, prev1 = prev1, current

        return prev1

    @staticmethod
    def climb_stairs(n):
        """爬楼梯问题：每次可以爬1或2个台阶，有多少种方法到达顶部

        Args:
            n: 台阶数

        Returns:
            爬到顶部的方法数
        """
        if n <= 1:
            return 1

        dp = [0] * (n + 1)
        dp[0] = 1
        dp[1] = 1

        for i in range(2, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]

        return dp[n]

    # ====== 数组问题 ======

    @staticmethod
    def max_subarray(nums):
        """最大子数组和（Kadane算法）

        Args:
            nums: 整数数组

        Returns:
            最大子数组的和
        """
        if not nums:
            return 0

        dp = nums[0]
        max_sum = dp

        for i in range(1, len(nums)):
            dp = max(nums[i], dp + nums[i])
            max_sum = max(max_sum, dp)

        return max_sum

    @staticmethod
    def max_subarray_with_indices(nums):
        """最大子数组和（返回子数组索引）

        Args:
            nums: 整数数组

        Returns:
            (最大和, 起始索引, 结束索引)
        """
        if not nums:
            return 0, 0, 0

        dp = nums[0]
        max_sum = dp
        start = 0
        end = 0
        temp_start = 0

        for i in range(1, len(nums)):
            if nums[i] > dp + nums[i]:
                dp = nums[i]
                temp_start = i
            else:
                dp = dp + nums[i]

            if dp > max_sum:
                max_sum = dp
                start = temp_start
                end = i

        return max_sum, start, end

    @staticmethod
    def house_robber(nums):
        """打家劫舍：不能偷相邻的房屋，求最大金额

        Args:
            nums: 每个房屋的金额

        Returns:
            能偷到的最大金额
        """
        if not nums:
            return 0
        if len(nums) == 1:
            return nums[0]

        dp = [0] * len(nums)
        dp[0] = nums[0]
        dp[1] = max(nums[0], nums[1])

        for i in range(2, len(nums)):
            dp[i] = max(dp[i - 1], dp[i - 2] + nums[i])

        return dp[-1]

    @staticmethod
    def house_robber_optimized(nums):
        """空间优化的打家劫舍

        Args:
            nums: 每个房屋的金额

        Returns:
            能偷到的最大金额
        """
        if not nums:
            return 0
        if len(nums) == 1:
            return nums[0]

        prev2, prev1 = nums[0], max(nums[0], nums[1])

        for i in range(2, len(nums)):
            current = max(prev1, prev2 + nums[i])
            prev2, prev1 = prev1, current

        return prev1

    # ====== 背包问题 ======

    @staticmethod
    def knapsack_01(weights, values, capacity):
        """0/1背包问题：每个物品只能选一次

        Args:
            weights: 物品重量列表
            values: 物品价值列表
            capacity: 背包容量

        Returns:
            最大价值
        """
        n = len(weights)
        dp = [[0] * (capacity + 1) for _ in range(n + 1)]

        for i in range(1, n + 1):
            for w in range(capacity + 1):
                if weights[i - 1] <= w:
                    dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])
                else:
                    dp[i][w] = dp[i - 1][w]

        return dp[n][capacity]

    @staticmethod
    def knapsack_01_optimized(weights, values, capacity):
        """空间优化的0/1背包问题

        Args:
            weights: 物品重量列表
            values: 物品价值列表
            capacity: 背包容量

        Returns:
            最大价值
        """
        dp = [0] * (capacity + 1)

        for i in range(len(weights)):
            for w in range(capacity, weights[i] - 1, -1):
                dp[w] = max(dp[w], dp[w - weights[i]] + values[i])

        return dp[capacity]

    @staticmethod
    def unbounded_knapsack(weights, values, capacity):
        """完全背包问题：每个物品可以选多次

        Args:
            weights: 物品重量列表
            values: 物品价值列表
            capacity: 背包容量

        Returns:
            最大价值
        """
        dp = [0] * (capacity + 1)

        for w in range(capacity + 1):
            for i in range(len(weights)):
                if weights[i] <= w:
                    dp[w] = max(dp[w], dp[w - weights[i]] + values[i])

        return dp[capacity]

    # ====== 字符串问题 ======

    @staticmethod
    def longest_common_subsequence(text1, text2):
        """最长公共子序列（LCS）

        Args:
            text1: 第一个字符串
            text2: 第二个字符串

        Returns:
            最长公共子序列的长度
        """
        m, n = len(text1), len(text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        return dp[m][n]

    @staticmethod
    def longest_common_subsequence_with_sequence(text1, text2):
        """最长公共子序列（返回子序列）

        Args:
            text1: 第一个字符串
            text2: 第二个字符串

        Returns:
            最长公共子序列
        """
        m, n = len(text1), len(text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        # 回溯构建子序列
        lcs = []
        i, j = m, n
        while i > 0 and j > 0:
            if text1[i - 1] == text2[j - 1]:
                lcs.append(text1[i - 1])
                i -= 1
                j -= 1
            elif dp[i - 1][j] > dp[i][j - 1]:
                i -= 1
            else:
                j -= 1

        return ''.join(reversed(lcs))

    @staticmethod
    def longest_palindromic_subsequence(s):
        """最长回文子序列

        Args:
            s: 字符串

        Returns:
            最长回文子序列的长度
        """
        n = len(s)
        dp = [[0] * n for _ in range(n)]

        # 单个字符是长度为1的回文
        for i in range(n):
            dp[i][i] = 1

        # 长度从2到n
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                if s[i] == s[j]:
                    dp[i][j] = dp[i + 1][j - 1] + 2
                else:
                    dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])

        return dp[0][n - 1]

    @staticmethod
    def longest_palindromic_substring(s):
        """最长回文子串

        Args:
            s: 字符串

        Returns:
            最长回文子串
        """
        if not s:
            return ''

        n = len(s)
        dp = [[False] * n for _ in range(n)]
        start, max_length = 0, 1

        # 单个字符是回文
        for i in range(n):
            dp[i][i] = True

        # 检查长度为2的子串
        for i in range(n - 1):
            if s[i] == s[i + 1]:
                dp[i][i + 1] = True
                start = i
                max_length = 2

        # 检查长度大于2的子串
        for length in range(3, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                if s[i] == s[j] and dp[i + 1][j - 1]:
                    dp[i][j] = True
                    if length > max_length:
                        start = i
                        max_length = length

        return s[start:start + max_length]

    @staticmethod
    def edit_distance(word1, word2):
        """编辑距离（Levenshtein距离）

        Args:
            word1: 第一个字符串
            word2: 第二个字符串

        Returns:
            最少编辑次数
        """
        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # 初始化边界条件
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = min(
                        dp[i - 1][j] + 1,  # 删除
                        dp[i][j - 1] + 1,  # 插入
                        dp[i - 1][j - 1] + 1  # 替换
                    )

        return dp[m][n]

    # ====== 路径问题 ======

    @staticmethod
    def unique_paths(m, n):
        """不同路径：从左上角到右下角只能向右或向下移动

        Args:
            m: 行数
            n: 列数

        Returns:
            不同路径的数量
        """
        dp = [[1] * n for _ in range(m)]

        for i in range(1, m):
            for j in range(1, n):
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1]

        return dp[m - 1][n - 1]

    @staticmethod
    def unique_paths_with_obstacles(obstacle_grid):
        """不同路径II：网格中有障碍物

        Args:
            obstacle_grid: 障碍物网格（1表示障碍，0表示空地）

        Returns:
            不同路径的数量
        """
        if not obstacle_grid or not obstacle_grid[0]:
            return 0

        m, n = len(obstacle_grid), len(obstacle_grid[0])

        if obstacle_grid[0][0] == 1 or obstacle_grid[m - 1][n - 1] == 1:
            return 0

        dp = [[0] * n for _ in range(m)]
        dp[0][0] = 1

        # 初始化第一行
        for j in range(1, n):
            dp[0][j] = dp[0][j - 1] if obstacle_grid[0][j] == 0 else 0

        # 初始化第一列
        for i in range(1, m):
            dp[i][0] = dp[i - 1][0] if obstacle_grid[i][0] == 0 else 0

        for i in range(1, m):
            for j in range(1, n):
                if obstacle_grid[i][j] == 0:
                    dp[i][j] = dp[i - 1][j] + dp[i][j - 1]

        return dp[m - 1][n - 1]

    @staticmethod
    def min_path_sum(grid):
        """最小路径和：从左上角到右下角的路径和最小

        Args:
            grid: 数字网格

        Returns:
            最小路径和
        """
        if not grid or not grid[0]:
            return 0

        m, n = len(grid), len(grid[0])
        dp = [[0] * n for _ in range(m)]
        dp[0][0] = grid[0][0]

        # 初始化第一行
        for j in range(1, n):
            dp[0][j] = dp[0][j - 1] + grid[0][j]

        # 初始化第一列
        for i in range(1, m):
            dp[i][0] = dp[i - 1][0] + grid[i][0]

        for i in range(1, m):
            for j in range(1, n):
                dp[i][j] = min(dp[i - 1][j], dp[i][j - 1]) + grid[i][j]

        return dp[m - 1][n - 1]

    # ====== 子序列问题 ======

    @staticmethod
    def longest_increasing_subsequence(nums):
        """最长递增子序列（LIS）

        Args:
            nums: 数字数组

        Returns:
            最长递增子序列的长度
        """
        if not nums:
            return 0

        n = len(nums)
        dp = [1] * n

        for i in range(1, n):
            for j in range(i):
                if nums[j] < nums[i]:
                    dp[i] = max(dp[i], dp[j] + 1)

        return max(dp)

    @staticmethod
    def longest_increasing_subsequence_with_sequence(nums):
        """最长递增子序列（返回子序列）

        Args:
            nums: 数字数组

        Returns:
            最长递增子序列
        """
        if not nums:
            return []

        n = len(nums)
        dp = [1] * n
        prev = [-1] * n

        for i in range(1, n):
            for j in range(i):
                if nums[j] < nums[i] and dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1
                    prev[i] = j

        # 找到最长子序列的结束位置
        max_length = max(dp)
        end_index = dp.index(max_length)

        # 回溯构建子序列
        lis = []
        while end_index != -1:
            lis.append(nums[end_index])
            end_index = prev[end_index]

        return list(reversed(lis))

    # ====== 股票问题 ======

    @staticmethod
    def max_profit_one_transaction(prices):
        """买卖股票的最佳时机（只能交易一次）

        Args:
            prices: 股票价格数组

        Returns:
            最大利润
        """
        if not prices or len(prices) < 2:
            return 0

        min_price = prices[0]
        max_profit = 0

        for price in prices[1:]:
            max_profit = max(max_profit, price - min_price)
            min_price = min(min_price, price)

        return max_profit

    @staticmethod
    def max_profit_multiple_transactions(prices):
        """买卖股票的最佳时机（可以交易多次）

        Args:
            prices: 股票价格数组

        Returns:
            最大利润
        """
        if not prices or len(prices) < 2:
            return 0

        profit = 0

        for i in range(1, len(prices)):
            if prices[i] > prices[i - 1]:
                profit += prices[i] - prices[i - 1]

        return profit

    # ====== 零钱问题 ======

    @staticmethod
    def coin_change(coins, amount):
        """零钱兑换：最少的硬币数量

        Args:
            coins: 硬币面额数组
            amount: 目标金额

        Returns:
            最少硬币数量，如果无法兑换返回 -1
        """
        if amount == 0:
            return 0

        dp = [float('inf')] * (amount + 1)
        dp[0] = 0

        for coin in coins:
            for i in range(coin, amount + 1):
                dp[i] = min(dp[i], dp[i - coin] + 1)

        return dp[amount] if dp[amount] != float('inf') else -1

    @staticmethod
    def coin_change_combinations(coins, amount):
        """零钱兑换II：组合数

        Args:
            coins: 硬币面额数组
            amount: 目标金额

        Returns:
            组合的数量
        """
        dp = [0] * (amount + 1)
        dp[0] = 1

        for coin in coins:
            for i in range(coin, amount + 1):
                dp[i] += dp[i - coin]

        return dp[amount]


# 测试代码
if __name__ == '__main__':
    dp = DynamicProgramming()

    print('===== 基础动态规划 =====')
    print('斐波那契(10):', dp.fibonacci(10))  # 55
    print('爬楼梯(10):', dp.climb_stairs(10))  # 89

    print('\n===== 数组问题 =====')
    print('最大子数组和 [-2,1,-3,4,-1,2,1,-5,4]:', dp.max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))  # 6
    print('打家劫舍 [1,2,3,1]:', dp.house_robber([1, 2, 3, 1]))  # 4

    print('\n===== 背包问题 =====')
    print('0/1背包:', dp.knapsack_01([1, 3, 4], [15, 20, 30], 4))  # 35
    print('完全背包:', dp.unbounded_knapsack([1, 3, 4], [15, 20, 30], 4))  # 60

    print('\n===== 字符串问题 =====')
    print('最长公共子序列("abcde", "ace"):', dp.longest_common_subsequence('abcde', 'ace'))  # 3
    print('最长回文子序列("bbbab"):', dp.longest_palindromic_subsequence('bbbab'))  # 4
    print('编辑距离("horse", "ros"):', dp.edit_distance('horse', 'ros'))  # 3

    print('\n===== 路径问题 =====')
    print('不同路径(3,7):', dp.unique_paths(3, 7))  # 28
    print('最小路径和([[1,3,1],[1,5,1],[4,2,1]]):', dp.min_path_sum([[1, 3, 1], [1, 5, 1], [4, 2, 1]]))  # 7

    print('\n===== 子序列问题 =====')
    print('最长递增子序列([10,9,2,5,3,7,101,18]):', dp.longest_increasing_subsequence([10, 9, 2, 5, 3, 7, 101, 18]))  # 4

    print('\n===== 股票问题 =====')
    print('一次交易([7,1,5,3,6,4]):', dp.max_profit_one_transaction([7, 1, 5, 3, 6, 4]))  # 5
    print('多次交易([7,1,5,3,6,4]):', dp.max_profit_multiple_transactions([7, 1, 5, 3, 6, 4]))  # 7

    print('\n===== 零钱问题 =====')
    print('零钱兑换([1,2,5], 11):', dp.coin_change([1, 2, 5], 11))  # 3
    print('零钱兑换II([1,2,5], 5):', dp.coin_change_combinations([1, 2, 5], 5))  # 4
