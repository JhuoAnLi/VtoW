import json
import heapq  # for efficient min heap operations

import heapq  # for efficient min heap operations

class TrieNode:
    def __init__(self):
        self.children = {}
        self.value = None


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, key, value):
        node = self.root
        for char in key:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.value = value

    def search(self, key):
        node = self.root
        for char in key:
            if char not in node.children:
                return None
            node = node.children[char]
        return node.value


def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)

    for i, c1 in enumerate(s1):
        current_row = [i + 1]

        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)

            current_row.append(min(insertions, deletions, substitutions))

        previous_row = current_row

    return previous_row[-1]


def find_closest_matches(query, trie, k=5):
    min_heap = []

    def dfs(node, key_so_far):
        nonlocal min_heap
        if node.value is not None:
            distance = levenshtein_distance(query, key_so_far)
            heapq.heappush(min_heap, (distance, key_so_far, node.value))

    def traverse(node, key_so_far):
        dfs(node, key_so_far)
        for char, child_node in node.children.items():
            traverse(child_node, key_so_far + char)

    traverse(trie.root, "")

    return [(result[1], result[2], result[0]) for result in heapq.nsmallest(k, min_heap)]


# Example usage:
my_dict = json.loads(open("bopomofo_dict_with_frequency2.json", "r").read())
my_dict2 = json.loads(open("canjie_dict.json", "r").read())
trie = Trie()

# Insert keys into the trie
for key in my_dict:
    trie.insert(key, my_dict[key])
for key in my_dict2:
    trie.insert(key, my_dict2[key])

while True:
    query_string = ""
    query_string = input("Enter a query: ")

    closest_matches = find_closest_matches(query_string, trie, k=5)
    print("Closest 5 matches:")
    for match in closest_matches:
        print(f"Key: {match[1]}, Value: {match[0]}, Distance: {match[2]}")
