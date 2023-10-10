document.getElementById('toggleButton').addEventListener('click', function() {
    var button = document.getElementById('toggleButton');
    if (button.innerText === 'Multilingual IME unactivate') {
        button.innerText = 'Multilingual IME activate';
        button.classList.add('activate');
    } else {
        button.innerText = 'Multilingual IME unactivate';
        button.classList.remove('activate');
    }
});