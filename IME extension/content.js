// This function converts all text nodes within an element to uppercase
function convertTextToUppercase(element) {
    if (element.nodeType === Node.TEXT_NODE) {
        element.textContent = element.textContent.toUpperCase();
    } else if (element.nodeType === Node.ELEMENT_NODE) {
        for (const childNode of element.childNodes) {
            convertTextToUppercase(childNode);
        }
    }
}

// Call the conversion function when the page is fully loaded
document.addEventListener("DOMContentLoaded", function() {
    convertTextToUppercase(document.body);
});