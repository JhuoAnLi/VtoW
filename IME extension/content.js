var SecondPara = document.getElementById("Alh6id");
SecondPara.remove();

document.addEventListener("input", function(event) {
    if (event.target.tagName === "INPUT" || event.target.tagName === "TEXTAREA") {

        var textarea = event.target;
        var existingSelect = textarea.nextElementSibling;
        var selectVisible = false;
        var selectedIndex = 0;

        var test = textarea.value;
        var inputforbackend = "";
        for (var i = test.length - 1; i >= 0; i--) {
            if (test[i] === ' ') {
                break;
            }
            inputforbackend = test[i] + inputforbackend;
        }
        // if (inputforbackend[inputforbackend.length - 1] != '3' && inputforbackend[inputforbackend.length - 1] != '4' && inputforbackend[inputforbackend.length - 1] != '6' && inputforbackend[inputforbackend.length - 1] != '7') { inputforbackend + ' '; }
        console.log(inputforbackend);
        if (textarea.value !== "" && !existingSelect) {
            var select = document.createElement("select");
            var optionValues = ["apple", "banana", "juice", "guava", "tea"];

            optionValues.forEach(function(value) {
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
                } else if (event.key === "Enter" && selectVisible) {
                    var selectedOption = select.options[selectedIndex].value;
                    var currentValue = textarea.value;
                    var lastSpaceIndex = currentValue.lastIndexOf(" ");
                    if (lastSpaceIndex != -1) {
                        var newValue = currentValue.substring(0, lastSpaceIndex + 1) + selectedOption;
                        textarea.value = newValue;
                    } else {
                        textarea.value = selectedOption;
                    }

                    select.style.display = "none";
                    selectVisible = false;
                    textarea.focus();
                    select.options[0].selected = true;
                    document.querySelector('form').addEventListener('submit', function(event) {
                        event.preventDefault();
                    });
                }
            });
        }

        textarea.addEventListener("input", function(event) {
            var inputValue = textarea.value;
            const ee = inputValue;
            console.log("用戶输入的文字:", ee);
        });
    }
});