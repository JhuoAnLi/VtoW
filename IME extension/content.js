"use strict";

window.onload = async function () {
    let my_IMEHandler = new MyIMEHandler();
    
    document.addEventListener("click", function (event) {
        if (event.target.tagName == "TEXTAREA" || event.target.tagName == "INPUT" || (event.target.tagName == "DIV" && event.target.contentEditable == "true")) {
            console.log("in textarea");
            const textarea = event.target;
            my_IMEHandler.bindToTextarea(textarea);
        } else {
            console.log("not in textarea");
            return;
        }
    });


    chrome.storage.local.get(['IMEActivated'], function (result) {
        if (result.IMEActivated !== undefined) {
            my_IMEHandler.setActivated(result.IMEActivated);
        }
    });
    
    
    chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
        if (request.action === 'activate') {
            my_IMEHandler.setActivated(true);
            console.log("IMEActivated", my_IMEHandler.activated);
            chrome.storage.local.set({ IMEActivated: true });
        } else if (request.action === 'deactivate') {
            my_IMEHandler.setActivated(false);
            console.log("IMEActivated", my_IMEHandler.activated);
            chrome.storage.local.set({ IMEActivated: false });
        }
    });
};


// function keyStrokeToString2(slice_dict) {
//     let result = [];
//     for (let i = 0; i < slice_dict.length; i++) {
//         const keyStrokeArray = slice_dict[i].arr;

//         let poss = [];
//         keyStrokeArray.forEach((element) => {
//             poss.push(findClosestMatches(element, trie, 5))
//         });
//         result = [...result, ...generateCombinations(poss)];


    
//         function generateCombinations(originalList) {
//             const resultList = [];
    
//             function generate(index, currentCombination, currentScore) {
//                 if (index === originalList.length) {
//                     resultList.push({ str: currentCombination, score: currentScore });
//                     return;
//                 }
    
//                 const currentDimension = originalList[index];
//                 for (let element of currentDimension) {
//                     for (let wordObj of element.value) {
//                         generate(
//                             index + 1,
//                             currentCombination + wordObj.word,
//                             currentScore + wordObj.freq
//                         );
//                     }
//                 }
//             }
    
//             generate(0, '', 0);
    
//             return resultList;
//         }
//     }
//     result = result.sort((a, b) => b.score - a.score);
//     result = result.map(element => element.str);

//     result.splice(1, 0, slice_dict[0].arr.join(""));
//     result = [...new Set(result)] // remove duplicates
//     return result;
// }

// function tokenizeString2(input_string) {
//     return cutStringWithMinScore(input_string, scoreFunction);

//     function cutStringWithMinScore(string, scoreFunction) {
//         const n = string.length;
//         const dp = new Array(n).fill(Infinity);
//         const tokens = new Array(n).fill('');
//         const scoreCache = {};

//         for (let i = 0; i < n; i++) {
//             let prevDP = i > 0 ? dp.slice() : null;
//             for (let j = 0; j <= i; j++) {
//                 const subString = string.substring(j, i + 1);

//                 if (j === 0) {
//                     dp[i] = getScore(subString, null);
//                     tokens[i] = subString;
//                 } else {
//                     const prevToken = tokens[j - 1];
//                     const tokenScore = getScore(subString, prevToken);
//                     const newScore = (prevDP ? prevDP[j - 1] : 0) + tokenScore;

//                     if (newScore < dp[i]) {
//                         dp[i] = newScore;
//                         tokens[i] = subString;
//                     }
//                 }
//             }
//         }

//         // Reconstruct the tokens with minimum score
//         const resultTokens = [];
//         let i = n - 1;
//         while (i >= 0) {
//             resultTokens.unshift(tokens[i]);
//             i -= tokens[i].length;
//         }

//         return resultTokens.filter((token) => token !== ''); // Filter out empty tokens

//         function getScore(subString, prevToken) {
//             const cacheKey = `${subString}-${prevToken}`;

//             if (cacheKey in scoreCache) {
//                 return scoreCache[cacheKey];
//             }

//             const tokenScore = scoreFunction(subString, prevToken);
//             scoreCache[cacheKey] = tokenScore;
//             return tokenScore;
//         }
//     }
//     function scoreFunction(string, prevToken_string) {
//         let score = 0;
//         const currentToken = findClosestMatches(string, trie, 1)[0];
//         const current_token_type = currentToken.value[0].type;
//         const distance = currentToken.distance;

