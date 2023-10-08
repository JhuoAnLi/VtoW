let x = 0;
let y = 0;
document.addEventListener("mousemove", function(event) {
    x = event.clientX;
    y = event.clientY;
});


document.addEventListener("input", function(event) {

    if (event.target.tagName === "INPUT" || event.target.tagName === "TEXTAREA") {

        var textarea = event.target;
        // console.log(event.target);
        textarea.addEventListener("input", function(event) {
            var inputValue = textarea.value;
            let container = document.createElement("div");

            container.innerHTML = `
              <select id="mySelect">
                <option value="option1">apple</option>
                <option value="option2">banana</option>
                <option value="option3">juice</option>
              </select>
            `;

            container.addEventListener("change", function(event) {
                textarea.value = event.target.value;

            });
            textarea.appendChild(container);
            const ee = event.target.value;
            console.log("用戶輸入的文字:", ee);
            // showMenu(x, y);
        });

    }
});

function showMenu(x, y) {
    const menuUrl = chrome.runtime.getURL("popup.html");


    const activeElement = document.activeElement;


    const menuLeft = x - 500;
    const menuTop = y + 100;


    const popupWindow = window.open(menuUrl, "VerticalMenu", `width=200,height=150,top=${menuTop},left=${menuLeft}`);


    window.addEventListener("keydown", function(event) {
        if (event.key === "Enter") {

            popupWindow.close();

            activeElement.focus();
        }
    });
}
// content.js

// document.addEventListener("input", function(event) {
//     if (event.target.tagName === "INPUT" || event.target.tagName === "TEXTAREA") {
//         // 向 background script 发送消息以显示 popup.html
//         chrome.runtime.sendMessage({ action: "showPopup" });
//     }
// });