document.addEventListener("DOMContentLoaded", () => {
    const chatForm = document.getElementById("chat-form");
    const userInput = document.getElementById("user-input");
    const chatMessages = document.getElementById("chat-messages");

    chatForm.addEventListener("submit", function (event) {
        event.preventDefault(); // Evita que la página se recargue

        const userMessage = userInput.value.trim();
        if (userMessage === "") {
            return;
        }

        // 1. Muestra el mensaje del usuario en el chat
        addMessage(userMessage, "user-message");
        userInput.value = ""; // Limpia el campo de entrada

        // 2. Muestra un indicador de que el bot está "pensando"
        addMessage("...", "bot-message", true);


        // 3. Envía la pregunta a la API de FastAPI
        fetch("http://127.0.0.1:8000/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ question: userMessage }),
        })
            .then(response => response.json())
            .then(data => {
                removeTypingIndicator();
                addMessage(data.answer, "bot-message");
            })
            .catch(error => {
                removeTypingIndicator();
                addMessage("Lo siento, hubo un error al conectar con la IA.", "bot-message");
                console.error("Error:", error);
            });

    });

    function addMessage(text, className, isTyping = false) {
        const messageDiv = document.createElement("div");
        messageDiv.className = `message ${className}`;
        messageDiv.textContent = text;
        if (isTyping) {
            messageDiv.id = "typing-indicator";
        }
        chatMessages.appendChild(messageDiv);
        // Mueve el scroll hacia el último mensaje
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function removeTypingIndicator() {
        const typingIndicator = document.getElementById("typing-indicator");
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
});