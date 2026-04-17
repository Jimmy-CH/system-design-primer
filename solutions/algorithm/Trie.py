"""
前缀树（Trie）算法实现
包含多种Trie树的操作和应用场景
"""


class TrieNode(object):

    def __init__(self):
        """Trie节点"""
        self.children = {}  # 子节点字典 {字符: TrieNode}
        self.is_end = False  # 是否是单词结束节点
        self.count = 0  # 以该节点结尾的单词数量
        self.prefix_count = 0  # 经过该节点的单词前缀数量

    def __repr__(self):
        return f'TrieNode(children={len(self.children)}, is_end={self.is_end})'


class Trie(object):

    def __init__(self):
        """初始化Trie树"""
        self.root = TrieNode()

    def insert(self, word):
        """插入单词到Trie树

        Args:
            word: 要插入的单词
        """
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.prefix_count += 1
        node.is_end = True
        node.count += 1

    def search(self, word):
        """搜索单词是否在Trie树中

        Args:
            word: 要搜索的单词

        Returns:
            True 如果单词存在，否则 False
        """
        node = self._search_node(word)
        return node is not None and node.is_end

    def starts_with(self, prefix):
        """搜索是否有单词以该前缀开头

        Args:
            prefix: 前缀

        Returns:
            True 如果存在前缀，否则 False
        """
        node = self._search_node(prefix)
        return node is not None

    def _search_node(self, word):
        """搜索单词对应的节点

        Args:
            word: 单词

        Returns:
            对应的节点，如果不存在返回 None
        """
        node = self.root
        for char in word:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def delete(self, word):
        """从Trie树中删除单词

        Args:
            word: 要删除的单词

        Returns:
            True 如果删除成功，否则 False
        """
        node = self.root
        path = [(None, None, node)]  # (parent_char, parent_node, current_node)

        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
            node.prefix_count -= 1
            path.append((char, node, None))

        if not node.is_end:
            return False

        node.is_end = False
        node.count -= 1

        # 从后往前删除不需要的节点
        for i in range(len(path) - 1, 0, -1):
            char, parent_node, _ = path[i - 1]
            child_node = path[i][2]

            # 如果子节点不是单词结束且没有其他子节点，则删除
            if not child_node.is_end and not child_node.children:
                del parent_node.children[char]
            else:
                break

        return True

    def count_words_with_prefix(self, prefix):
        """统计以给定前缀开头的单词数量

        Args:
            prefix: 前缀

        Returns:
            单词数量
        """
        node = self._search_node(prefix)
        if node is None:
            return 0
        return node.prefix_count

    def get_all_words_with_prefix(self, prefix):
        """获取所有以给定前缀开头的单词

        Args:
            prefix: 前缀

        Returns:
            单词列表
        """
        node = self._search_node(prefix)
        if node is None:
            return []

        words = []
        self._dfs_collect_words(node, prefix, words)
        return words

    def _dfs_collect_words(self, node, current_prefix, words):
        """深度优先搜索收集所有单词

        Args:
            node: 当前节点
            current_prefix: 当前前缀
            words: 结果列表
        """
        if node.is_end:
            words.append(current_prefix)

        for char, child in sorted(node.children.items()):
            self._dfs_collect_words(child, current_prefix + char, words)

    def get_all_words(self):
        """获取Trie树中所有单词

        Returns:
            所有单词列表
        """
        words = []
        self._dfs_collect_words(self.root, '', words)
        return words

    def __repr__(self):
        """返回Trie树的字符串表示"""
        words = self.get_all_words()
        return f'Trie(words={words})'


class MapSum(object):

    """实现带有前缀和的Map"""

    def __init__(self):
        """初始化"""
        self.root = TrieNode()
        self.map = {}  # 存储单词和对应的值

    def insert(self, key, value):
        """插入键值对

        Args:
            key: 键
            value: 值
        """
        delta = value - self.map.get(key, 0)
        self.map[key] = value

        node = self.root
        for char in key:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.prefix_count += delta
        node.is_end = True

    def sum(self, prefix):
        """计算以给定前缀开头的所有键的和

        Args:
            prefix: 前缀

        Returns:
            和
        """
        node = self.root
        for char in prefix:
            if char not in node.children:
                return 0
            node = node.children[char]
        return node.prefix_count


class WordDictionary(object):

    """实现支持模糊搜索的字典（支持'.'通配符）"""

    def __init__(self):
        """初始化"""
        self.root = TrieNode()

    def add_word(self, word):
        """添加单词

        Args:
            word: 单词
        """
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word):
        """搜索单词（支持'.'通配符）

        Args:
            word: 单词（可能包含'.'）

        Returns:
            True 如果单词存在，否则 False
        """
        return self._dfs_search(self.root, word, 0)

    def _dfs_search(self, node, word, index):
        """深度优先搜索

        Args:
            node: 当前节点
            word: 单词
            index: 当前索引

        Returns:
            True 如果找到，否则 False
        """
        if index == len(word):
            return node.is_end

        char = word[index]
        if char == '.':
            # 遍历所有子节点
            for child in node.children.values():
                if self._dfs_search(child, word, index + 1):
                    return True
            return False
        else:
            if char not in node.children:
                return False
            return self._dfs_search(node.children[char], word, index + 1)


