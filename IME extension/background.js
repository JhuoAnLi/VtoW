chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    console.log("Message received:", message);

    if (message.action === "convertToUppercase") {
        const convertedText = message.text.toUpperCase();
        sendResponse({ result: convertedText });

        console.log("Received a message from content script or popup:", message.text);
    }
});