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
    }

    insert(key, value, type) {
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
    const BOPOMOFO_DICT_URL = chrome.runtime.getURL('./src/bopomofo_dict_with_frequency2.json');
    const CANJIE_DICT_URL = chrome.runtime.getURL('./src/canjie_dict_with_frequency.json');
    const ENGLISH_DICT_URL = chrome.runtime.getURL('./src/english_dict_with_frequency.json');
    const TOKEN_TYPE_LIST = {
        ENGLISH: "english",
        BOPOMOFO: "bopomofo",
        CANJIE: "canjie"
    }


    try {
        // load json
        const response1 = await fetch(BOPOMOFO_DICT_URL);
        const bopomofo_dict = await response1.json();

        const response2 = await fetch(CANJIE_DICT_URL);
        const canjie_dict = await response2.json();

        const response3 = await fetch(ENGLISH_DICT_URL);
        const english_dict = await response3.json();

        // build trie
        for (let key in bopomofo_dict) {
            trie.insert(key, bopomofo_dict[key], TOKEN_TYPE_LIST.BOPOMOFO);
        }
        for (let key in canjie_dict) { //need to fix json file
            trie.insert(key, canjie_dict[key], TOKEN_TYPE_LIST.CANJIE);
        }
        for (let key in english_dict) {
            trie.insert(key, english_dict[key], TOKEN_TYPE_LIST.ENGLISH);
        }
        return trie;

    } catch (error) {
        console.error('Error Building Trie from JSON files:', error);
    }
}