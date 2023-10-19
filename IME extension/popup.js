document.getElementById('toggleButton').addEventListener('click', function() {
    let button = document.getElementById('toggleButton');
    if (button.innerText === 'Unactivate Multilingual IME') {
        button.innerText = 'Activate Multilingual IME';
        button.classList.add('activate');
        console.log('Message sent from popup.js: fdjaiofjdoiasp');

        chrome.runtime.sendMessage({ action: 'activate' });
    } else {
        button.innerText = 'Unactivate Multilingual IME';
        button.classList.remove('activate');

        chrome.runtime.sendMessage({ action: 'deactivate' });
    }
});

