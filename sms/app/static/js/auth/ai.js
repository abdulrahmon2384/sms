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
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    messageContainer.innerHTML = `
        <div class="flex gap-4 ${type === 'user' ? 'flex-row-reverse' : ''}">
            ${type !== 'user' ? `
                <div class="shrink-0 h-8 w-8 bg-teal-400 rounded-full flex items-center justify-center">
                    <i data-lucide="bot" class="h-5 w-5 text-white"></i>
                </div>
            ` : ''}
            
            <div class="flex flex-col ${type === 'user' ? 'items-end' : 'items-start'} max-w-[80%]">
                <div class="${type === 'user' ? 'bg-teal-400 text-white' : 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white'} px-4 py-3 rounded-xl shadow-sm transition-all duration-200">
                    ${message}
                    <div class="mt-1 text-xs ${type === 'user' ? 'text-teal-100' : 'text-gray-500 dark:text-gray-400'}">${time}</div>
                </div>
            </div>

            ${type === 'user' ? `
                <div class="shrink-0 h-8 w-8 bg-gray-600 rounded-full flex items-center justify-center">
                    <i data-lucide="user" class="h-5 w-5 text-white"></i>
                </div>
            ` : ''}
        </div>
    `;

    chatArea.appendChild(messageContainer);
    
    // Auto-scroll to bottom
    const scrollToBottom = () => {
        chatArea.scrollTop = chatArea.scrollHeight;
        messageContainer.scrollIntoView({ behavior: 'smooth' });
    };
    
    // Use requestAnimationFrame for smooth scroll
    requestAnimationFrame(scrollToBottom);
    
    // Refresh Lucide icons
    if (window.lucide) {
        lucide.createIcons();
    }
}


async function loadChatHistory() {
    try {
        const response = await fetch(CHAT_API_URL);
        const data = await response.json();

        // Check if there's existing chat data
        if (data.chat && data.chat.length > 0) {
            data.chat.forEach(message => {
                addMessage(message.message, message.type);
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

                // storeChat(userMessage) // Store only the user message initially
            ]);

            if (aiResponse && aiResponse.response) {
                addMessage(aiResponse.response, 'ai');
                await storeChat(userMessage, aiResponse.response);  // Store AI response separately
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