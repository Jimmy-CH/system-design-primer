class Node(object):

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class DoublyLinkedList(object):

    def __init__(self):
        self.head = None
        self.tail = None

    def append_to_front(self, node):
        """将节点添加到链表头部（最近使用）"""
        if not self.head:
            self.head = node
            self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node

    def move_to_front(self, node):
        """将节点移动到链表头部"""
        if node == self.head:
            return
        self.remove(node)
        self.append_to_front(node)

    def remove(self, node):
        """从链表中移除节点"""
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next

        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev

        node.prev = None
        node.next = None

    def remove_from_tail(self):
        """移除并返回链表尾部节点（最久未使用）"""
        if not self.tail:
            return None
        node = self.tail
        self.remove(node)
        return node


class LRU(object):

    def __init__(self, capacity):
        """初始化 LRU 缓存
        
        Args:
            capacity: 缓存的最大容量
        """
        if capacity <= 0:
            raise ValueError('Capacity must be greater than 0')
        self.capacity = capacity
        self.size = 0
        self.cache = {}  # key: key, value: node
        self.linked_list = DoublyLinkedList()

    def get(self, key):
        """获取缓存中指定 key 的值
        
        Args:
            key: 要查找的键
            
        Returns:
            key 对应的值，如果不存在则返回 None
        """
        if key not in self.cache:
            return None
        node = self.cache[key]
        self.linked_list.move_to_front(node)
        return node.value

    def set(self, key, value):
        """设置缓存中指定 key 的值
        
        Args:
            key: 要设置的键
            value: 要设置的值
        """
        if key in self.cache:
            # key 已存在，更新值并移动到头部
            node = self.cache[key]
            node.value = value
            self.linked_list.move_to_front(node)
        else:
            # key 不存在，创建新节点
            if self.size == self.capacity:
                # 缓存已满，移除最久未使用的节点
                tail_node = self.linked_list.remove_from_tail()
                if tail_node:
                    del self.cache[tail_node.key]
                    self.size -= 1
            # 添加新节点
            new_node = Node(key, value)
            self.linked_list.append_to_front(new_node)
            self.cache[key] = new_node
            self.size += 1

    def delete(self, key):
        """删除缓存中指定 key
        
        Args:
            key: 要删除的键
        """
        if key in self.cache:
            node = self.cache[key]
            self.linked_list.remove(node)
            del self.cache[key]
            self.size -= 1

    def clear(self):
        """清空缓存"""
        self.cache.clear()
        self.linked_list = DoublyLinkedList()
        self.size = 0

    def __len__(self):
        """返回缓存当前大小"""
        return self.size

    def __contains__(self, key):
        """判断 key 是否在缓存中"""
        return key in self.cache

    def __repr__(self):
        """返回缓存的字符串表示"""
        items = []
        node = self.linked_list.head
        while node:
            items.append(f'{node.key}: {node.value}')
            node = node.next
        return f'LRU([{", ".join(items)}])'


# 使用 OrderedDict 实现的 LRU 缓存
from collections import OrderedDict


class LRUWithOrderedDict(object):

    def __init__(self, capacity):
        """初始化 LRU 缓存

        Args:
            capacity: 缓存的最大容量
        """
        if capacity <= 0:
            raise ValueError('Capacity must be greater than 0')
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        """获取缓存中指定 key 的值

        Args:
            key: 要查找的键

        Returns:
            key 对应的值，如果不存在则返回 None
        """
        if key not in self.cache:
            return None
        # 移动到末尾表示最近使用
        self.cache.move_to_end(key)
        return self.cache[key]

    def set(self, key, value):
        """设置缓存中指定 key 的值

        Args:
            key: 要设置的键
            value: 要设置的值
        """
        if key in self.cache:
            # key 已存在，更新值并移动到末尾
            self.cache.move_to_end(key)
        else:
            # key 不存在，检查是否需要淘汰
            if len(self.cache) >= self.capacity:
                # 移除最久未使用的元素（最前面的元素）
                self.cache.popitem(last=False)
        self.cache[key] = value

    def delete(self, key):
        """删除缓存中指定 key

        Args:
            key: 要删除的键
        """
        if key in self.cache:
            del self.cache[key]

    def clear(self):
        """清空缓存"""
        self.cache.clear()

    def __len__(self):
        """返回缓存当前大小"""
        return len(self.cache)

    def __contains__(self, key):
        """判断 key 是否在缓存中"""
        return key in self.cache

    def __repr__(self):
        """返回缓存的字符串表示"""
        items = [f'{k}: {v}' for k, v in self.cache.items()]
        return f'LRUWithOrderedDict([{", ".join(items)}])'


# 测试代码
if __name__ == '__main__':
    # lru = LRU(capacity=3)
    # lru.set('a', 1)
    # lru.set('b', 2)
    # lru.set('c', 3)
    # print(lru.get('a'))  # 输出: 1
    # lru.set('d', 4)      # 容量满，移除最久未使用的 'b'
    # print(lru.get('b'))  # 输出: None
    print('使用 OrderedDict 的 LRU 缓存:')
    lru_od = LRUWithOrderedDict(capacity=3)
    lru_od.set('a', 1)
    lru_od.set('b', 2)
    lru_od.set('c', 3)
    print(lru_od.get('a'))  # 输出: 1
    lru_od.set('d', 4)      # 容量满，移除 'b'
    print(lru_od.get('b'))  # 输出: None
    print(lru_od)           # 输出: LRUWithOrderedDict([a: 1, c: 3, d: 4])

