
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
            button.innerHTML = '按下開始錄音';
            recording = false;
        }
    }

    recognition.onresult = function(event){
        console.log(event.results);

        let text = '';
        const lines = [];
        for(let i = 0; i < event.results.length; i++){
            // console.log(event.results[i][0].transcript);
            lines.push(
                {
                    text: convertKeyWords(event.results[i][0].transcript), 
                    color: confidenceToColor(event.results[i][0].confidence),
                    isFinal: event.results[i].isFinal
                });
        }

        for (let i = 0; i < lines.length; i++) {
            if (lines[i].text.includes('[停止錄音]') && lines[i].isFinal) {
                lines[i].text = lines[i].text.replace('[停止錄音]', '');
                button.click();
            }else if(lines[i].text.includes('[刪除]') && lines[i].isFinal){
                lines[i].text = lines[i].text.replace('[刪除]', '');
                lines[i].text = "";
            }
        }

        for (let i = 0; i < lines.length; i++) {
            text += `<text style="color: ${lines[i].color}">${lines[i].text}</text>`
        }
        output.innerHTML = text;
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
