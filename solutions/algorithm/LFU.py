"""
LFU（Least Frequently Used）算法实现
包含多种LFU缓存实现方式
"""
from collections import defaultdict, OrderedDict


class Node(object):

    """LFU缓存节点"""

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.freq = 1  # 访问频率


class DLinkedList(object):

    """双向链表，维护访问顺序"""

    def __init__(self):
        self.head = Node(0, 0)  # 哨兵节点
        self.tail = Node(0, 0)  # 哨兵节点
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def __len__(self):
        return self.size

    def append(self, node):
        """在链表头部添加节点（表示最近访问）"""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
        self.size += 1

    def pop(self, node=None):
        """移除节点"""
        if self.size == 0:
            return

        if not node:
            node = self.tail.prev

        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1

        return node


class LFUCache(object):

    """LFU缓存实现（双向链表 + 哈希表）"""

    def __init__(self, capacity):
        """初始化LFU缓存

        Args:
            capacity: 缓存容量
        """
        if capacity <= 0:
            raise ValueError('Capacity must be greater than 0')

        self.capacity = capacity
        self.size = 0
        self.min_freq = 0  # 当前最小访问频率

        # key -> Node
        self.key_to_node = {}

        # frequency -> DLinkedList
        self.freq_to_nodes = defaultdict(DLinkedList)

    def _update_node(self, node):
        """更新节点频率

        Args:
            node: 要更新的节点
        """
        freq = node.freq

        # 从旧频率链表中移除
        self.freq_to_nodes[freq].pop(node)

        # 如果旧频率链表为空且是最小频率，更新最小频率
        if self.min_freq == freq and not self.freq_to_nodes[freq]:
            self.min_freq += 1

        # 更新频率
        node.freq += 1

        # 添加到新频率链表
        self.freq_to_nodes[node.freq].append(node)

    def get(self, key):
        """获取缓存值

        Args:
            key: 键

        Returns:
            值，如果不存在返回 None
        """
        if key not in self.key_to_node:
            return None

        node = self.key_to_node[key]

        # 更新节点频率
        self._update_node(node)

        return node.value

    def put(self, key, value):
        """设置缓存值

        Args:
            key: 键
            value: 值
        """
        if self.capacity == 0:
            return

        if key in self.key_to_node:
            # 更新已有节点
            node = self.key_to_node[key]
            node.value = value
            self._update_node(node)
        else:
            # 添加新节点
            if self.size >= self.capacity:
                # 淘汰最小频率链表的尾部节点
                node_to_remove = self.freq_to_nodes[self.min_freq].pop()
                del self.key_to_node[node_to_remove.key]
                self.size -= 1

            # 创建新节点
            node = Node(key, value)
            self.key_to_node[key] = node
            self.freq_to_nodes[1].append(node)
            self.min_freq = 1
            self.size += 1

    def delete(self, key):
        """删除缓存

        Args:
            key: 键
        """
        if key in self.key_to_node:
            node = self.key_to_node[key]
            freq = node.freq

            # 从频率链表中移除
            self.freq_to_nodes[freq].pop(node)

            # 从哈希表中移除
            del self.key_to_node[key]
            self.size -= 1

            # 更新最小频率
            if freq == self.min_freq and not self.freq_to_nodes[freq]:
                self.min_freq = min(self.freq_to_nodes.keys()) if self.freq_to_nodes else 0

    def clear(self):
        """清空缓存"""
        self.key_to_node.clear()
        self.freq_to_nodes.clear()
        self.size = 0
        self.min_freq = 0

    def __len__(self):
        return self.size

    def __contains__(self, key):
        return key in self.key_to_node

    def __repr__(self):
        items = []
        for freq in sorted(self.freq_to_nodes.keys()):
            node = self.freq_to_nodes[freq].head.next
            while node != self.freq_to_nodes[freq].tail:
                items.append(f'{node.key}:{node.value}(freq={node.freq})')
                node = node.next
        return f'LFUCache([{", ".join(items)}])'


