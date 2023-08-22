
let recognition;
let button;
let recording = false;


init();

function init(){
    const SpeechRecognition = window.SpeechRecognitionAlternative|| window.webkitSpeechRecognition;
    const SpeechGrammarList = window.SpeechGrammarList || window.webkitSpeechGrammarList;
    const SpeechRecognitionEvent = window.SpeechRecognitionEvent || window.webkitSpeechRecognitionEvent;

    const recognition = new SpeechRecognition();

    const keywords = [
        '刪除',
        '刪除前一句',
        '清除',
        '停止錄音',

        '逗號',
        '句號',
        '問號',
        '冒號',
        '分號',
        '上引號',
        '下引號',
        '上括號',
        '下括號',
        '驚嘆號',
    ] 
    const grammer = '#JSGF V1.0; grammar keywords; public <keywords> = ' + keywords.join(' | ') + ' ;'


    const grammarList = new SpeechGrammarList();
    grammarList.addFromString(grammer, 1);


    recognition.grammers = grammarList;
    recognition.continuous = true;
    recognition.lang = 'zh-TW';
    recognition.interimResults = true;
    recognition.maxAlternatives = 1;


    button = document.getElementById('record-btn');
    const output = document.getElementById('convertedText');

    let recording = false;
    button.onclick = function(){
        if(!recording){
            recognition.start();
            button.innerHTML = '錄音中...';
            console.log('Ready to receive a command.');
            recording = true;
        }else{
            recognition.stop();
            button.innerHTML = '開始錄音';
            recording = false;
        }
    }

    recognition.onresult = function(event){
        console.log(event.results);

        const last = event.results.length - 1;
        // console.log(event.results[last])
        
        let text = convertKeyWords(event.results[last][0].transcript);
        let color = confidenceToColor(event.results[last][0].confidence);
        let isFinal = event.results[last].isFinal;
        console.log(text, color, isFinal);

        //handle command
        if (text.includes('[停止錄音]') && isFinal) {
            text = text.replace('[停止錄音]', '');
            button.click();
        }else if(text.includes('[刪除]') && isFinal){
            text = text.replace('[刪除]', '');
            text = "";
        }else if(text.includes('[刪除前一句]') && isFinal){ //not working
            text = text.replace('[刪除前一句]', '');
            output.lastElementChild.previousElementSibling.innerHTML = "";
        }else if (text.includes('[清除]') && isFinal) {
            text = text.replace('[清除]', '');
            text = "";
            output.textContent = ""; //clear all child  
            output.appendChild(document.createElement('text'));
        }

        const lastElement = output.lastElementChild;
        while (lastElement && lastElement.nodeType !== 1) {
            lastElement = lastElement.previousElementSibling;
        }
        lastElement.innerHTML = text;
        lastElement.style.color = isFinal? color : '#ff0000';
        
        if (isFinal) {
            output.appendChild(document.createElement('text'));
        }
    }
}

function confidenceToColor(confidence){
    const scale_root = 0.5;
    const scale = (confidence - scale_root) / (1 - scale_root);


    /** From rosszurowski/lerp-color.js
     * A linear interpolator for hexadecimal colors
     * @param {String} a
     * @param {String} b
     * @param {Number} amount
     * @example
     * // returns #7F7F7F
     * lerpColor('#000000', '#ffffff', 0.5)
     * @returns {String}
     */
    function lerpColor(a, b, amount) { 
        var ah = parseInt(a.replace(/#/g, ''), 16),
            ar = ah >> 16, ag = ah >> 8 & 0xff, ab = ah & 0xff,
            bh = parseInt(b.replace(/#/g, ''), 16),
            br = bh >> 16, bg = bh >> 8 & 0xff, bb = bh & 0xff,
            rr = ar + amount * (br - ar),
            rg = ag + amount * (bg - ag),
            rb = ab + amount * (bb - ab);
    
        return '#' + ((1 << 24) + (rr << 16) + (rg << 8) + rb | 0).toString(16).slice(1);
    }
    return lerpColor('#ff0000', '#00ff00', scale);
}


function convertKeyWords(oringalText){
    oringalText = oringalText.replace(/刪除/g, '[刪除]');
    oringalText = oringalText.replace(/刪除前一句/g, '[刪除前一句]');
    oringalText = oringalText.replace(/清除/g, '[清除]');
    oringalText = oringalText.replace(/停止錄音/, '[停止錄音]')
    oringalText = oringalText.replace(/逗號/g, '，');
    oringalText = oringalText.replace(/句號/g, '。');
    oringalText = oringalText.replace(/問號/g, '？');
    oringalText = oringalText.replace(/冒號/g, '：');
    oringalText = oringalText.replace(/分號/g, '；');
    oringalText = oringalText.replace(/上引號/g, '「');
    oringalText = oringalText.replace(/下引號/g, '」');
    oringalText = oringalText.replace(/上括號/g, '（');
    oringalText = oringalText.replace(/下括號/g, '）');
    oringalText = oringalText.replace(/驚嘆號/g, '！');
    return oringalText;
}
