document.getElementById('toggleButton').addEventListener('click', function() {
    let button = document.getElementById('toggleButton');
    if (button.innerText === 'Deactivate') {
        button.innerText = 'Activate';
        button.classList.add('activate');
        chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
            chrome.tabs.sendMessage(tabs[0].id, { action: 'activate' }, function(response) {

            });
        });
    } else {
        button.innerText = 'Deactivate';
        button.classList.remove('activate');

        chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
            chrome.tabs.sendMessage(tabs[0].id, { action: 'deactivate' }, function(response) {

            });
        });
    }
});