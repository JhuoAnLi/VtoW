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
let IMEActivated = true;
const SHOW_LENGTH = 5;
const SEARCH_DISTANCE = 3;
const NUM_OF_RESULT = 1;
let trie = new Trie();


window.onload = async function () {
    const BOPOMOFO_DICT_URL = chrome.runtime.getURL('./src/bopomofo_dict_with_frequency2.json');
    const CANJIE_DICT_URL = chrome.runtime.getURL('./src/canjie_dict_with_frequency.json');

    try {
        // load json
        const response1 = await fetch(BOPOMOFO_DICT_URL);
        const bopomofo_dict = await response1.json();

        const response2 = await fetch(CANJIE_DICT_URL);
        const canjie_dict = await response2.json();

        // build trie
        for (let key in bopomofo_dict) {
            trie.insert(key, bopomofo_dict[key]);
        }
        for (let key in canjie_dict) { //need to fix json file
            trie.insert(key, canjie_dict[key]); 
        }

        if (IMEActivated) {
            main();
        }


    } catch (error) {
        console.error('Error loading JSON files:', error);
    }
};

const selectElement = document.createElement("select");
selectElement.id = "my-select";
selectElement.style.display = "block";

const floatingElement = document.createElement("div");
floatingElement.id = "floatingElement";
floatingElement.style.position = "absolute";
floatingElement.style.zIndex = "999";
floatingElement.appendChild(selectElement);
document.body.appendChild(floatingElement);

const hiddenDiv = document.createElement("div");
hiddenDiv.id = "hiddenDiv";
hiddenDiv.style.display = "inline-block";
hiddenDiv.style.position = "absolute";
hiddenDiv.style.top = "-9999px";
hiddenDiv.style.left = "-9999px";
hiddenDiv.style.visibility = "hidden";
document.body.appendChild(hiddenDiv);


function main(){
    document.addEventListener("click", function (event) {

        if (event.target.tagName == "TEXTAREA" || event.target.tagName == "INPUT" || (event.target.tagName == "DIV" && event.target.contentEditable == "true")) {
            console.log("in textarea");

            const textarea = event.target;
            document.getElementById("select")?.remove();
            textarea.addEventListener("keydown", IMEHandler);
            textarea.addEventListener("input", updateFloatingElement);
            
            function updateFloatingElement() {
                const cursorPosition = getCaretCoordinates();
                const textareaRect = textarea.getBoundingClientRect();
    
                const top = textareaRect.top + window.scrollY + cursorPosition.top + 15; // Adjust top position as needed
                const left = textareaRect.left + window.scrollX + cursorPosition.left; // Adjust left position as needed
                
                // console.log("top", top, "left", left);
                floatingElement.style.top = top + "px";
                floatingElement.style.left = left + "px";
            }
    
            function getCaretCoordinates() {
                const text = textarea.value.substring(0, textarea.selectionStart);
                hiddenDiv.textContent = text;
                const rect = hiddenDiv.getBoundingClientRect();
                return {
                    top: rect.height,
                    left: rect.width,
                };
            }
        } else {
            buffer = "";
            console.log("not in textarea");
            return;
        }
    });
}

