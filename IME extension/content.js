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
  }

  insert(key, value) {
    let node = this.root;
    for (let char of key) {
      if (!(char in node.children)) {
        node.children[char] = new TrieNode();
      }
      node = node.children[char];
    }
    node.value = value.map((element) => ({
      word: element[0],
      frequency: element[1]
    }));
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


// global variables
let SecondPara = document.getElementById("Alh6id");
SecondPara.remove();
let buffer = "";
let backendoutputarray = [];
let trie = new Trie();
let BOPOMOFO_DICT_URL = chrome.runtime.getURL('./src/bopomofo_dict_with_frequency2.json');

fetch(BOPOMOFO_DICT_URL).then((response) => response.json()).then((json) => {
  let bopomofo_dict = json;
  for (let key in bopomofo_dict) {
    trie.insert(key, bopomofo_dict[key]);
  }
  // let textarea = document.getElementsByTagName("textarea")[0];


  document.addEventListener("keydown", function (event) {
    if (event.target.tagName !== "TEXTAREA") {
      console.log("not in textarea");
      return;
    }
    // console.log("in textarea");
    console.log("key: ", event.key);

    if (event.key === "Backspace") {
      buffer = buffer.substring(0, buffer.length - 1);
    } else if (/^[a-zA-Z0-9-\=\[\]\;\'\,\.\/ ]$/.test(event.key)) { 
      buffer = buffer + event.key;
    } else {
      console.log("else part");
    }
    console.log("buffer: ", buffer);

    let token_list = tokenizeString(buffer);
    console.log("1", token_list);
    token_list = combineTokens(token_list);
    console.log("2", token_list);
    let possible_results = keyStrokeToString(token_list);
    console.log(possible_results);

    // let selectElement = document.createElement("select");
    // possible_results.forEach(function (value) {
    //   let option = document.createElement("option");
    //   option.value = value;
    //   option.textContent = value;
    //   selectElement.appendChild(option);
    // });
    // selectElement.size = backendoutputarray.length;
    // selectElement.style.display = "none";
    // event.target.parentNode.appendChild(selectElement);
  });
});

/**
  * @param {string} inputString
  * @return {array} possible results
  */
function tokenizeString(inputString) {
  let token = "";
  let token_arrary = [];
  console.log(inputString);
  for (let i = 0; i < inputString.length; i++) {
    if (inputString[i] === ' ' || inputString[i] === '3' || inputString[i] === '4' || inputString[i] === '6' || inputString[i] === '7') {
      token = token + inputString[i];
      token_arrary.push(token);
      token = "";
    } else {
      token = token + inputString[i];
    }
  }
  if (token != "") token_arrary.push(token);
  return token_arrary;
}

/**
 * 
 * @param {string} s1 
 * @param {string} s2 
 * @returns {number} Levenshtein Distance of s1 and s2
 */
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


/**
 * @param {string} query
 * @param {Trie} trie
 * @param {number} num_of_result
 * @return {array} array of objects of the form {distance, keySoFar, value} 
 */
function findClosestMatches(query, trie, num_of_result = 5) {
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

  return minHeap.slice(0, num_of_result).map(result => (
    {
      "distance": result[0],
      "keySoFar": result[1],
      "value": result[2]
    }
  ));
}


/**
 * 
 * @param {array} inputarray 
 * @returns {array} string array of combined tokens
 */
function combineTokens(inputarray) {
  let newInputArray = [];
  while (true) {
    newInputArray = [];
    let modified = false;
    for (let i = 0; i < inputarray.length - 1; i++) {
      let combinedString = inputarray[i] + inputarray[i + 1];
      let combinedDistance = findClosestMatches(combinedString, trie, 1)[0].distance;
      if (combinedDistance === 0) {
        newInputArray.push(combinedString);
        i++;
        modified = true;
      } else {
        newInputArray.push(inputarray[i]);
      }
    }
    if (modified === true) {
      inputarray = newInputArray;
    } else {
      break;
    }
  }
  return inputarray;
}

/**
 * 
 * @param {array} keyStrokeArray 
 * @returns {array} string array of possible results
 */
function keyStrokeToString(keyStrokeArray) { // fix this function
  let outputarray = ["", "", "", "", ""];
  for (let i = 0; i < keyStrokeArray.length; i++) {
    let result = findClosestMatches(keyStrokeArray[i], trie, 5);
    if (result[0].distance === 0) {
      console.log("distance is 0");
      outputarray.forEach((element, index) => {
        console.log(result[0].value[0].word)
        outputarray[index] = element + result[0].value[0].word; // fix this
      });
    } else {
      for (let j = 0; j < outputarray.length; j++) {
        outputarray[j] = outputarray[j] + result[j].value[0].word;
      }
    }
  }
  return outputarray;
}