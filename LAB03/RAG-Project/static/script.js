document.addEventListener("DOMContentLoaded", () => {
    const inputForm = document.getElementById("inputForm");
    const queryInput = document.getElementById("queryInput");
    const chatFeed = document.getElementById("chatFeed");
    const sendBtn = document.getElementById("sendBtn");
    const clearBtn = document.getElementById("clearBtn");
    const typingIndicator = document.getElementById("typingIndicator");
    const sourcesList = document.getElementById("sourcesList");
    const noSourcesMsg = document.querySelector(".no-sources-msg");

    // Auto-scroll chat feed to the bottom
    function scrollToBottom() {
        chatFeed.scrollTop = chatFeed.scrollHeight;
    }

    // Helper to format time
    function getFormattedTime() {
        const now = new Date();
        return now.toLocaleTimeString("th-TH", { hour: "2-digit", minute: "2-digit" });
    }

    // Add a chat bubble to the feed
    function appendMessage(text, isUser = false) {
        const messageDiv = document.createElement("div");
        messageDiv.className = `message ${isUser ? "user-message" : "bot-message"} fade-in`;
        
        const bubble = document.createElement("div");
        bubble.className = "msg-bubble";
        bubble.textContent = text;
        
        const timeSpan = document.createElement("span");
        timeSpan.className = "msg-time";
        timeSpan.textContent = getFormattedTime();

        messageDiv.appendChild(bubble);
        messageDiv.appendChild(timeSpan);
        chatFeed.appendChild(messageDiv);
        scrollToBottom();
    }

    // Helper to determine score color class
    function getScoreClass(score) {
        if (score >= 0.85) return "score-high";
        if (score >= 0.70) return "score-med";
        return "score-low";
    }

    // Update the sidebar with retrieved source documents
    function updateSources(results) {
        sourcesList.innerHTML = "";
        
        if (!results || results.length === 0) {
            noSourcesMsg.classList.remove("hidden");
            return;
        }

        noSourcesMsg.classList.add("hidden");

        results.forEach((item, index) => {
            const card = document.createElement("div");
            card.className = "source-card";
            
            const scoreClass = getScoreClass(item.score);
            
            card.innerHTML = `
                <div class="source-card-header">
                    <span class="category-tag">${item.category || "ความรู้ทั่วไป"}</span>
                    <span class="score-badge ${scoreClass}">Sim: ${item.score.toFixed(4)}</span>
                </div>
                <div class="source-question">Q: ${item.question}</div>
                <div class="source-snippet">${item.answer}</div>
                <div class="source-footer">
                    <span>Rank #${index + 1}</span>
                    <span>Line ${item.line_no}</span>
                </div>
            `;
            sourcesList.appendChild(card);
        });
    }

    // Handle form submission
    inputForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        const query = queryInput.value.trim();
        if (!query) return;

        // Display user message
        appendMessage(query, true);
        queryInput.value = "";
        
        // Show typing indicator
        typingIndicator.classList.remove("hidden");
        scrollToBottom();
        
        // Disable input during request
        queryInput.disabled = true;
        sendBtn.disabled = true;

        try {
            const response = await fetch("/api/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ query: query })
            });

            if (!response.ok) {
                throw new Error("เกิดข้อผิดพลาดในการเชื่อมต่อเซิร์ฟเวอร์");
            }

            const data = await response.json();
            
            // Hide typing indicator
            typingIndicator.classList.add("hidden");

            if (data.results && data.results.length > 0) {
                // Return top result answer as primary bot message
                const bestResult = data.results[0];
                appendMessage(bestResult.answer);
                
                // Update sources sidebar with all results
                updateSources(data.results);
            } else {
                appendMessage("ขออภัยด้วยครับ บอยังไม่พบข้อมูลที่เกี่ยวข้องในระบบความรู้เลยครับ 😅");
                updateSources([]);
            }

        } catch (error) {
            console.error(error);
            typingIndicator.classList.add("hidden");
            appendMessage(`เกิดข้อผิดพลาด: ${error.message} กรุณาลองใหม่อีกครั้งนะครับ 🛑`);
        } finally {
            // Re-enable inputs
            queryInput.disabled = false;
            sendBtn.disabled = false;
            queryInput.focus();
            scrollToBottom();
        }
    });

    // Handle clear chat button
    clearBtn.addEventListener("click", () => {
        chatFeed.innerHTML = `
            <div class="message bot-message fade-in">
                <div class="msg-bubble">
                    ล้างการคุยเรียบร้อยแล้วครับ! 🎸 ถามคำถามเกี่ยวกับคอร์ดกีตาร์ ทฤษฎีดนตรี หรือเพลงใหม่ได้เลยครับ
                </div>
                <span class="msg-time">${getFormattedTime()}</span>
            </div>
        `;
        sourcesList.innerHTML = "";
        noSourcesMsg.classList.remove("hidden");
    });
});
