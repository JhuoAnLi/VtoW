let x = 0;
let y = 0;
document.addEventListener("mousemove", function(event) {
    x = event.clientX;
    y = event.clientY;
});


document.addEventListener("input", function(event) {
    if (event.target.tagName === "INPUT" || event.target.tagName === "TEXTAREA") {

        var textarea = event.target;
        var existingSelect = textarea.nextElementSibling;

        if (textarea.value !== "" && !existingSelect) {
            var select = document.createElement("select");
            select.innerHTML = `
                <option value="apple">apple</option>
                <option value="banana">banana</option>
                <option value="juice">juice</option>
                <option value="guava">guava</option>
            `;
            select.addEventListener("change", function(event) {
                var selectedOption = event.target.value;
                var currentValue = textarea.value;

                var lastSpaceIndex = currentValue.lastIndexOf(" ");

                if (lastSpaceIndex !== -1) {
                    var newValue = currentValue.substring(0, lastSpaceIndex + 1) + selectedOption;
                    textarea.value = newValue;
                } else {
                    textarea.value = selectedOption;
                }
            });

            textarea.parentNode.appendChild(select);
        }
        textarea.addEventListener("input", function(event) {
            var inputValue = textarea.value;
            const ee = inputValue;
            console.log("用戶輸入的文字:", ee);

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