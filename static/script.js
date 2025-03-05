const apiUrl = '/chat';
const errorDiv = document.getElementById('error');

async function fetchMessages() {
    try {
        const response = await fetch(`${apiUrl}/history`);
        if (!response.ok) {
            throw new Error('Failed to fetch messages');
        }
        const messages = await response.json();
        const messagesDiv = document.getElementById('messages');
        messagesDiv.innerHTML = '';
        messages.forEach(msg => {
            const message = document.createElement('div');
            message.className = 'message';
            message.textContent = `${msg.user}: ${msg.message}`;
            messagesDiv.appendChild(message);
        });
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
        errorDiv.textContent = '';
    } catch (error) {
        errorDiv.textContent = 'Error loading messages. Please try again.';
        console.error('Error:', error);
    }
}

async function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    if (message) {
        try {
            const response = await fetch(`${apiUrl}/message`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message }),
            });
            if (!response.ok) {
                throw new Error('Failed to send message');
            }
            input.value = '';
            await fetchMessages();
            errorDiv.textContent = '';
        } catch (error) {
            errorDiv.textContent = 'Error sending message. Please try again.';
            console.error('Error:', error);
        }
    }
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}


fetchMessages();