//         if (prevToken_string === null || prevToken_string === undefined) {
//             score = 0;
//         } else {
//             const prevToken = findClosestMatches(prevToken_string, trie, 1)[0];
//             const pre_token_type = prevToken.value[0].type;
//             if (current_token_type !== pre_token_type) {
//                 score = 1;
//             } else {
//                 score = -1;
//             }
//         }

//         const ALPHA = 0.6;
//         const BETA = 1.1;
//         if (distance === 0) {
//             score += 0;
//         } else {
//             score += BETA * distance - ALPHA * string.length;
//         }
//         return score;
//     }
// }

// function scoreFunction(string, prevToken_string) {
//     let score = 0;
//     const currentToken = findClosestMatches(string, trie, 1)[0];
//     const current_token_type = currentToken.value[0].type;
//     const distance = currentToken.distance;

//     if (prevToken_string === null || prevToken_string === undefined) {
//         score = 0;
//     } else {
//         const prevToken = findClosestMatches(prevToken_string, trie, 1)[0];
//         const pre_token_type = prevToken.value[0].type;
//         if (current_token_type !== pre_token_type) {
//             score = 1;
//         } else {
//             score = -1;
//         }
//     }

//     const ALPHA = 0.3;
//     const BETA = 1;
//     if (distance === 0) {
//         score += 0;
//     } else {
//         score += BETA * distance - ALPHA * string.length;
//     }
//     return score;
// }

// function tokenizeString3(inputString) {
//     let token = "";
//     let token_arrary = [];
//     for (let i = 0; i < inputString.length; i++) {
//         if (inputString[i] === ' ' || inputString[i] === '3' || inputString[i] === '4' || inputString[i] === '6' || inputString[i] === '7') {
//             token = token + inputString[i];
//             token_arrary.push(token);
//             token = "";
//         } else {
//             token = token + inputString[i];
//         }
//     }
//     if (token != "") token_arrary.push(token);

//     token_arrary = combineTokens(token_arrary);

//     token = "";
//     let new_token_arrary = [];
//     for (let i = 0; i < inputString.length; i++) {
//         if (inputString[i] === ' ') {
//             new_token_arrary.push(token);
//             new_token_arrary.push(inputString[i]);
//             token = "";
//         } else {
//             token = token + inputString[i];
//         }
//     }
//     if (token != "") new_token_arrary.push(token);

//     const token_arrary_score = token_arrary.reduce((total, element) => total + scoreFunction(element), 0);
//     const new_token_arrary_score = new_token_arrary.reduce((total, element) => total + scoreFunction(element), 0);
//     return [{arr: token_arrary, score: token_arrary_score}, {arr: new_token_arrary, score: new_token_arrary_score}]
// }


// function shiff(array1, array2){
//     let result_list = [];

//     let array1_index = 0;
//     let array2_index = 0;
//     let array1_score = 0;
//     let array2_score = 0;
//     let array1_sub = [];
//     let array2_sub = [];
    

//     while (array1_index < array1.length && array2_index < array2.length){
//         console.log("here in shiff:", array1_sub, array2_sub);
//         if (array1_sub.length < array2_sub.length){
//             console.log("chanage here");
//             array1_score += trie.findClosestMatches(array1[array1_index], 1)[0].distance;
//             array1_sub.push(array1[array1_index]);
//             array1_index++;
//         }else if (array1_sub.length > array2_sub.length){
//             console.log("chanage here");
//             array2_score += trie.findClosestMatches(array2[array2_index], 1)[0].distance;
//             array2_sub.push(array2[array2_index]);
//             array2_index++;
//         }else {
//             if (array1_score < array2_score){
//                 result_list.push(array1_sub);
//             }else {
//                 result_list.push(array2_sub);
//             }
//             array1_sub = [];
//             array2_sub = [];
//             array1_index++;
//             array2_index++;
//         }
//     }
//     console.log("out in shiff:", array1_sub, array2_sub);
//     return result_list;
// }
// const firstTokenArray = ["su3", "cl3", " ", "this ", "is "];
// const secondTokenArray = ["su3cl3", " ", "this", " ", "is", " "];
// const shiffTokenArray = shiff(firstTokenArray, secondTokenArray);
// console.log("here shiff:", shiffTokenArray);
