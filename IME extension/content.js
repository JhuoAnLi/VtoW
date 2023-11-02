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
}


// global variables
const SHOW_LENGTH = 5;
const SEARCH_DISTANCE = 3;
const NUM_OF_RESULT = 1;
let trie = new Trie();
let IMEActivated = false;
const TOKEN_TYPE_LIST = {
    ENGLISH: "english",
    BOPOMOFO: "bopomofo",
    CANJIE: "canjie"
}


chrome.storage.local.get(['IMEActivated'], function (result) {
    if (result.IMEActivated !== undefined) {
        IMEActivated = result.IMEActivated;
    }
});


chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    if (request.action === 'activate') {
        IMEActivated = true;
        console.log("IMEActivated", IMEActivated);
        chrome.storage.local.set({ IMEActivated: true });
    } else if (request.action === 'deactivate') {
        IMEActivated = false;
        console.log("IMEActivated", IMEActivated);
        chrome.storage.local.set({ IMEActivated: false });
    }
});


window.onload = async function () {
    const BOPOMOFO_DICT_URL = chrome.runtime.getURL('./src/bopomofo_dict_with_frequency2.json');
    const CANJIE_DICT_URL = chrome.runtime.getURL('./src/canjie_dict_with_frequency.json');
    const ENGLISH_DICT_URL = chrome.runtime.getURL('./src/english_dict_with_frequency.json');

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

        console.log("trie", trie);
        main();


    } catch (error) {
        console.error('Error loading JSON files:', error);
    }
};

const selectElement = document.createElement("select");
selectElement.id = "my-select";

const floatingElement = document.createElement("div");
floatingElement.id = "floatingElement";
floatingElement.style.position = "absolute";
floatingElement.style.zIndex = "999";
floatingElement.style.display = "none";
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

const div = document.createElement("div");

function main() {
    document.addEventListener("click", function (event) {

        if (event.target.tagName == "TEXTAREA" || event.target.tagName == "INPUT" || (event.target.tagName == "DIV" && event.target.contentEditable == "true")) {
            console.log("in textarea");

            const textarea = event.target;
            const selectElement = document.getElementById("select");
            if (selectElement) {
                selectElement.remove();
            }
            textarea.addEventListener("keydown", IMEHandler);
            textarea.addEventListener("input", updateFloatingElement);
            createDivWithSameStyles(textarea);

            function createDivWithSameStyles(textarea) {
                const textareaStyles = window.getComputedStyle(textarea);
                for (let prop of textareaStyles) {
                    div.style[prop] = textareaStyles[prop];
                }

                // Set the div to be invisible
                div.style.display = "none";
                div.style.visibility = "hidden"; 
                div.style.backgroundColor = "blue";
                div.style.opacity = "0.5";
                div.style.pointerEvents = "none";
                div.style.zIndex = "999";
                div.id = "my-div";
                // Position the div over the textarea
                const rect = textarea.getBoundingClientRect();
                div.style.position = "absolute";
                div.style.top = rect.top + "px";
                div.style.left = rect.left + "px";
                div.style.width = rect.width + "px";
                div.style.height = rect.height + "px";

                document.body.appendChild(div); // fix here
            }


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
            floatingElement.style.display = "none";
            return;
        }
    });
}

let buffer = "";
let cursorStartPosition = 0;