class LFUCacheOrderedDict(object):

    """使用OrderedDict实现的LFU缓存"""

    def __init__(self, capacity):
        """初始化LFU缓存

        Args:
            capacity: 缓存容量
        """
        if capacity <= 0:
            raise ValueError('Capacity must be greater than 0')

        self.capacity = capacity
        self.size = 0
        self.min_freq = 0

        # key -> (value, frequency)
        self.key_to_value_freq = {}

        # frequency -> OrderedDict(key -> value)
        self.freq_to_keys = defaultdict(OrderedDict)

    def _update_freq(self, key):
        """更新key的频率

        Args:
            key: 键
        """
        value, freq = self.key_to_value_freq[key]

        # 从旧频率字典中移除
        del self.freq_to_keys[freq][key]

        # 如果旧频率字典为空且是最小频率，更新最小频率
        if self.min_freq == freq and not self.freq_to_keys[freq]:
            self.min_freq += 1

        # 更新频率
        new_freq = freq + 1
        self.key_to_value_freq[key] = (value, new_freq)
        self.freq_to_keys[new_freq][key] = value

    def get(self, key):
        """获取缓存值

        Args:
            key: 键

        Returns:
            值，如果不存在返回 None
        """
        if key not in self.key_to_value_freq:
            return None

        value = self.key_to_value_freq[key][0]
        self._update_freq(key)

        return value

    def put(self, key, value):
        """设置缓存值

        Args:
            key: 键
            value: 值
        """
        if self.capacity == 0:
            return

        if key in self.key_to_value_freq:
            # 更新已有节点
            _, freq = self.key_to_value_freq[key]
            self.key_to_value_freq[key] = (value, freq)
            self._update_freq(key)
        else:
            # 添加新节点
            if self.size >= self.capacity:
                # 淘汰最小频率字典中最旧的key
                old_key, _ = self.freq_to_keys[self.min_freq].popitem(last=False)
                del self.key_to_value_freq[old_key]
                self.size -= 1

            # 添加新节点
            self.key_to_value_freq[key] = (value, 1)
            self.freq_to_keys[1][key] = value
            self.min_freq = 1
            self.size += 1

    def delete(self, key):
        """删除缓存

        Args:
            key: 键
        """
        if key in self.key_to_value_freq:
            value, freq = self.key_to_value_freq[key]

            # 从频率字典中移除
            del self.freq_to_keys[freq][key]

            # 从哈希表中移除
            del self.key_to_value_freq[key]
            self.size -= 1

            # 更新最小频率
            if freq == self.min_freq and not self.freq_to_keys[freq]:
                self.min_freq = min(self.freq_to_keys.keys()) if self.freq_to_keys else 0

    def clear(self):
        """清空缓存"""
        self.key_to_value_freq.clear()
        self.freq_to_keys.clear()
        self.size = 0
        self.min_freq = 0

    def __len__(self):
        return self.size

    def __contains__(self, key):
        return key in self.key_to_value_freq

    def __repr__(self):
        items = []
        for freq in sorted(self.freq_to_keys.keys()):
            for key, value in self.freq_to_keys[freq].items():
                items.append(f'{key}:{value}(freq={freq})')
        return f'LFUCacheOrderedDict([{", ".join(items)}])'


