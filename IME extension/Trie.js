"use strict";

class TrieNode {
    constructor() {
        this.children = {};
        this.value = null;
    }
}
class Trie {
    constructor() {
        this.root = new TrieNode();
        this.keyStrokeCatch = {};
        this.type_list = new Set();
    }

    insert(key, value, type) {
        if (!this.type_list.has(type)) {
            this.type_list.add(type);
        }

        let node = this.root;
        for (let char of key) {
            if (!(char in node.children)) {
                node.children[char] = new TrieNode();
            }
            node = node.children[char];
        }
        if (node.value === null) {
            node.value = value.map((element) => ({
                word: element[0],
                frequency: element[1],
                type: type
            }));
        } else {
            node.value = node.value.concat(value.map((element) => ({
                word: element[0],
                frequency: element[1]
            })));
        }
    }

    search(key) {
        let node = this.root;
        for (let char of key) {
            if (!(char in node.children)) {
                return null;
            }
            node = node.children[char];
        }
        return node.value;
    }

    /**
     * 
     * @param {string} query
     * @param {number} num_of_result 
     * @returns {array} array of objects of the form {distance, keySoFar, value}
     */
    findClosestMatches(query, num_of_result) {
        if (query in this.keyStrokeCatch) {
            return this.keyStrokeCatch[query];
        }
        let minHeap = [];

        function dfs(node, keySoFar) {
            if (node.value !== null) {
                let distance = levenshteinDistance(query, keySoFar);
                minHeap.push([distance, keySoFar, node.value]);
            }
        }
    
        function traverse(node, keySoFar) {
            dfs(node, keySoFar);
            for (let char in node.children) {
                traverse(node.children[char], keySoFar + char);
            }
        }

        function levenshteinDistance(s1, s2) {
            if (s1.length < s2.length) {
                return levenshteinDistance(s2, s1);
            }
        
            if (s2.length === 0) {
                return s1.length;
            }
        
            let previousRow = [...Array(s2.length + 1).keys()];
        
            for (let i = 0; i < s1.length; i++) {
                let currentRow = [i + 1];
        
                for (let j = 0; j < s2.length; j++) {
                    let insertions = previousRow[j + 1] + 1;
                    let deletions = currentRow[j] + 1;
                    let substitutions = previousRow[j] + (s1[i] !== s2[j]);
        
                    currentRow.push(Math.min(insertions, deletions, substitutions));
                }
        
                previousRow = currentRow;
            }
            return previousRow[previousRow.length - 1];
        }

        traverse(this.root, "");
        minHeap.sort((a, b) => a[0] - b[0]);

        const result = minHeap.slice(0, num_of_result).map(result => ({
            "distance": result[0],
            "keySoFar": result[1],
            "value": result[2]
        }));
        this.keyStrokeCatch[query] = result;

        return result
    }
}


async function build_Trie(){
    const trie = new Trie();
    const JSON_URLs = {
        ENGLISH: chrome.runtime.getURL('./src/english_dict_with_frequency.json'),
        BOPOMOFO: chrome.runtime.getURL('./src/bopomofo_dict_with_frequency2.json'),
        CANJIE: chrome.runtime.getURL('./src/canjie_dict_with_frequency.json'),
        PINYIN: chrome.runtime.getURL('./src/pinyin_dict.json'),
        THAI: chrome.runtime.getURL('./src/thai_dict.json'),
        VIETNAMESE: chrome.runtime.getURL('./src/vietnam_dict.json'),
    }

    for (let Language_key in JSON_URLs) {
        try {
            const response = await fetch(JSON_URLs[Language_key]);
            const dict = await response.json();
            for (let key in dict) {
                trie.insert(key, dict[key], Language_key);
            }
            // return trie;
        } catch (error) {
            console.error(`Error Building Trie from ${Language_key} JSON files:`, error);
        }
    }
    return trie;
}