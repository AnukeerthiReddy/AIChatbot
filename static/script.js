// Chat functionality
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const clearBtn = document.getElementById('clear-btn');
const historyBtn = document.getElementById('history-btn');

// Add message to chat
function addMessage(role, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}-message`;
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.innerHTML = `<strong>${role === 'user' ? 'You' : 'Bot'}:</strong> ${content}`;
    
    messageDiv.appendChild(messageContent);
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Show typing indicator
function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message';
    typingDiv.id = 'typing-indicator';
    typingDiv.innerHTML = `
        <div class="message-content">
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Remove typing indicator
function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// Send message to server
async function sendMessage() {
    const message = userInput.value.trim();
    
    if (!message) {
        return;
    }
    
    // Add user message to chat
    addMessage('user', message);
    userInput.value = '';
    
    // Disable input while processing
    sendBtn.disabled = true;
    userInput.disabled = true;
    
    // Show typing indicator
    showTypingIndicator();
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message }),
        });
        
        const data = await response.json();
        
        // Remove typing indicator
        removeTypingIndicator();
        
        if (data.status === 'success') {
            addMessage('bot', data.response);
        } else {
            addMessage('bot', 'Sorry, I encountered an error. Please try again.');
        }
    } catch (error) {
        removeTypingIndicator();
        addMessage('bot', 'Sorry, I couldn\'t connect to the server. Please try again.');
        console.error('Error:', error);
    } finally {
        // Re-enable input
        sendBtn.disabled = false;
        userInput.disabled = false;
        userInput.focus();
    }
}

// Clear conversation
async function clearConversation() {
    if (!confirm('Are you sure you want to clear the conversation history?')) {
        return;
    }
    
    try {
        const response = await fetch('/clear', {
            method: 'POST',
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            // Clear chat display
            chatMessages.innerHTML = `
                <div class="message bot-message">
                    <div class="message-content">
                        <strong>Bot:</strong> Conversation history cleared. How can I help you?
                    </div>
                </div>
            `;
        }
    } catch (error) {
        alert('Error clearing conversation. Please try again.');
        console.error('Error:', error);
    }
}

// View history
async function viewHistory() {
    try {
        const response = await fetch('/history');
        const data = await response.json();
        
        if (data.status === 'success' && data.history.length > 0) {
            let historyText = 'Conversation History:\n\n';
            data.history.forEach(msg => {
                const role = msg.role === 'user' ? 'You' : 'Bot';
                historyText += `${role}: ${msg.content}\n\n`;
            });
            alert(historyText);
        } else {
            alert('No conversation history yet.');
        }
    } catch (error) {
        alert('Error loading history. Please try again.');
        console.error('Error:', error);
    }
}

// Event listeners
sendBtn.addEventListener('click', sendMessage);
clearBtn.addEventListener('click', clearConversation);
historyBtn.addEventListener('click', viewHistory);

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Focus on input when page loads
userInput.focus();
