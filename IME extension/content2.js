console.log("content2.js loaded");

document.addEventListener("input", function (event) {
  if (event.target.tagName === "INPUT" || event.target.tagName === "TEXTAREA") {

    let textarea = event.target;
    let existingSelect = textarea.nextElementSibling;
    let selectVisible = false;
    let selectedIndex = 0;
    let buffer = ""

    textarea.addEventListener("keydown", function (event) {
      // event.preventDefault();

      console.log(event.key, event.ctrlKey, event.altKey, event.shiftKey, event.metaKey);
      buffer += event.key;
      if (event.key === " ") {
        // call serach function
      }
    });
  }
});

console.log("forground");

let bopomofo_dict_url = chrome.runtime.getURL('./src/bopomofo_dict_with_frequency2.json');
// let bopomofo_dict


fetch(bopomofo_dict_url)
  .then((response) => bopomofo_dict = response.json()) // file contains json
  .then((json) => {
    console.log(json)
    // Example usage:
    // Assume my_dict and my_dict2 are defined before this point
    let bopomofo_dict = json;
    let trie = new Trie();
    console.log(bopomofo_dict);
    // Insert keys into the trie
    for (let key in bopomofo_dict) {
      trie.insert(key, bopomofo_dict[key]);
    }


    while (true) {
      let queryString = prompt("Enter a query:");
      if (!queryString) {
        break;
      }

      let closestMatches = findClosestMatches(queryString, trie, 5);
      console.log("Closest 5 matches:");
      for (let match of closestMatches) {
        console.log(`Key: ${match[1]}, Value: ${match[0]}, Distance: ${match[2]}`);
      }
    }
  });



class TrieNode {
  constructor() {
    this.children = {};
    this.value = null;
  }
}
class Trie {
  constructor() {
    this.root = new TrieNode();
  }

  insert(key, value) {
    let node = this.root;
    for (let char of key) {
      if (!(char in node.children)) {
        node.children[char] = new TrieNode();
      }
      node = node.children[char];
    }
    node.value = value;
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

function findClosestMatches(query, trie, k = 5) {
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

  traverse(trie.root, "");

  minHeap.sort((a, b) => a[0] - b[0]);

  return minHeap.slice(0, k).map(result => [result[1], result[2], result[0]]);
}


