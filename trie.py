class TrieNode:
    def __init__(self):
        self.children = {}

class Trie:
    def __init__(self, words):
        self.root = TrieNode()
        self.insert(words)

    def insert(self, words):
        for word in words:
            node = self.root
            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
    
    def search_node(self, path):
        node = self.root
        for i in range(len(path)):
            if path[i] not in node.children:
                return None
            node = node.children[path[i]]
        return node
        
    def count_child(self, path, char):
        pos = self.search_node(path)
        if pos == None:
            return 0
        if char not in pos.children:
            return 0
        pos = pos.children[char]
        return len(pos.children)