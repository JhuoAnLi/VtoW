// background.js

// 在瀏覽器啟動時執行的程式碼
chrome.runtime.onStartup.addListener(function() {
    // 在這裡添加啟動時的任務
    console.log("onStartup");
});