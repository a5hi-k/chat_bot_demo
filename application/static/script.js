function sendMessage(chatArea) {
    const userInput = document.getElementById(`user-input-${chatArea}`);
    const message = userInput.value;
    if (message.trim() !== '') {
        addMessage('user', message, chatArea);
        userInput.value = '';
        
        // Send the message to the Flask backend
        fetch(`/chat${chatArea}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message }),
        })
        .then(response => response.json())
        .then(data => {
            addMessage('bot', data.response, chatArea);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}

// Add icon or symbol based on the message role
// var icon = role === "user" ? "👤" : "🤖";

function addMessage(sender, message, chatArea) {
    const chatBox = document.getElementById(`chat-box-${chatArea}`);
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('chat-message');
    messageDiv.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
    messageDiv.textContent = message;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function clearChat(chatArea) {
    const chatBox = document.getElementById(`chat-box-${chatArea}`);
    chatBox.innerHTML = '';
}