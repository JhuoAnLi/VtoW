document.addEventListener('DOMContentLoaded', function () {
    const myTextArea = document.getElementById("my-textarea");
    const exampleSentence = document.getElementById("example-sentence");
    const startBtn = document.getElementById("start-btn");
    const resetBtn = document.getElementById("reset-btn");
    const nextBtn = document.getElementById("next-btn");
    const time_spend = document.getElementById("time-spend");
    const timer = document.getElementById("timer");
    const wpm = document.getElementById("wpm");
    const keystroke_count = document.getElementById("keystroke-count");
    const backspace_count = document.getElementById("backspace-count");
    const shift_count = document.getElementById("shift-count");
    const key_pressed = document.getElementById("key-pressed");


    const sentences = ["中文", "abc"];
    let currentSentence = 0; 
    let startTime;
    let endTime;
    let keystrokeCounter = 0;
    let backspaceCounter = 0;
    let shiftCounter = 0;
    let timerInterval;


    function resetAll(){
        currentSentence = 0;
        keystrokeCounter = 0;
        backspaceCounter = 0;
        shiftCounter = 0;
        time_spend.textContent = "";
        key_pressed.textContent = "";
        keystroke_count.textContent = "";
        backspace_count.textContent = "";
        exampleSentence.textContent = "";
        shift_count.textContent = "";
        timer.textContent = "";
        myTextArea.value = "";
        clearInterval(timerInterval);
    }

    function showKeyStroke(keystroke) {
        const keyStrokeElement = document.createElement("div");
        keyStrokeElement.classList.add("disappearing-element");
        keyStrokeElement.textContent = keystroke;
        key_pressed.insertBefore(keyStrokeElement, key_pressed.firstChild);
    }

    startBtn.addEventListener("click", function () {
        resetAll();
        startTime = new Date().getTime();
        timerInterval = setInterval(()=>{timer.textContent = `${(new Date().getTime() - startTime)/1000} seconds`;}, 1);

        startBtn.disabled = true;
        exampleSentence.textContent = sentences[currentSentence];
        myTextArea.focus();
    });

    resetBtn.addEventListener("click", function () {
        resetAll();
    });


    let clear = false;
    myTextArea.addEventListener('keydown', function (event) {
        if (clear) {
            myTextArea.value = "";
            clear = false;
        }

        if (event.code === "Enter") {
            checkCorrect();
            event.preventDefault();
        } else if (event.code === "Backspace") {
            backspaceCounter++;
        }else if (event.code === "ShiftLeft" || event.code === "ShiftRight") {
            shiftCounter++;
        }
        
        keystrokeCounter++;
        const keystroke = codeToEnglish(event.code);
        showKeyStroke(keystroke);
        updateResult();

        function checkCorrect(){
            if (clear) {
                myTextArea.value = "";
                clear = false;
            }
    
            if (myTextArea.value == sentences[currentSentence]) {
                updateSentence();
            }
    
            function updateSentence() {
                if (currentSentence === sentences.length - 1) {
                    clearInterval(timerInterval);
                    exampleSentence.textContent = "You have finished all the sentences! Click the reset button to start again.";
                    startBtn.disabled = false;
                    myTextArea.value = "";
                    updateResult();
                    clear = true;
                    return;
                } else {
                    currentSentence++;
                    exampleSentence.textContent = sentences[currentSentence];
                    myTextArea.value = "";
                }
            }
    
            function updateResult(){
                keystroke_count.textContent = keystrokeCounter;
                backspace_count.textContent = backspaceCounter;
    
                endTime = new Date().getTime();
                time_spend.textContent = `${(endTime - startTime)/1000} seconds`;

            }
        }
    });

    function updateResult(){
        keystroke_count.textContent = keystrokeCounter;
        backspace_count.textContent = backspaceCounter;
        shift_count.textContent = shiftCounter;
    }

    function codeToEnglish(code) {
        console.log(code);
        const specialKeyMap = {
            "Backspace": "[Backspace]",
            "Tab": "[Tab]",
            "Enter": "[Enter]",
            "ShiftLeft": "[Shift]",
            "ShiftRight": "[Shift]",
            "ControlLeft": "[Control]",
            "ControlRight": "[Control]",
            "AltLeft": "[Alt]",
            "AltRight": "[Alt]",
            "Pause": "[Pause]",
            "CapsLock": "[Caps Lock]",
            "Escape": "[Escape]",
            "Space": "[Space]",
            "PageUp": "[Page Up]",
            "PageDown": "[Page Down]",
            "End": "[End]",
            "Home": "[Home]",
            "ArrowLeft": "[Arrow Left]",
            "ArrowUp": "[Arrow Up]",
            "ArrowRight": "[Arrow Right]",
            "ArrowDown": "[Arrow Down]",
            "Insert": "[Insert]",
            "Delete": "[Delete]",
            "OSLeft": "[Left Win]",
            "OSRight": "[Right Win]",
            "ContextMenu": "[Context Menu]",
            "NumpadMultiply": "[Num *]",
            "NumpadAdd": "[Num +]",
            "NumpadSubtract": "[Num -]",
            "NumpadDecimal": "[Num .]",
            "NumpadDivide": "[Num /]",
            "NumLock": "[Num Lock]",
            "ScrollLock": "[Scroll Lock]",
            "Semicolon": "[;]",
            "Equal": "[=]",
            "Comma": "[,]",
            "Minus": "[-]",
            "Period": "[.]",
            "Slash": "[/]",
            "Backquote": "[`]",
            "BracketLeft": "[[",
            "Backslash": "[\\]",
            "BracketRight": "[]]",
            "Quote": "[']",
            // Add more special keys as needed
        };

        if (specialKeyMap[code]) {
            return specialKeyMap[code];
        } else if (/^Digit\d$/.test(code)) {
            return code.slice(-1); // Extract the digit from "DigitX" format
        } else if (/^Key[a-zA-Z]$/.test(code)) {
            return code.slice(-1).toLowerCase(); // Extract the letter and convert to lowercase
        }

        return '[Unknown]';
    }
});
