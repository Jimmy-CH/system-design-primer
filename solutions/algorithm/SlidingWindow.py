"""
滑动窗口算法实现
包含多种经典的滑动窗口问题解决方案
"""


class SlidingWindow(object):

    # ====== 固定大小窗口 ======

    @staticmethod
    def max_sum_fixed_window(nums, k):
        """固定窗口大小：求最大子数组和

        Args:
            nums: 数字数组
            k: 窗口大小

        Returns:
            最大和
        """
        if not nums or k <= 0 or k > len(nums):
            return 0

        # 计算第一个窗口的和
        window_sum = sum(nums[:k])
        max_sum = window_sum

        # 滑动窗口
        for i in range(k, len(nums)):
            window_sum += nums[i] - nums[i - k]
            max_sum = max(max_sum, window_sum)

        return max_sum

    @staticmethod
    def average_fixed_window(nums, k):
        """固定窗口大小：计算所有窗口的平均值

        Args:
            nums: 数字数组
            k: 窗口大小

        Returns:
            平均值列表
        """
        if not nums or k <= 0 or k > len(nums):
            return []

        result = []
        window_sum = sum(nums[:k])
        result.append(window_sum / k)

        for i in range(k, len(nums)):
            window_sum += nums[i] - nums[i - k]
            result.append(window_sum / k)

        return result

    @staticmethod
    def max_consecutive_ones(nums, k):
        """最大连续1的个数（最多可以翻转k个0）

        Args:
            nums: 只包含0和1的数组
            k: 可以翻转的0的个数

        Returns:
            最大连续1的个数
        """
        left = 0
        max_length = 0
        zero_count = 0

        for right in range(len(nums)):
            if nums[right] == 0:
                zero_count += 1

            # 当0的个数超过k时，收缩窗口
            while zero_count > k:
                if nums[left] == 0:
                    zero_count -= 1
                left += 1

            max_length = max(max_length, right - left + 1)

        return max_length

    # ====== 可变大小窗口 ======

    @staticmethod
    def min_subarray_sum(nums, target):
        """最小子数组和：和 >= target 的最小长度子数组

        Args:
            nums: 正整数数组
            target: 目标和

        Returns:
            最小子数组长度，如果不存在返回 0
        """
        left = 0
        current_sum = 0
        min_length = float('inf')

        for right in range(len(nums)):
            current_sum += nums[right]

            # 收缩窗口，找到满足条件的最小窗口
            while current_sum >= target:
                min_length = min(min_length, right - left + 1)
                current_sum -= nums[left]
                left += 1

        return min_length if min_length != float('inf') else 0

    @staticmethod
    def max_subarray_less_than_k(nums, k):
        """和小于k的最大子数组长度

        Args:
            nums: 正整数数组
            k: 目标值

        Returns:
            最大子数组长度
        """
        left = 0
        current_sum = 0
        max_length = 0

        for right in range(len(nums)):
            current_sum += nums[right]

            # 收缩窗口，使和小于k
            while current_sum >= k and left <= right:
                current_sum -= nums[left]
                left += 1

            max_length = max(max_length, right - left + 1)

        return max_length

    # ====== 字符串滑动窗口 ======

    @staticmethod
    def longest_substring_without_repeating(s):
        """无重复字符的最长子串

        Args:
            s: 字符串

        Returns:
            最长子串长度
        """
        char_index = {}
        left = 0
        max_length = 0

        for right, char in enumerate(s):
            # 如果字符在窗口中，移动左边界
            if char in char_index and char_index[char] >= left:
                left = char_index[char] + 1

            char_index[char] = right
            max_length = max(max_length, right - left + 1)

        return max_length

    @staticmethod
    def min_window_substring(s, t):
        """最小覆盖子串：在s中包含t所有字符的最小子串

        Args:
            s: 源字符串
            t: 目标字符串

        Returns:
            最小覆盖子串，如果不存在返回空字符串
        """
        from collections import defaultdict

        if not s or not t or len(t) > len(s):
            return ''

        # 统计t中字符频率
        need = defaultdict(int)
        for char in t:
            need[char] += 1

        # 需要匹配的字符种类数
        required = len(need)

        left = 0
        formed = 0
        window_counts = defaultdict(int)
        result = float('inf'), None, None  # (window length, left, right)

        for right, char in enumerate(s):
            # 扩展窗口
            window_counts[char] += 1

            if char in need and window_counts[char] == need[char]:
                formed += 1

            # 收缩窗口
            while left <= right and formed == required:
                char = s[left]

                # 更新结果
                if right - left + 1 < result[0]:
                    result = (right - left + 1, left, right)

                # 从窗口中移除字符
                window_counts[char] -= 1
                if char in need and window_counts[char] < need[char]:
                    formed -= 1

                left += 1

        return s[result[1]:result[2] + 1] if result[0] != float('inf') else ''

    @staticmethod
    def length_of_longest_substring_k_distinct(s, k):
        """最多包含k个不同字符的最长子串

        Args:
            s: 字符串
            k: 不同字符的最大数量

        Returns:
            最长子串长度
        """
        if k == 0:
            return 0

        char_count = {}
        left = 0
        max_length = 0

        for right, char in enumerate(s):
            char_count[char] = char_count.get(char, 0) + 1

            # 收缩窗口，使不同字符数不超过k
            while len(char_count) > k:
                left_char = s[left]
                char_count[left_char] -= 1
                if char_count[left_char] == 0:
                    del char_count[left_char]
                left += 1

            max_length = max(max_length, right - left + 1)

        return max_length

    @staticmethod
    def character_replacement(s, k):
        """字符替换：最多替换k个字符，使所有字符相同的最长子串

        Args:
            s: 字符串（只包含大写字母）
            k: 最多替换次数

        Returns:
            最长子串长度
        """
        char_count = {}
        max_count = 0
        left = 0
        max_length = 0

        for right, char in enumerate(s):
            char_count[char] = char_count.get(char, 0) + 1
            max_count = max(max_count, char_count[char])

            # 窗口大小 - 最大字符出现次数 > k，需要收缩
            while (right - left + 1) - max_count > k:
                left_char = s[left]
                char_count[left_char] -= 1
                left += 1

            max_length = max(max_length, right - left + 1)

        return max_length

    @staticmethod
    def check_inclusion(s1, s2):
        """字符串的排列：检查s1的排列是否是s2的子串

        Args:
            s1: 字符串1
            s2: 字符串2

        Returns:
            True 如果存在，否则 False
        """
        from collections import Counter

        if len(s1) > len(s2):
            return False

        s1_count = Counter(s1)
        window_count = Counter(s2[:len(s1)])

        if s1_count == window_count:
            return True

        for i in range(len(s1), len(s2)):
            # 移除左边字符
            left_char = s2[i - len(s1)]
            window_count[left_char] -= 1
            if window_count[left_char] == 0:
                del window_count[left_char]

            # 添加右边字符
            right_char = s2[i]
            window_count[right_char] += 1

            if s1_count == window_count:
                return True

        return False

    # ====== 数组滑动窗口 ======

    @staticmethod
    def find_anagrams(s, p):
        """找到字符串中所有字母异位词

        Args:
            s: 源字符串
            p: 模式字符串

        Returns:
            所有异位词的起始索引
        """
        from collections import Counter

        if len(p) > len(s):
            return []

        p_count = Counter(p)
        window_count = Counter(s[:len(p)])
        result = []

        if p_count == window_count:
            result.append(0)

        for i in range(len(p), len(s)):
            # 移除左边字符
            left_char = s[i - len(p)]
            window_count[left_char] -= 1
            if window_count[left_char] == 0:
                del window_count[left_char]

            # 添加右边字符
            right_char = s[i]
            window_count[right_char] += 1

            if p_count == window_count:
                result.append(i - len(p) + 1)

        return result

    @staticmethod
    def subarrays_with_k_distinct(nums, k):
        """恰好有k个不同整数的子数组个数

        Args:
            nums: 整数数组
            k: 不同整数的个数

        Returns:
            子数组个数
        """
        def at_most_k(k):
            """最多有k个不同整数的子数组个数"""
            if k == 0:
                return 0

            count = {}
            left = 0
            result = 0

            for right, num in enumerate(nums):
                count[num] = count.get(num, 0) + 1

                while len(count) > k:
                    left_num = nums[left]
                    count[left_num] -= 1
                    if count[left_num] == 0:
                        del count[left_num]
                    left += 1

                result += right - left + 1

            return result

        return at_most_k(k) - at_most_k(k - 1)

    @staticmethod
    def longest_subarray_of_1s_after_deleting(nums):
        """删除一个元素后最长的全是1的子数组

        Args:
            nums: 只包含0和1的数组

        Returns:
            最长子数组长度
        """
        left = 0
        zero_count = 0
        max_length = 0

        for right in range(len(nums)):
            if nums[right] == 0:
                zero_count += 1

            while zero_count > 1:
                if nums[left] == 0:
                    zero_count -= 1
                left += 1

            max_length = max(max_length, right - left)

        return max_length

    # ====== 多指针滑动窗口 ======

    @staticmethod
    def min_operations(nums, x):
        """最小操作数：从数组两端移除元素，使和等于x的最少操作数

        Args:
            nums: 正整数数组
            x: 目标和

        Returns:
            最小操作数，如果不可能返回 -1
        """
        total_sum = sum(nums)
        target = total_sum - x

        if target == 0:
            return len(nums)
        if target < 0:
            return -1

        left = 0
        current_sum = 0
        max_length = -1

        for right in range(len(nums)):
            current_sum += nums[right]

            while current_sum > target and left <= right:
                current_sum -= nums[left]
                left += 1

            if current_sum == target:
                max_length = max(max_length, right - left + 1)

        return len(nums) - max_length if max_length != -1 else -1

    @staticmethod
    def max_score(card_points, k):
        """可以获得的最大点数：从两端抽取k张卡牌

        Args:
            card_points: 卡牌点数数组
            k: 抽取卡牌数量

        Returns:
            最大点数
        """
        n = len(card_points)
        window_size = n - k

        if window_size == 0:
            return sum(card_points)

        # 计算第一个窗口的和
        window_sum = sum(card_points[:window_size])
        min_sum = window_sum
        total_sum = window_sum

        # 滑动窗口，找到最小窗口和
        for i in range(window_size, n):
            window_sum += card_points[i] - card_points[i - window_size]
            min_sum = min(min_sum, window_sum)
            total_sum += card_points[i]

        return total_sum - min_sum

    @staticmethod
    def count_subarrays_with_less_than_k(nums, k):
        """乘积小于k的子数组个数

        Args:
            nums: 正整数数组
            k: 目标值

        Returns:
            子数组个数
        """
        if k <= 1:
            return 0

        left = 0
        product = 1
        count = 0

        for right, num in enumerate(nums):
            product *= num

            while product >= k and left <= right:
                product //= nums[left]
                left += 1

            count += right - left + 1

        return count

    # ====== 模式匹配 ======

    @staticmethod
    def find_all_anagrams_in_string(s, p):
        """在字符串中查找所有变位词的起始位置

        Args:
            s: 源字符串
            p: 模式字符串

        Returns:
            所有匹配的起始位置列表
        """
        from collections import Counter

        if len(p) > len(s):
            return []

        p_count = Counter(p)
        window_count = Counter(s[:len(p)])
        result = []

        if p_count == window_count:
            result.append(0)

        for i in range(len(p), len(s)):
            left_char = s[i - len(p)]
            window_count[left_char] -= 1
            if window_count[left_char] == 0:
                del window_count[left_char]

            right_char = s[i]
            window_count[right_char] += 1

            if p_count == window_count:
                result.append(i - len(p) + 1)

        return result


