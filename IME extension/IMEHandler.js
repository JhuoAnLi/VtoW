SHOW_LENGTH = 5;

class MyIMEHandler {
    constructor(textarea) {
        
        build_Trie().then((response) => { // fix: bad code here
            this.trie = response
            this.activated = true;

            this.buffer = "";
            this.cursorStartPosition = 0;
            this.selectedIndex = 0;
            this.selectElement = this.createSelectElement();
            this.floatingElement = this.createFloatingElement();
            this.hiddenDiv = this.createHiddenDiv();

            this.textarea = textarea;
            // this.textarea.getBoundingClientRect();
    
            this.buffer = "";
            this.cursorStartPosition = 0;

    
            // this.textarea.addEventListener("input", this.updateFloatingElement.bind(this));
            // this.textarea.addEventListener("keydown", this.typeingHandler.bind(this));

            console.log("IMEHandler created");
        });
    }


    bindToTextarea(textarea) { // fix: bind does not work
        if (textarea === undefined) return;
        if (this.textarea === textarea){
            this.buffer = "";
            this.selectedIndex = 0;
            return;
        }

        if (this.textarea !== undefined){
            this.textarea.removeEventListener("input", this.updateFloatingElement);
            this.textarea.removeEventListener("keydown", this.typeingHandler);
        }
        console.log("unbind to textarea")
        this.textarea = textarea;
        this.textarea.getBoundingClientRect();

        this.buffer = "";
        this.cursorStartPosition = 0;
        this.selectedIndex = 0;

        this.textarea.addEventListener("input", this.updateFloatingElement.bind(this));
        this.textarea.addEventListener("keydown", this.typeingHandler.bind(this));

        console.log("bind to textarea");

    }

    createFloatingElement() {
        const element = document.createElement("div");
        element.id = "floatingElement";
        element.style.position = "absolute";
        element.style.zIndex = "999";
        element.style.display = "none";
        element.appendChild(this.selectElement);
        document.body.appendChild(element);
        return element;
    }

    createSelectElement() {
        const element = document.createElement("select");
        element.addEventListener("keydown", this.selectionHandeler.bind(this));
        element.id = "my-select";
        return element;
    }

    createHiddenDiv() {
        const div = document.createElement("div");
        div.id = "hiddenDiv";
        div.style.display = "inline-block";
        div.style.position = "absolute";
        div.style.top = "-9999px";
        div.style.left = "-9999px";
        div.style.visibility = "hidden";
        document.body.appendChild(div);
        return div;
    }

    createOptions(possible_results) {
        this.selectElement.innerHTML = "";
        possible_results.forEach(function (value) {
            let option = document.createElement("option");
            option.classList.add("my-option");
            option.value = value;
            option.textContent = value;
            this.selectElement.appendChild(option);
        }.bind(this));
    }

    updateFloatingElement() {
        const textareaRect = this.textarea.getBoundingClientRect();
        const getCaretCoordinates = () => {
            const text = this.textarea.value.substring(0, this.textarea.selectionStart);
            this.hiddenDiv.textContent = text;
            const rect = this.hiddenDiv.getBoundingClientRect();
            return {
                top: rect.height,
                left: rect.width,
            };
        };
        const cursorPosition = getCaretCoordinates();

        const top = textareaRect.top + window.scrollY + cursorPosition.top + 15; // Adjust top position as needed
        const left = textareaRect.left + window.scrollX + cursorPosition.left; // Adjust left position as needed

        this.floatingElement.style.top = top + "px";
        this.floatingElement.style.left = left + "px";
    }