function IMEHandler(event) {
    // variable declaration
    let selectValue = "";
    let textarea = event.target;

    if (event.ctrlKey === true && event.key === "\\") {
        IMEActivated = !IMEActivated;
        console.log("IMEActivated", IMEActivated);
    }
    if (IMEActivated === false){
        buffer = "";
        floatingElement.style.display = "none";
        return;
    } 

    if (buffer == "") { // reset cursorStartPosition
        cursorStartPosition = event.target.selectionStart;
    }
    // console.log("event.key", event.key);
    // console.log("buffer", buffer);
    // console.log("cursorStartPosition", cursorStartPosition);

    switch (event.key) {
        case "Backspace":
            buffer = buffer.substring(0, buffer.length - 1);
            break;
        case "ArrowDown":
            if (buffer == "") return;
            pressArrowDown();
            break;
        case "Enter":
            console.log("IMEActivated", IMEActivated);
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
        floatingElement.style.display = "none";
        return;
    } else {
        floatingElement.style.display = "block";

        // version 1 inaccurate
        // const token_list = tokenizeString(buffer);
        // console.log("1", token_list);
        // const combined_token_list = combineTokens(token_list);
        // console.log("2", combined_token_list);
        // const possible_results = keyStrokeToString(combined_token_list);
        // console.log("3", possible_results);

        // version 2 slow need to fix
        // const token_list = tokenizeString2(buffer);
        // const combined_token_list = token_list;
        // console.log("combined_token_list", combined_token_list);
        // const possible_results = keyStrokeToString2(combined_token_list);


        // version 3
        const possible_token_dict = tokenizeString3(buffer);
        const possible_results = keyStrokeToString2(possible_token_dict);

        createOptions(possible_results);
    }

    function pressArrowDown() {
        selectElement.size = SHOW_LENGTH;
        selectElement.focus();
        selectElement.open = true;
        selectElement.addEventListener("keydown", selectionHandeler);
        event.preventDefault();
        event.stopPropagation();
    }

    function pressTab() {
        let selectValue = selectElement.options[0].value;
        textarea.value = textarea.value.substring(0, cursorStartPosition) + selectValue + textarea.value.substring(textarea.selectionStart, textarea.value.length);
        buffer = "";
        floatingElement.style.display = "none";
        textarea.setSelectionRange(cursorStartPosition + selectValue.length, cursorStartPosition + selectValue.length);
        textarea.focus();
        textarea.click();
        event.preventDefault();
        event.stopPropagation();
    }

    function predict() {
        const WORDS_BEFORE_PREDICT_LENGTH = 10;
        const query = textarea.value.substring(cursorStartPosition - WORDS_BEFORE_PREDICT_LENGTH, cursorStartPosition);

        predictiong_query(query).then((response) => {
            console.log(response);

            textarea.value = textarea.value + response[0].generated_text;
            buffer = "";
            floatingElement.style.display = "none";
        });
        event.preventDefault();
        event.stopPropagation();
    }


    let selectedIndex = 0;

    function selectionHandeler(event) {
        event.preventDefault();
        switch (event.key) {
            case "Tab":
            case "Enter":
                textarea.value = textarea.value.substring(0, cursorStartPosition) + selectValue + textarea.value.substring(textarea.selectionStart, textarea.value.length);
                floatingElement.style.display = "none";
                buffer = "";
                selectedIndex = 0;
                selectElement.size = 1;
                textarea.focus();
                textarea.click();
                textarea.setSelectionRange(cursorStartPosition + selectValue.length, cursorStartPosition + selectValue.length); // bad
                event.stopPropagation();
                selectElement.removeEventListener("keydown", selectionHandeler);
                return;
                break;
            case "Escape":
                floatingElement.style.display = "none";
                buffer = "";
                selectElement.size = 1;
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
    const data = { "inputs": `Q: Please continue writing the following sentences.\n\nSentence: ${input_string}` }
    const response = await fetch(
        "https://api-inference.huggingface.co/models/google/flan-t5-base", {
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


let keyStrokeCatch = {};
/**
 * @param {string} query
 * @param {Trie} trie
 * @param {number} num_of_result
 * @return {array} array of objects of the form {distance, keySoFar, value} 
 */
function findClosestMatches(query, trie, num_of_result = NUM_OF_RESULT) {
    if (query in keyStrokeCatch) {
        return keyStrokeCatch[query];
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

    traverse(trie.root, "");

    minHeap.sort((a, b) => a[0] - b[0]);

    const result = minHeap.slice(0, num_of_result).map(result => ({
        "distance": result[0],
        "keySoFar": result[1],
        "value": result[2]
    }));
    keyStrokeCatch[query] = result;

    // const CUT_OFF_LENGTH = 100;
    // if (Object.keys(keyStrokeCatch).length > CUT_OFF_LENGTH) { // cut off the first n elements
    //     const keys = Object.keys(keyStrokeCatch).slice(CUT_OFF_LENGTH/2);
    //     keyStrokeCatch = Object.fromEntries(keys.map(key => [key, keyStrokeCatch[key]]));
    // }
    return result
}


/**
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
    inputarray = inputarray.filter(element => element !== "");
    return inputarray;
}


/**
 * @param {array} keyStrokeArray 
 * @returns {array} string array of possible results
 */
function keyStrokeToString(keyStrokeArray) {
    let outputarray = ["", "", "", "", ""];
    for (let i = 0; i < keyStrokeArray.length; i++) {
        let result = findClosestMatches(keyStrokeArray[i], trie, 5);

        if (result[0].distance === 0) {
            if (result[0].value.length === 1) {
                for (let k = 0; k < outputarray.length; k++) {
                    outputarray[k] = outputarray[k] + result[0].value[0].word;
                }
            } else {
                for (let j = 0; j < outputarray.length; j++) {
                    if (result[0].value[j] !== undefined) {
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

function keyStrokeToString2(slice_dict) {
    let result = [];
    for (let i = 0; i < slice_dict.length; i++) {
        const keyStrokeArray = slice_dict[i].arr;

        let poss = [];
        keyStrokeArray.forEach((element) => {
            poss.push(findClosestMatches(element, trie, 5))
        });
        result = [...result, ...generateCombinations(poss)];


    
        function generateCombinations(originalList) {
            const resultList = [];
    
            function generate(index, currentCombination, currentScore) {
                if (index === originalList.length) {
                    resultList.push({ str: currentCombination, score: currentScore });
                    return;
                }
    
                const currentDimension = originalList[index];
                for (let element of currentDimension) {
                    for (let wordObj of element.value) {
                        generate(
                            index + 1,
                            currentCombination + wordObj.word,
                            currentScore + wordObj.freq
                        );
                    }
                }
            }
    
            generate(0, '', 0);
    
            return resultList;
        }
    }
    result = result.sort((a, b) => b.score - a.score);
    result = result.map(element => element.str);

    result.splice(1, 0, slice_dict[0].arr.join(""));
    result = [...new Set(result)] // remove duplicates
    return result;
}

function tokenizeString2(input_string) {
    return cutStringWithMinScore(input_string, scoreFunction);

    function cutStringWithMinScore(string, scoreFunction) {
        const n = string.length;
        const dp = new Array(n).fill(Infinity);
        const tokens = new Array(n).fill('');
        const scoreCache = {};

        for (let i = 0; i < n; i++) {
            let prevDP = i > 0 ? dp.slice() : null;
            for (let j = 0; j <= i; j++) {
                const subString = string.substring(j, i + 1);

                if (j === 0) {
                    dp[i] = getScore(subString, null);
                    tokens[i] = subString;
                } else {
                    const prevToken = tokens[j - 1];
                    const tokenScore = getScore(subString, prevToken);
                    const newScore = (prevDP ? prevDP[j - 1] : 0) + tokenScore;

                    if (newScore < dp[i]) {
                        dp[i] = newScore;
                        tokens[i] = subString;
                    }
                }
            }
        }

        // Reconstruct the tokens with minimum score
        const resultTokens = [];
        let i = n - 1;
        while (i >= 0) {
            resultTokens.unshift(tokens[i]);
            i -= tokens[i].length;
        }

        return resultTokens.filter((token) => token !== ''); // Filter out empty tokens

        function getScore(subString, prevToken) {
            const cacheKey = `${subString}-${prevToken}`;

            if (cacheKey in scoreCache) {
                return scoreCache[cacheKey];
            }

            const tokenScore = scoreFunction(subString, prevToken);
            scoreCache[cacheKey] = tokenScore;
            return tokenScore;
        }
    }
    function scoreFunction(string, prevToken_string) {
        let score = 0;
        const currentToken = findClosestMatches(string, trie, 1)[0];
        const current_token_type = currentToken.value[0].type;
        const distance = currentToken.distance;

        if (prevToken_string === null || prevToken_string === undefined) {
            score = 0;
        } else {
            const prevToken = findClosestMatches(prevToken_string, trie, 1)[0];
            const pre_token_type = prevToken.value[0].type;
            if (current_token_type !== pre_token_type) {
                score = 1;
            } else {
                score = -1;
            }
        }

        const ALPHA = 0.6;
        const BETA = 1.1;
        if (distance === 0) {
            score += 0;
        } else {
            score += BETA * distance - ALPHA * string.length;
        }
        return score;
    }
}

function scoreFunction(string, prevToken_string) {
    let score = 0;
    const currentToken = findClosestMatches(string, trie, 1)[0];
    const current_token_type = currentToken.value[0].type;
    const distance = currentToken.distance;

    if (prevToken_string === null || prevToken_string === undefined) {
        score = 0;
    } else {
        const prevToken = findClosestMatches(prevToken_string, trie, 1)[0];
        const pre_token_type = prevToken.value[0].type;
        if (current_token_type !== pre_token_type) {
            score = 1;
        } else {
            score = -1;
        }
    }

    const ALPHA = 0.3;
    const BETA = 1;
    if (distance === 0) {
        score += 0;
    } else {
        score += BETA * distance - ALPHA * string.length;
    }
    return score;
}

function tokenizeString3(inputString) {
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

    token_arrary = combineTokens(token_arrary);

    token = "";
    let new_token_arrary = [];
    for (let i = 0; i < inputString.length; i++) {
        if (inputString[i] === ' ') {
            new_token_arrary.push(token);
            new_token_arrary.push(inputString[i]);
            token = "";
        } else {
            token = token + inputString[i];
        }
    }
    if (token != "") new_token_arrary.push(token);

    const token_arrary_score = token_arrary.reduce((total, element) => total + scoreFunction(element), 0);
    const new_token_arrary_score = new_token_arrary.reduce((total, element) => total + scoreFunction(element), 0);
    return [{arr: token_arrary, score: token_arrary_score}, {arr: new_token_arrary, score: new_token_arrary_score}]
}