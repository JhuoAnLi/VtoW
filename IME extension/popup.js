document.addEventListener("DOMContentLoaded", function() {
    const inputText = document.getElementById("inputText");
    const convertButton = document.getElementById("convertButton");
    const outputText = document.getElementById("outputText");


    convertButton.addEventListener("click", function() {
        const text = inputText.value;

        const convertedText = text.toUpperCase();

        outputText.textContent = convertedText;
    });
});