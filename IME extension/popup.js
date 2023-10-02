// Get references to the HTML elements
const inputText = document.getElementById("inputText");
const convertButton = document.getElementById("convertButton");
const outputText = document.getElementById("outputText");

// Add a click event listener to the convert button
convertButton.addEventListener("click", () => {
    // Get the text from the input textarea and convert it to uppercase
    const text = inputText.value;
    const uppercaseText = text.toUpperCase();

    // Display the uppercase text in the output div
    outputText.textContent = uppercaseText;
    console.log(outputText);
});