# 测试代码
if __name__ == '__main__':
    sw = SlidingWindow()

    print('===== 固定大小窗口 =====')
    print('最大和 [1,4,2,10,23,3,1,0,20], k=4:', sw.max_sum_fixed_window([1, 4, 2, 10, 23, 3, 1, 0, 20], 4))  # 39
    print('最大连续1 [1,1,1,0,0,0,1,1,1,1,0], k=2:', sw.max_consecutive_ones([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2))  # 6

    print('\n===== 可变大小窗口 =====')
    print('最小子数组 [2,3,1,2,4,3], target=7:', sw.min_subarray_sum([2, 3, 1, 2, 4, 3], 7))  # 2

    print('\n===== 字符串滑动窗口 =====')
    print('无重复子串 "abcabcbb":', sw.longest_substring_without_repeating('abcabcbb'))  # 3
    print('最小覆盖子串 s="ADOBECODEBANC", t="ABC":', sw.min_window_substring('ADOBECODEBANC', 'ABC'))  # BANC
    print('最多k个不同字符 "eceba", k=2:', sw.length_of_longest_substring_k_distinct('eceba', 2))  # 3
    print('字符替换 "ABAB", k=2:', sw.character_replacement('ABAB', 2))  # 4
    print('字符串排列 s1="ab", s2="eidbaooo":', sw.check_inclusion('ab', 'eidbaooo'))  # True

    print('\n===== 数组滑动窗口 =====')
    print('找异位词 s="cbaebabacd", p="abc":', sw.find_anagrams('cbaebabacd', 'abc'))  # [0, 6]
    print('恰好k个不同 [1,2,1,2,3], k=2:', sw.subarrays_with_k_distinct([1, 2, 1, 2, 3], 2))  # 7

    print('\n===== 多指针滑动窗口 =====')
    print('最小操作数 [1,1,4,2,3], x=5:', sw.min_operations([1, 1, 4, 2, 3], 5))  # 2
    print('最大点数 [1,2,3,4,5,6,1], k=3:', sw.max_score([1, 2, 3, 4, 5, 6, 1], 3))  # 12
    print('乘积小于k [10,5,2,6], k=100:', sw.count_subarrays_with_less_than_k([10, 5, 2, 6], 100))  # 8
