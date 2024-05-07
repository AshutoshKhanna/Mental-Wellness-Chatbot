const userInput = document.getElementById('user-input');
const sendIcon = document.getElementById('send-icon');
const microphoneIcon = document.getElementById('microphone-icon');
const chatBox = document.getElementById('chat-box');
const clearChatBtn = document.getElementById('clear-chat-icon');
const readAloudIcon = document.getElementById('read-aloud-icon');
let isVoiceInput = false;
let recognition;
let currentUtterance = null;

microphoneIcon.addEventListener('click', toggleVoiceInput);
sendIcon.addEventListener('click', sendMessage);  // Update this line
userInput.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

function toggleVoiceInput() {
    isVoiceInput = !isVoiceInput;
    userInput.style.display = isVoiceInput ? 'none' : 'block';

    if (isVoiceInput) {
        startVoiceRecognition();
        microphoneIcon.src = "static/microphone-on.svg";
    } else {
        stopVoiceRecognition();
        microphoneIcon.src = "static/microphone-off.svg";
    }
}



function startVoiceRecognition() {
    recognition = new window.webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    
    recognition.onstart = () => {
        console.log('Voice recognition started');
    };

    recognition.onresult = (event) => {
        const transcript = event.results[event.results.length - 1][0].transcript;
        userInput.value = transcript;
    };
    
    recognition.onerror = (event) => {
        console.error('Voice recognition error:', event.error);
    };
    
    recognition.onend = () => {
        console.log('Voice recognition ended');
    };
    
    recognition.start();
}

function stopVoiceRecognition() {
    if (recognition) {
        recognition.stop();
        recognition = null;
    }
}

function sendMessage() {
    const userMessage = isVoiceInput ? userInput.value : userInput.value.trim();
    if (userMessage !== '') {
        appendUserMessage(userMessage);
        userInput.value = '';

        fetch('/get_response', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: userMessage })
        })
        .then(response => response.json())
        .then(data => {
            const assistantResponse = data.response;
            appendBotMessage(assistantResponse);
        });
    }
}

function appendUserMessage(message) {
    const userMessageDiv = document.createElement('div');
    userMessageDiv.classList.add('message', 'user-message');
    userMessageDiv.textContent = message;

    const userBox = document.createElement('div');
    userBox.classList.add('message-box', 'user-box');

    const userImage = document.createElement('img');
    userImage.src = 'static/user-image.png'; // Update with the correct path for user image
    userImage.classList.add('message-image', 'user-image');
    userBox.appendChild(userImage);

    userBox.appendChild(userMessageDiv);

    chatBox.appendChild(userBox);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function appendBotMessage(message) {
    const botBox = document.createElement('div');
    botBox.classList.add('message-box', 'bot-box');

    const botImage = document.createElement('img');
    botImage.src = 'static/bot-image.png'; // Update with the correct path for bot image
    botImage.classList.add('message-image', 'bot-image');
    botBox.appendChild(botImage);

    const botMessageDiv = document.createElement('div');
    botMessageDiv.classList.add('message', 'bot-message');
    botMessageDiv.textContent = message;

    const readAloudIcon = document.createElement('img');
    readAloudIcon.classList.add('read-aloud-icon');
    readAloudIcon.src = "static/start-reading.svg"; // Start reading SVG
    readAloudIcon.alt = "Read Aloud Icon";
    readAloudIcon.dataset.state = 'start';
    readAloudIcon.addEventListener('click', toggleReadAloud);

    botBox.appendChild(botMessageDiv);
    botBox.appendChild(readAloudIcon);

    chatBox.appendChild(botBox);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function toggleReadAloud() {
    const readAloudIcon = this;
    const botMessageDiv = this.previousElementSibling;

    if (readAloudIcon.dataset.state === 'start') {
        readAloudIcon.src = "static/stop-reading.svg"; // Stop reading SVG
        readAloudIcon.dataset.state = 'stop';

        currentUtterance = readMessageAloud(botMessageDiv.textContent);
    } else {
        readAloudIcon.src = "static/start-reading.svg"; // Start reading SVG
        readAloudIcon.dataset.state = 'start';

        if (currentUtterance) {
            speechSynthesis.cancel();
            currentUtterance = null;
        }
    }
}

function readMessageAloud(message) {
    const utterance = new SpeechSynthesisUtterance(message);
    speechSynthesis.speak(utterance);
    return utterance;
}


clearChatBtn.addEventListener('click', clearChat);
function clearChat() {
    chatBox.innerHTML = '';
}