let buffer = "";
let cursorStartPosition = 0;
function IMEHandler(event){
    // variable declaration
    let selectValue = "";
    let textarea = event.target;

    if (buffer == "") { // reset cursorStartPosition
        // console.log("buffer is empty reset cursorStartPosition");
        cursorStartPosition = event.target.selectionStart;  
    }
    console.log("buffer", buffer);
    // console.log("cursorStartPosition", cursorStartPosition);

    console.log("event.key", event.key)
    switch (event.key) {
        case "Backspace":
            buffer = buffer.substring(0, buffer.length - 1);
            break;
        case "ArrowDown":
            if (buffer == "") return;
            pressArrowDown();
            break;
        case "Enter":
            break;
        case "ArrowLeft":
        case "ArrowRight":
            buffer = "";
            break;
        case "`":
            predict();
            break;
        case "Tab":
            if (buffer == "") return;
            pressTab();
            break;
        case "Escape":
            buffer = "";
            break;
        default:
            if (/^[a-zA-Z0-9 `=\[\];',.\/~!@#\$%^&*()_+{}:"<>?-]$/.test(event.key)) {
                buffer = buffer + event.key;
            } else {
                console.log("else part");
            }
            break;
    }

    if (buffer == "") {
        selectElement.style.display = "none";
        return;
    }else{
        selectElement.style.display = "block";
        const token_list = tokenizeString(buffer);
        // console.log("1", token_list);
        const combined_token_list = combineTokens(token_list);
        // console.log("2", token_list);
        const possible_results = keyStrokeToString(combined_token_list);
        // console.log("3", possible_results);

        createOptions(possible_results);
    }

    function pressArrowDown(){
        selectElement.size = SHOW_LENGTH;
        selectElement.focus();
        selectElement.open = true;
        selectElement.addEventListener("keydown", selectionHandeler);
        event.preventDefault();
        event.stopPropagation();
    }

    function pressTab(){
        let selectValue = selectElement.options[0].value;
        textarea.value = textarea.value.substring(0, cursorStartPosition) + selectValue + textarea.value.substring(textarea.selectionStart, textarea.value.length);
        buffer = "";
        selectElement.style.display = "none";
        textarea.setSelectionRange(cursorStartPosition + selectValue.length, cursorStartPosition + selectValue.length);
        textarea.focus();
        textarea.click();
        event.preventDefault();
        event.stopPropagation();
    }

    function predict(){
        const WORDS_BEFORE_PREDICT_LENGTH = 10;
        const query = textarea.value.substring(cursorStartPosition - WORDS_BEFORE_PREDICT_LENGTH, cursorStartPosition);

        predictiong_query(query).then((response) => {
            console.log(response);
            
            textarea.value = textarea.value + response[0].generated_text;
            buffer = "";
            selectElement.style.display = "none";
        });
        event.preventDefault();
        event.stopPropagation();
    }


    let selectedIndex = 0;
    function selectionHandeler(event) {
        // console.log("in selectionHandeler", selectedIndex);
        
        event.preventDefault();
        switch (event.key) {
            case "Enter":
                textarea.value = textarea.value.substring(0, cursorStartPosition) + selectValue + textarea.value.substring(textarea.selectionStart, textarea.value.length);
                selectElement.style.display = "none";
                buffer = "";
                selectedIndex = 0;
                textarea.focus();
                textarea.click();
                textarea.setSelectionRange(cursorStartPosition + selectValue.length, cursorStartPosition + selectValue.length); // bad
                event.stopPropagation();
                selectElement.removeEventListener("keydown", selectionHandeler);
                return;
                break;
            case "Escape":
                selectElement.style.display = "none";
                buffer = "";
                textarea.focus();
                break;
            case "ArrowUp":
                selectedIndex = (selectedIndex - 1 + selectElement.options.length) % selectElement.options.length;
                break;
            case "ArrowDown":
                selectedIndex = (selectedIndex + 1) % selectElement.options.length;
                break;
            default:
                console.log("else part");
                break;
        }
        selectElement.options[selectedIndex].selected = true;
        selectValue = selectElement.options[selectedIndex].value;
        event.stopPropagation();
    };
}

function createOptions(possible_results) {
  selectElement.innerHTML = "";
  possible_results.forEach(function (value) {
    let option = document.createElement("option");
    option.classList.add("my-option");
    option.value = value;
    option.textContent = value;
    selectElement.appendChild(option);
  });
}

async function predictiong_query(input_string) {
    // const data = {"inputs": `Please predict the next two words of ths sentence "${input_string}"`}
    const data = {"inputs": `Q: Please continue writing the following sentences.\n\nSentence: ${input_string}`}
	const response = await fetch(
		"https://api-inference.huggingface.co/models/google/flan-t5-base",
		{
			headers: { Authorization: "Bearer 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" },
			method: "POST",
			body: JSON.stringify(data),
		}
	);
	const result = await response.json();
	return result;
}

/**
 * @param {string} inputString
 * @return {array} possible results
 */
function tokenizeString(inputString) {
    let token = "";
    let token_arrary = [];
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
function findClosestMatches(query, trie, num_of_result = NUM_OF_RESULT) {
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

    return minHeap.slice(0, num_of_result).map(result => ({
        "distance": result[0],
        "keySoFar": result[1],
        "value": result[2]
    }));
}


/**
 * 
 * @param {array} inputarray 
 * @returns {array} string array of combined tokens
 */
function combineTokens(inputarray) {
    inputarray.push("");
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

let keyStrokeCatch = [];
/**
 * 
 * @param {array} keyStrokeArray 
 * @returns {array} string array of possible results
 */
function keyStrokeToString(keyStrokeArray) {
    let outputarray = ["", "", "", "", ""];
    for (let i = 0; i < keyStrokeArray.length; i++) {
        let result = [];
        if (keyStrokeArray[i] in keyStrokeCatch) {
            result = keyStrokeCatch[keyStrokeArray[i]];
        }else{
            result = findClosestMatches(keyStrokeArray[i], trie, 5);
            keyStrokeCatch[keyStrokeArray[i]] = result;
        }

        if (result[0].distance === 0) {
            if (result[0].value.length === 1) {
                for (let k = 0; k < outputarray.length; k++) {
                    outputarray[k] = outputarray[k] + result[0].value[0].word;
                }
            } else {
                for (let j = 0; j < outputarray.length; j++) {
                    if (result[0].value[j] !== undefined){
                        outputarray[j] = outputarray[j] + result[0].value[j].word;
                    }
                }
            }
        } else {
            for (let y = 0; y < outputarray.length; y++) {
                outputarray[y] = outputarray[y] + keyStrokeArray[i];
            }
        }
    }
    outputarray.splice(1, 0, keyStrokeArray.join(""));
    outputarray = [...new Set(outputarray)] // remove duplicates
    return outputarray;
}