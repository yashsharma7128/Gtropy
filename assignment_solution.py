import Levenshtein
import time

class TrieNode:
    def __init__(self):
        self.children = {}  # child node which contains character and address of next childnode
        self.word_end = False # tells if the word has ended or not


class Dictionary:
    def __init__(self):
        self.root = TrieNode() # intialised root node by making instance of TrieNode class

    def insert(self, word):
        # Space Complexity: O(M * N) - M is the average length of words, N is the number of words
        # Time Complexity: O(M * N) - M is the average length of words, N is the number of words
        if not word.isalpha():  # discard invalid input 
            return

        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode() #adding character to Trienode 
            node = node.children[char]
        node.word_end = True
    
    def search(self, word, max_distance=2):
        # Space Complexity: O(M) - M is the length of the search query
        # Time Complexity: O(M) - M is the length of the search query
        if not word.isalpha():  # discard invalid input 
            print('Invalid Input')
            return []

        word = word.lower()
        node = self.root
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                return self.word_suggestions(word, max_distance)

        if node.word_end:
            return [word]
        else:
            suggestions = self.word_suggestions(word, max_distance)
            return suggestions
    #sort the suggetions and call the function to find them
    def word_suggestions(self, word, max_distance):
        suggestions = []
        # Space Complexity: O(K * N * M) - K is the number of suggestions, N is the number of nodes in Trie, M is the average length of words
        # Time Complexity: O(K * N * M) - K is the number of suggestions, N is the number of nodes in Trie, M is the average length of words
        self.find_suggestions(self.root, '', word, suggestions, max_distance)
        suggestions.sort(key=lambda s: Levenshtein.distance(word, s))
        return suggestions
    # find the suggestions
    def find_suggestions(self, node, current, target, suggestions, max_distance):
        if node.word_end:
            distance = Levenshtein.distance(target, current)
            if distance <= max_distance:
                suggestions.append(current)

        for char, child_node in node.children.items():
            self.find_suggestions(child_node, current + char, target, suggestions, max_distance)

#build dictionary function 
def build_dictionary(file_path):
    dictionary = Dictionary()
    with open(file_path, 'r') as file:
        for line in file:
            word = line.strip()
            dictionary.insert(word)
    return dictionary

# build and intialise the dictionary class and trienode using input list
file_path = 'list.txt'
my_dictionary = build_dictionary(file_path)

while True:
    # Ask the user for a search query
    search_word = input("Enter a word to search (type 'exit1' to exit): ").strip().lower()

    # Check if the user wants to exit or search again
    if search_word == 'exit1':
        break

    # search is performed and time when code started to run also noted
    start_time = time.time()
    result = my_dictionary.search(search_word)

    #for displaying result 
    if result == search_word:
        print(f"Word '{search_word}' found in the dictionary ")
    elif result:
        print(f"Word '{search_word}' not found in the dictionary. Suggestions: {result}")
    else :
        print("not found")
    #time at end of the search and time taken to search the query
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"your search took: {elapsed_time} seconds")
