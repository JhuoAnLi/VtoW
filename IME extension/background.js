// This is a background script for your Chrome extension
// You can add background-specific logic here if needed

// Example: Listening for a message from a content script
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.action === "convertToUppercase") {
        // You can add background logic here if needed
        // For now, let's just log the message
        console.log("Received a message from content script:", message.text);
    }
});