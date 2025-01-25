const CHAT_API_URL = "/api/intelleva_ai/load_history"; 
const AI_API_URL = "/api/intelleva_ai/chat"; 
const STORE_CHAT_API_URL = "/api/intelleva_ai/save_chat"; 


const chatArea = document.getElementById('chatArea');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
const clearChatButton = document.getElementById('clearChat');


userInput.addEventListener('input', () => {
    sendButton.disabled = !userInput.value.trim();
});


function addMessage(message, type) {
    const messageContainer = document.createElement('div');
    messageContainer.classList.add('flex', 'space-x-4', type === 'user' ? 'justify-end' : 'justify-start');
    
    const messageBubble = document.createElement('div');
    messageBubble.classList.add('flex', 'flex-col', 'max-w-xs');
    messageBubble.innerHTML = `<span class="bg-${type === 'user' ? 'teal-400' : 'black'} text-white p-2 rounded-lg shadow-lg text-sm">${message}</span>`;
    
    messageContainer.appendChild(messageBubble);
    chatArea.appendChild(messageContainer);
    chatArea.scrollTop = chatArea.scrollHeight; // Scroll to the latest message
}


async function loadChatHistory() {
    try {
        console.log("im inside loadchatHistory")
        const response = await fetch(CHAT_API_URL);
        const data = await response.json();

        // Check if there's existing chat data
        if (data && data.chat && data.chat.length > 0) {
            data.chat.forEach(message => {
                console.log(message)
                addMessage(message.text, message.type);
            });
        } else {
            // Welcome message if no chat history
            addMessage("Welcome! How may I assist you today?", "ai");
        }
    } catch (error) {
        console.error("Error fetching chat history:", error);
    }
}


sendButton.addEventListener('click', async () => {
    const userMessage = userInput.value.trim();
    if (userMessage) {
        addMessage(userMessage, 'user');
        userInput.value = '';
        sendButton.disabled = true;

        try {
            // Start AI response and chat storage in parallel
            const [aiResponse, storeResponse] = await Promise.all([
                fetch(AI_API_URL, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: userMessage }),
                }).then(res => res.json()),

                storeChat(userMessage) // Store only the user message initially
            ]);

            if (aiResponse && aiResponse.response) {
                addMessage(aiResponse.response, 'ai');
                await storeChat(null, aiResponse.response);  // Store AI response separately
            }
        } catch (error) {
            console.error("Error communicating with AI API:", error);
        }
    }
});


async function storeChat(userMessage = null, aiMessage = null) {
    if (!userMessage && !aiMessage) return;

    try {
        fetch(STORE_CHAT_API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_message: userMessage, ai_message: aiMessage }),
        });
    } catch (error) {
        console.error("Error storing chat data:", error);
    }
}


async function clearChatHistory() {
    try {
        const response = await fetch('/api/intelleva_ai/clear_history', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        const result = await response.json();

        if (response.ok) {
            console.log("Chat history cleared successfully:", result.message);
        } else {
            console.error("Error clearing chat history:", result.error || result.message);
        }
    } catch (error) {
        console.error("Error connecting to the server:", error);
    }
}


clearChatButton.addEventListener('click', () => {
    chatArea.innerHTML = '';
    addMessage("Welcome! How may I assist you today?", "ai");
    clearChatHistory(); 
});


loadChatHistory();