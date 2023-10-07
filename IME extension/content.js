let x = 0;
let y = 0;
document.addEventListener("mousemove", function(event) {
    x = event.clientX;
    y = event.clientY;
});


document.addEventListener("input", function(event) {

    if (event.target.tagName === "INPUT" || event.target.tagName === "TEXTAREA") {

        const inputValue = event.target.value;

        console.log("用戶輸入的文字:", inputValue);
        showMenu(x, y);
    }
});

function showMenu(x, y) {
    const menuUrl = chrome.runtime.getURL("menu.html");


    const activeElement = document.activeElement;


    const menuLeft = x;
    const menuTop = y + 100;


    const popupWindow = window.open(menuUrl, "VerticalMenu", `width=200,height=150,top=${menuTop},left=${menuLeft}`);


    window.addEventListener("keydown", function(event) {
        if (event.key === "Enter") {

            popupWindow.close();

            activeElement.focus();
        }
    });
}