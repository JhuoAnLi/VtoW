var SecondPara = document.getElementById("Alh6id");
SecondPara.remove();
var buffer = "";
var buffer2 = "";
var backendoutputarray = [];
document.addEventListener("keydown", function(event) {
    if (event.key === "Backspace") { // solve the problem of backspace XD
        buffer = buffer.substring(0, buffer.length - 1);

    } else if (/^[a-zA-Z0-9 ]$/.test(event.key)) {
        buffer = buffer + event.key;
        var inputforbackend = "";
        var inputarray = [];
        for (var i = 0; i < buffer.length; i++) {
            if (buffer[i] === ' ' || buffer[i] === '3' || buffer[i] === '4' || buffer[i] === '6' || buffer[i] === '7') {
                inputforbackend = inputforbackend + buffer[i];
                inputarray.push(inputforbackend);
                inputforbackend = "";
            } else {
                inputforbackend = inputforbackend + buffer[i];
            }
        }
        if (inputforbackend != "") inputarray.push(inputforbackend);
    }
    //backendoutputarray[]=function(inputarray); here is the function to get the output from backend
    ////['su3','cl3', ' ', 'i ', 'have ', 'a ', 'dog'] =>
    //['你好 我有一隻狗','擬好 我有一隻狗','擬郝 我有一隻狗']
    console.log(inputarray);
});
document.addEventListener("input", function(event) {
    if (event.target.tagName === "INPUT" || event.target.tagName === "TEXTAREA") {

        var textarea = event.target;
        var existingSelect = textarea.nextElementSibling;
        var selectVisible = false;
        var selectedIndex = 0;
        if (textarea.value !== "" && !existingSelect) {
            var select = document.createElement("select");
            backendoutputarray = ["你好 我有一隻狗", "擬好 我有一隻狗", "擬郝 我有一隻狗"];
            backendoutputarray.forEach(function(value) {
                var option = document.createElement("option");
                option.value = value;
                option.textContent = value;
                select.appendChild(option);
            });

            select.style.display = "none";

            textarea.parentNode.appendChild(select);

            textarea.addEventListener("keydown", function(event) {

                if (event.key === "ArrowDown") {
                    if (!selectVisible) {
                        selectedIndex = 0;
                        console.log(selectedIndex, selectVisible, event.key);
                        select.style.display = "block";
                        selectVisible = true;
                        event.preventDefault();
                    } else if (selectVisible && selectedIndex < select.options.length - 1) {
                        selectedIndex++;
                        select.options[selectedIndex].selected = true;
                        console.log(selectedIndex, selectVisible, event.key);
                        event.preventDefault();
                    }
                } else if (event.key === "ArrowUp") {
                    if (selectVisible) {

                        if (selectedIndex > 0) {
                            selectedIndex--;
                            select.options[selectedIndex].selected = true;
                            console.log(selectedIndex, selectVisible, event.key);
                        }
                    }
                    event.preventDefault();
                } else if (event.key === "ArrowDown") {
                    if (selectVisible) {

                        if (selectedIndex < select.options.length - 1) {
                            selectedIndex++;
                            select.options[selectedIndex].selected = true;
                            console.log(selectedIndex, selectVisible, event.key);
                        }
                    }
                    event.preventDefault();
                }
                if (event.key === "ArrowRight" && selectVisible) { //rightkey
                    var selectedOption = select.options[selectedIndex].value;
                    buffer2 = buffer2 + selectedOption;
                    setTimeout(() => {
                        textarea.value = buffer2;
                    }, 0);
                    buffer = "";
                    select.style.display = "none";
                    selectVisible = false;
                    textarea.focus();
                    select.options[0].selected = true;
                }

            });
        }
        textarea.addEventListener("input", function(event) {
            var inputValue = textarea.value;
            const ee = inputValue;
            console.log("输入的文字:", ee);
        });
    }
});