// // popup.js

// document.addEventListener("DOMContentLoaded", function() {
//     const menuContainer = document.getElementById("menu-container");


//     menuContainer.addEventListener("click", function(event) {
//         if (event.target.classList.contains("menu-item")) {
//             const selectedText = event.target.innerText;
//             chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
//                 const activeTab = tabs[0];
//                 chrome.scripting.executeScript({
//                     target: { tabId: activeTab.id },
//                     function: function(selectedText) {

//                         const inputElement = document.activeElement;
//                         if (inputElement) {
//                             const startPosition = inputElement.selectionStart;
//                             const endPosition = inputElement.selectionEnd;
//                             const currentValue = inputElement.value;
//                             const newValue = currentValue.substring(0, startPosition) +
//                                 selectedText +
//                                 currentValue.substring(endPosition);
//                             inputElement.value = newValue;
//                         }
//                     },
//                     args: [selectedText]
//                 });
//             });
//         }
//     });
// });