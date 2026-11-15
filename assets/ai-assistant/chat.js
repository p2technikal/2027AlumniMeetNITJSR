const API_URL = "https://nitjsr-reunion-assistant.onrender.com/chat";
const toggleButton = document.getElementById("chat-toggle");
const closeButton = document.getElementById("chat-close");
const chatWindow = document.getElementById("chat-window");
const chatMessages = document.getElementById("chat-messages");
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const suggestionButtons = document.querySelectorAll(
    ".chat-suggestions button"
);

// Open and close chat
function openChat() {
    chatWindow.classList.add("open");
    chatWindow.setAttribute("aria-hidden", "false");
    toggleButton.setAttribute("aria-expanded", "true");
    chatInput.focus();
}

function closeChat() {
    chatWindow.classList.remove("open");
    chatWindow.setAttribute("aria-hidden", "true");
    toggleButton.setAttribute("aria-expanded", "false");
}

toggleButton.addEventListener("click", () => {
    if (chatWindow.classList.contains("open")) {
        closeChat();
    } else {
        openChat();
    }
});

closeButton.addEventListener("click", closeChat);

// Display messages safely
function addMessage(message, type) {
    const messageElement = document.createElement("div");

    messageElement.className =
        type === "user" ? "user-message" : "bot-message";

    messageElement.textContent = message;

    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function sendMessage(question) {
    addMessage(question, "user");

    const loadingMessage = document.createElement("div");
    loadingMessage.className = "bot-message";
    loadingMessage.textContent = "Thinking...";
    chatMessages.appendChild(loadingMessage);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question })
        });

        if (!response.ok) {
            throw new Error("Backend request failed");
        }

        const data = await response.json();
        loadingMessage.textContent = data.answer;
    } catch (error) {
        console.error("Chat error:", error);
        loadingMessage.textContent =
            "Sorry, I'm unable to connect right now. Please try again.";
    }

    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Handle form submission
chatForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const question = chatInput.value.trim();

    if (!question) return;

    sendMessage(question);
    chatInput.value = "";
});

// Handle suggested questions
suggestionButtons.forEach(button => {
    button.addEventListener("click", () => {
        openChat();
        sendMessage(button.dataset.question);
    });
});