class LFUCacheSimple(object):

    """简化的LFU缓存实现（使用计数器）"""

    def __init__(self, capacity):
        """初始化LFU缓存

        Args:
            capacity: 缓存容量
        """
        if capacity <= 0:
            raise ValueError('Capacity must be greater than 0')

        self.capacity = capacity
        self.size = 0

        # key -> (value, frequency, timestamp)
        self.cache = {}

        self.timestamp = 0

    def get(self, key):
        """获取缓存值

        Args:
            key: 键

        Returns:
            值，如果不存在返回 None
        """
        if key not in self.cache:
            return None

        value, freq, _ = self.cache[key]
        self.cache[key] = (value, freq + 1, self.timestamp)
        self.timestamp += 1

        return value

    def put(self, key, value):
        """设置缓存值

        Args:
            key: 键
            value: 值
        """
        if self.capacity == 0:
            return

        if key in self.cache:
            # 更新已有节点
            _, freq, _ = self.cache[key]
            self.cache[key] = (value, freq + 1, self.timestamp)
        else:
            # 添加新节点
            if self.size >= self.capacity:
                # 淘汰频率最低且时间最旧的节点
                lfu_key = min(
                    self.cache.keys(),
                    key=lambda k: (self.cache[k][1], self.cache[k][2])
                )
                del self.cache[lfu_key]
                self.size -= 1

            # 添加新节点
            self.cache[key] = (value, 1, self.timestamp)
            self.size += 1

        self.timestamp += 1

    def delete(self, key):
        """删除缓存

        Args:
            key: 键
        """
        if key in self.cache:
            del self.cache[key]
            self.size -= 1

    def clear(self):
        """清空缓存"""
        self.cache.clear()
        self.size = 0
        self.timestamp = 0

    def __len__(self):
        return self.size

    def __contains__(self, key):
        return key in self.cache

    def __repr__(self):
        items = []
        for key, (value, freq, _) in sorted(
            self.cache.items(),
            key=lambda x: (x[1][1], x[1][2])
        ):
            items.append(f'{key}:{value}(freq={freq})')
        return f'LFUCacheSimple([{", ".join(items)}])'


# 测试代码
if __name__ == '__main__':
    print('===== LFU缓存（双向链表实现）=====')
    lfu = LFUCache(capacity=2)
    lfu.put(1, 1)
    lfu.put(2, 2)
    print('get(1):', lfu.get(1))  # 1
    lfu.put(3, 3)  # 淘汰key 2（频率最低）
    print('get(2):', lfu.get(2))  # None
    print('get(3):', lfu.get(3))  # 3
    lfu.put(4, 4)  # 淘汰key 1（频率最低）
    print('get(1):', lfu.get(1))  # None
    print('get(3):', lfu.get(3))  # 3
    print('get(4):', lfu.get(4))  # 4
    print('LFU缓存:', lfu)

    print('\n===== LFU缓存（OrderedDict实现）=====')
    lfu_od = LFUCacheOrderedDict(capacity=2)
    lfu_od.put(1, 1)
    lfu_od.put(2, 2)
    print('get(1):', lfu_od.get(1))  # 1
    lfu_od.put(3, 3)  # 淘汰key 2
    print('get(2):', lfu_od.get(2))  # None
    print('get(3):', lfu_od.get(3))  # 3
    lfu_od.put(4, 4)  # 淘汰key 1
    print('get(1):', lfu_od.get(1))  # None
    print('get(3):', lfu_od.get(3))  # 3
    print('get(4):', lfu_od.get(4))  # 4
    print('LFU缓存:', lfu_od)

    print('\n===== LFU缓存（简化实现）=====')
    lfu_simple = LFUCacheSimple(capacity=2)
    lfu_simple.put(1, 1)
    lfu_simple.put(2, 2)
    print('get(1):', lfu_simple.get(1))  # 1
    lfu_simple.put(3, 3)  # 淘汰key 2
    print('get(2):', lfu_simple.get(2))  # None
    print('get(3):', lfu_simple.get(3))  # 3
    lfu_simple.put(4, 4)  # 淘汰key 1
    print('get(1):', lfu_simple.get(1))  # None
    print('get(3):', lfu_simple.get(3))  # 3
    print('get(4):', lfu_simple.get(4))  # 4
    print('LFU缓存:', lfu_simple)

    print('\n===== 性能测试 =====')
    import time

    # 测试双向链表实现
    start = time.time()
    lfu = LFUCache(capacity=1000)
    for i in range(10000):
        lfu.put(i, i)
        lfu.get(i % 500)
    print('双向链表实现:', time.time() - start, '秒')

    # 测试OrderedDict实现
    start = time.time()
    lfu_od = LFUCacheOrderedDict(capacity=1000)
    for i in range(10000):
        lfu_od.put(i, i)
        lfu_od.get(i % 500)
    print('OrderedDict实现:', time.time() - start, '秒')

    # 测试简化实现
    start = time.time()
    lfu_simple = LFUCacheSimple(capacity=1000)
    for i in range(10000):
        lfu_simple.put(i, i)
        lfu_simple.get(i % 500)
    print('简化实现:', time.time() - start, '秒')