class ReplaceWords(object):

    """实现单词替换功能"""

    def __init__(self, dictionary):
        """初始化

        Args:
            dictionary: 字典列表
        """
        self.trie = Trie()
        for word in dictionary:
            self.trie.insert(word)

    def replace(self, sentence):
        """替换单词

        Args:
            sentence: 句子

        Returns:
            替换后的句子
        """
        words = sentence.split()
        result = []

        for word in words:
            prefix = self._find_shortest_prefix(word)
            result.append(prefix if prefix else word)

        return ' '.join(result)

    def _find_shortest_prefix(self, word):
        """找到最短的前缀

        Args:
            word: 单词

        Returns:
            最短前缀，如果不存在返回 None
        """
        node = self.trie.root
        prefix = ''

        for char in word:
            if char not in node.children:
                return None
            prefix += char
            node = node.children[char]
            if node.is_end:
                return prefix

        return None


class TrieWithDeletion(object):

    """支持删除操作的Trie树"""

    def __init__(self):
        """初始化"""
        self.root = TrieNode()

    def insert(self, word):
        """插入单词"""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word):
        """搜索单词"""
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end

    def starts_with(self, prefix):
        """搜索前缀"""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

    def delete(self, word):
        """删除单词"""
        return self._delete_helper(self.root, word, 0)

    def _delete_helper(self, node, word, index):
        """删除辅助函数"""
        if index == len(word):
            if not node.is_end:
                return False
            node.is_end = False
            return len(node.children) == 0

        char = word[index]
        if char not in node.children:
            return False

        should_delete_child = self._delete_helper(node.children[char], word, index + 1)

        if should_delete_child:
            del node.children[char]
            return len(node.children) == 0 and not node.is_end

        return False


# 测试代码
if __name__ == '__main__':
    print('===== 基础Trie树 =====')
    trie = Trie()
    trie.insert('apple')
    trie.insert('app')
    trie.insert('application')
    trie.insert('banana')

    print('搜索 "apple":', trie.search('apple'))  # True
    print('搜索 "app":', trie.search('app'))  # True
    print('搜索 "appl":', trie.search('appl'))  # False
    print('前缀 "app":', trie.starts_with('app'))  # True
    print('前缀 "ban":', trie.starts_with('ban'))  # True
    print('前缀 "orange":', trie.starts_with('orange'))  # False

    print('所有单词:', trie.get_all_words())  # ['app', 'apple', 'application', 'banana']
    print('以app开头的单词:', trie.get_all_words_with_prefix('app'))  # ['app', 'apple', 'application']
    print('以app开头的单词数:', trie.count_words_with_prefix('app'))  # 3

    trie.delete('apple')
    print('删除apple后搜索:', trie.search('apple'))  # False
    print('删除apple后的所有单词:', trie.get_all_words())  # ['app', 'application', 'banana']

    print('\n===== MapSum =====')
    map_sum = MapSum()
    map_sum.insert('apple', 3)
    map_sum.insert('app', 2)
    map_sum.insert('application', 5)

    print('前缀"app"的和:', map_sum.sum('app'))  # 10
    print('前缀"appl"的和:', map_sum.sum('appl'))  # 8
    map_sum.insert('app', 5)
    print('更新app后前缀"app"的和:', map_sum.sum('app'))  # 13

    print('\n===== WordDictionary =====')
    wd = WordDictionary()
    wd.add_word('bad')
    wd.add_word('dad')
    wd.add_word('mad')

    print('搜索 "pad":', wd.search('pad'))  # False
    print('搜索 "bad":', wd.search('bad'))  # True
    print('搜索 ".ad":', wd.search('.ad'))  # True
    print('搜索 "b..":', wd.search('b..'))  # True

    print('\n===== ReplaceWords =====')
    dictionary = ['cat', 'bat', 'rat']
    rw = ReplaceWords(dictionary)
    sentence = 'the cattle was rattled by the battery'
    print('替换前:', sentence)
    print('替换后:', rw.replace(sentence))  # 'the cat was rat by the bat'

    print('\n===== TrieWithDeletion =====')
    trie_del = TrieWithDeletion()
    trie_del.insert('apple')
    trie_del.insert('app')
    trie_del.insert('application')

    print('搜索 "apple":', trie_del.search('apple'))  # True
    trie_del.delete('apple')
    print('删除后搜索 "apple":', trie_del.search('apple'))  # False
    print('删除后搜索 "app":', trie_del.search('app'))  # True
    print('删除后前缀 "app":', trie_del.starts_with('app'))  # True
