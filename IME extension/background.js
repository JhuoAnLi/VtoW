// background.js

let isPopupOpen = false;

// 监听来自content script的消息
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.action === "showPopup" && !isPopupOpen) {
        // 显示popup.html
        chrome.windows.create({
            url: "popup.html",
            type: "popup",
            width: 220,
            height: 340
        }, function(window) {
            isPopupOpen = true;
        });
    } else if (message.action === "hidePopup" && isPopupOpen) {
        // 隐藏popup.html
        chrome.windows.getAll(function(windows) {
            for (let i = 0; i < windows.length; i++) {
                if (windows[i].type === "popup") {
                    chrome.windows.remove(windows[i].id);
                    isPopupOpen = false;
                    break;
                }
            }
        });
    }
});