    typeingHandler(event) {
        if (event.ctrlKey === true && event.key === "\\") {
            this.activated = !this.activated;
            console.log("IMEActivated", this.activated);
        }
        if (this.activated === false) {
            this.buffer = "";
            this.floatingElement.style.display = "none";
            return;
        }

        if (this.buffer == "") { // reset cursorStartPosition
            this.cursorStartPosition = event.target.selectionStart;
        }

        const arrowDown = () => {
            this.selectElement.size = SHOW_LENGTH;
            this.selectElement.focus();
            this.selectElement.open = true;
            this.selectedIndex = 0;
            event.preventDefault();
            event.stopPropagation();
        }

        const pressTab = () => {
            let selectValue = this.selectElement.options[0].value;
            this.textarea.value = this.textarea.value.substring(0, this.cursorStartPosition) + selectValue + this.textarea.value.substring(this.textarea.selectionStart, this.textarea.value.length);
            this.buffer = "";
            this.floatingElement.style.display = "none";
            this.textarea.setSelectionRange(this.cursorStartPosition + selectValue.length, this.cursorStartPosition + selectValue.length);
            this.textarea.focus();
            this.textarea.click();
            event.preventDefault();
            event.stopPropagation();
        }

        switch (event.key) {
            case "Backspace":
                this.buffer = this.buffer.substring(0, this.buffer.length - 1);
                break;
            case "ArrowDown":
                if (this.buffer == "") return; // fix: bad code here
                arrowDown();
                break;
            case "Enter":
                console.log("IMEActivated", this.activated);    
                break;
            case "ArrowLeft":
            case "ArrowRight":
                this.buffer = "";
                break;
            // case "`":
            //     predict();
            //     break;
            case "Tab":
                if (this.buffer == "") return;
                pressTab();
                break;
            case "Escape":
                this.buffer = "";
                break;
            default:
                if (/^[a-zA-Z0-9 `=\[\];',.\/~!@#\$%^&*()_+{}:"<>?-]$/.test(event.key)) {
                    this.buffer = this.buffer + event.key;
                } else {
                    console.log("else part: unrecognized key");
                }
                break;
        }

        if (this.buffer == "") {
            this.floatingElement.style.display = "none";
            return;
        } else {
            this.floatingElement.style.display = "block";
            
            console.log("buffer", this.buffer)
            // version 3
            const possible_token_dict = tokenizeString3(this.buffer, this.trie);
            const possible_results = keyStrokeToString2(possible_token_dict, this.trie);
            this.createOptions(possible_results);
        }


        function tokenizeString3(inputString, trie) {
            function firstTokenizer(inputString) {
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

            function secondTokenizer(inputString) {
                let token = "";
                let token_arrary = [];
                for (let i = 0; i < inputString.length; i++) {
                    if (inputString[i] === ' ') {
                        token_arrary.push(token);
                        token_arrary.push(inputString[i]);
                        token = "";
                    } else {
                        token = token + inputString[i];
                    }
                }
                if (token != "") token_arrary.push(token);
                return token_arrary;
            }

            function combineTokens(inputarray) {
                inputarray.push("");
                let newInputArray = [];
                while (true) {
                    newInputArray = [];
                    let modified = false;
                    for (let i = 0; i < inputarray.length - 1; i++) {
                        let combinedString = inputarray[i] + inputarray[i + 1];

                        let combinedDistance = trie.findClosestMatches(combinedString, 1)[0].distance;
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

            function scoreFunction(string, prevToken_string) {
                let score = 0;
                const currentToken = trie.findClosestMatches(string, 1)[0];
                const current_token_type = currentToken.value[0].type;
                const distance = currentToken.distance;

                if (prevToken_string === null || prevToken_string === undefined) {
                    score = 0;
                } else {
                    const prevToken = trie.findClosestMatches(prevToken_string, 1)[0];
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


            const firstTokenArray = combineTokens(firstTokenizer(inputString));
            const secondTokenArray = secondTokenizer(inputString);

            const first_token_arrary_score = firstTokenArray.reduce((total, element) => total + scoreFunction(element), 0);
            const second_token_arrary_score = secondTokenArray.reduce((total, element) => total + scoreFunction(element), 0);

            return [{ arr: firstTokenArray, score: first_token_arrary_score }, { arr: secondTokenArray, score: second_token_arrary_score }]
        }


        function keyStrokeToString2(slice_dict, trie) {
            let result = [];
            for (let i = 0; i < slice_dict.length; i++) {
                const keyStrokeArray = slice_dict[i].arr;

                let poss = [];
                keyStrokeArray.forEach((element) => {
                    poss.push(trie.findClosestMatches(element, 5))
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
    }

    selectionHandeler(event) {
        event.preventDefault();

        let selectValue = this.selectElement.options[this.selectedIndex].value;
        switch (event.key) {
            case "Tab":
            case "Enter":
                this.textarea.value = this.textarea.value.substring(0, this.cursorStartPosition) + selectValue + this.textarea.value.substring(this.textarea.selectionStart, this.textarea.value.length);
                this.floatingElement.style.display = "none";
                this.buffer = "";
                this.selectedIndex = 0;
                this.selectElement.size = 1;
                this.textarea.focus();
                this.textarea.click();
                this.textarea.setSelectionRange(this.cursorStartPosition + selectValue.length, this.cursorStartPosition + selectValue.length); // bad
                event.stopPropagation();
                this.selectElement.removeEventListener("keydown", this.selectionHandeler);
                return;
                break;
            case "Escape":
                this.floatingElement.style.display = "none";
                this.buffer = "";
                this.selectElement.size = 1;
                this.buffertextarea.focus();
                break;
            case "ArrowUp":
                this.selectedIndex = (this.selectedIndex - 1 + this.selectElement.options.length) % this.selectElement.options.length;
                break;
            case "ArrowDown":
                this.selectedIndex = (this.selectedIndex + 1) % this.selectElement.options.length;
                break;
            default:
                console.log("else part");
                break;  
        }
        this.selectElement.options[this.selectedIndex].selected = true;
        console.log("selectedIndex", this.selectedIndex);
        event.stopPropagation();
    };
}


/**
 * Deprecated
 * @param {*} input_string 
 * @returns 
 */

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


class TypingHandler {
    constructor() {

    }

    handel(event) {

    }
}

