document.addEventListener("DOMContentLoaded", () => {
    const chatForm = document.getElementById("chat-form");
    const userInput = document.getElementById("user-input");
    const chatMessages = document.getElementById("chat-messages");
    let userQuestion = ""; 

    chatForm.addEventListener("submit", function(event) {
        event.preventDefault();

        const userMessage = userInput.value.trim();
        if (userMessage === "") {
            return;
        }

        userQuestion = userMessage;

        addMessage(userMessage, "user-message");
        userInput.value = "";
        addMessage("...", "bot-message", true);

        fetch("https://konrad-api.onrender.com/ask", {
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

        if (className === 'bot-message' && !isTyping) {
            const feedbackContainer = document.createElement("div");
            feedbackContainer.className = "feedback-container";

            const thumbUp = document.createElement("button");
            thumbUp.className = "feedback-button";
            thumbUp.innerHTML = '👍';
            thumbUp.onclick = () => {
                document.querySelectorAll('.feedback-button').forEach(btn => btn.classList.remove('active'));
                thumbUp.classList.add('active');
                sendFeedback("positivo", userQuestion, text);
            };

            const thumbDown = document.createElement("button");
            thumbDown.className = "feedback-button";
            thumbDown.innerHTML = '👎';
            thumbDown.onclick = () => {
                document.querySelectorAll('.feedback-button').forEach(btn => btn.classList.remove('active'));
                thumbDown.classList.add('active');
                sendFeedback("negativo", userQuestion, text);
            };

            feedbackContainer.appendChild(thumbUp);
            feedbackContainer.appendChild(thumbDown);
            messageDiv.appendChild(feedbackContainer);
        }

        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function removeTypingIndicator() {
        const typingIndicator = document.getElementById("typing-indicator");
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    function sendFeedback(feedbackType, question, answer) {
        fetch("https://konrad-api.onrender.com/feedback", { // <-- URL CORREGIDA AQUÍ
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                question: question,
                answer: answer,
                feedback_type: feedbackType
            }),
        })
        .then(response => response.json())
        .then(data => {
            console.log("Feedback enviado:", data);
        })
        .catch(error => {
            console.error("Error al enviar feedback:", error);
        });
    }
});