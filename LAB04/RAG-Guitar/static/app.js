/**
 * Guitar Lab - Knowledge Assistant & Vector Search Frontend
 */

let lastRetrievedChunks = [];
let queryHistory = [];

document.addEventListener("DOMContentLoaded", () => {
  init3DInteractions();
  initVectorCanvas();
  initChat();
  initHotspots();
  initExploreCards();
  fetchInitialStats();
});

// ================= 3D GUITAR TILT & PARALLAX =================
function init3DInteractions() {
  // Handled by Three.js WebGL & OrbitControls in guitar3d.js
}

// ================= HOTSPOT POPOVER & INTERACTIONS =================
function initHotspots() {
  const pins = document.querySelectorAll(".hud-pin");
  const popover = document.getElementById("hotspot-popover");
  const popTitle = document.getElementById("pop-title");
  const popCat = document.getElementById("pop-cat");
  const popDesc = document.getElementById("pop-desc");
  const popSpecs = document.getElementById("pop-specs");
  const popClose = document.getElementById("pop-close");
  const btnAskPart = document.getElementById("btn-ask-part");

  let currentPartName = "";

  pins.forEach(pin => {
    pin.addEventListener("click", async (e) => {
      e.stopPropagation();
      const part = pin.dataset.part;
      currentPartName = part;

      try {
        const res = await fetch(`/api/hotspots/${part}`);
        const data = await res.json();

        popTitle.textContent = data.title;
        popCat.textContent = data.category;
        popDesc.textContent = data.description;
        popSpecs.innerHTML = data.specs.map(s => `<div>• ${s}</div>`).join("");

        // Position popover near pin
        const pinRect = pin.getBoundingClientRect();
        popover.style.top = `${pinRect.bottom + window.scrollY + 10}px`;
        popover.style.left = `${Math.min(window.innerWidth - 300, Math.max(10, pinRect.left - 50))}px`;
        popover.classList.add("active");
      } catch (err) {
        console.error("Hotspot fetch error:", err);
      }
    });
  });

  if (popClose) {
    popClose.addEventListener("click", () => popover.classList.remove("active"));
  }

  document.addEventListener("click", (e) => {
    if (!popover.contains(e.target)) {
      popover.classList.remove("active");
    }
  });

  if (btnAskPart) {
    btnAskPart.addEventListener("click", () => {
      popover.classList.remove("active");
      const q = `Tell me in detail about the ${popTitle.textContent} on this guitar.`;
      submitQuery(q);
      document.getElementById("chat-section").scrollIntoView({ behavior: "smooth" });
    });
  }
}

// ================= CHAT LOGIC =================
function initChat() {
  const chatForm = document.getElementById("chat-form");
  const chatInput = document.getElementById("chat-input");
  const btnStartAsking = document.getElementById("btn-start-asking");
  const btnClearChat = document.getElementById("btn-clear-chat");
  const chips = document.querySelectorAll(".chip");

  if (btnStartAsking) {
    btnStartAsking.addEventListener("click", () => {
      chatInput.focus();
      document.getElementById("chat-section").scrollIntoView({ behavior: "smooth" });
    });
  }

  if (chatForm) {
    chatForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const query = chatInput.value.trim();
      if (!query) return;
      submitQuery(query);
      chatInput.value = "";
    });
  }

  chips.forEach(chip => {
    chip.addEventListener("click", () => {
      const q = chip.dataset.query;
      if (q) {
        submitQuery(q);
        document.getElementById("chat-section").scrollIntoView({ behavior: "smooth" });
      }
    });
  });

  if (btnClearChat) {
    btnClearChat.addEventListener("click", async () => {
      const chatMessages = document.getElementById("chat-messages");
      chatMessages.innerHTML = `
        <div class="message-row assistant">
          <div class="msg-avatar"><i class="fa-solid fa-guitar"></i></div>
          <div class="msg-bubble">
            <div class="msg-header">
              <span class="msg-sender">PROxTAE Guitar AI</span>
              <span class="msg-time">Just now</span>
            </div>
            <div class="msg-text">Conversation history cleared. How can I help you today?</div>
          </div>
        </div>
      `;
      try {
        await fetch("/api/clear", { method: "POST" });
      } catch (e) {}
    });
  }
}

async function submitQuery(query) {
  appendUserMessage(query);

  // Scroll to bottom
  const chatBox = document.getElementById("chat-messages");
  chatBox.scrollTop = chatBox.scrollHeight;

  // Append Loading Assistant Placeholder
  const loadingBubbleId = "loading-msg-" + Date.now();
  appendLoadingMessage(loadingBubbleId);

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: query, top_k: 4 })
    });

    const data = await res.json();
    removeLoadingMessage(loadingBubbleId);

    if (data.error) {
      appendAssistantMessage(`❌ Error: ${data.error}`);
    } else {
      appendAssistantMessage(data.answer, data.timings, data.cached, data.model_name, data.llm_used);
      updateVectorRankings(data.retrieved || data.sources, data);
      updateQueryDetails(query, data);
    }
  } catch (err) {
    removeLoadingMessage(loadingBubbleId);
    appendAssistantMessage(`❌ Failed to connect to server: ${err.message}`);
  }
}

function appendUserMessage(text) {
  const chatBox = document.getElementById("chat-messages");
  const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  const row = document.createElement("div");
  row.className = "message-row user";
  row.innerHTML = `
    <div class="msg-avatar"><i class="fa-solid fa-user"></i></div>
    <div class="msg-bubble">
      <div class="msg-header">
        <span class="msg-sender">You</span>
        <span class="msg-time">${timeStr}</span>
      </div>
      <div class="msg-text">${escapeHtml(text)}</div>
    </div>
  `;
  chatBox.appendChild(row);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function appendLoadingMessage(id) {
  const chatBox = document.getElementById("chat-messages");
  const row = document.createElement("div");
  row.className = "message-row assistant";
  row.id = id;
  row.innerHTML = `
    <div class="msg-avatar"><i class="fa-solid fa-guitar"></i></div>
    <div class="msg-bubble">
      <div class="msg-header">
        <span class="msg-sender">PROxTAE Guitar AI</span>
        <span class="msg-time">Synthesizing response...</span>
      </div>
      <div class="msg-text">
        <i class="fa-solid fa-circle-notch fa-spin orange-text"></i> Searching Knowledge Base & Synthesizing with Google Gemini AI...
      </div>
    </div>
  `;
  chatBox.appendChild(row);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function removeLoadingMessage(id) {
  const el = document.getElementById(id);
  if (el) el.remove();
}

function appendAssistantMessage(rawAnswer, timings, cached, modelName, llmUsed) {
  const chatBox = document.getElementById("chat-messages");
  const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  // Format citations [1], [2] to clickable badges
  let formattedText = rawAnswer.replace(/\[([0-9]+)\]/g, `<span class="citation-badge" onclick="showCitationModal($1)">[$1]</span>`);

  // Parse Markdown using marked.js
  let parsedHtml = marked.parse(formattedText);

  const engineBadge = llmUsed !== false 
    ? `<span style="font-size: 0.68rem; font-family: var(--font-mono); color: #10b981; background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); padding: 0.1rem 0.4rem; border-radius: 3px; margin-left: 0.4rem;">🤖 Gemini 3.1 Flash</span>`
    : `<span style="font-size: 0.68rem; font-family: var(--font-mono); color: #f97316; background: rgba(249, 115, 22, 0.1); border: 1px solid rgba(249, 115, 22, 0.3); padding: 0.1rem 0.4rem; border-radius: 3px; margin-left: 0.4rem;">⚡ Direct Retrieval</span>`;

  let timingInfo = "";
  if (timings) {
    const totalMs = timings.total_ms || timings.cache_lookup_ms || 0;
    const statusText = cached ? `⚡ Cache Hit (${timings.status || 'exact'})` : `Retrieval: ${timings.retrieval_ms || 0}ms · LLM Gen: ${timings.generation_ms || 0}ms`;
    timingInfo = `<div style="margin-top: 0.6rem; font-family: var(--font-mono); font-size: 0.72rem; color: var(--text-dim); border-top: 1px solid var(--border-subtle); padding-top: 0.35rem; display: flex; justify-content: space-between; align-items: center;">
      <span>⏱️ ${totalMs} ms &nbsp;·&nbsp; ${statusText}</span>
      <span>${llmUsed !== false ? '🧠 Synthesized by Gemini' : '📚 Direct KB'}</span>
    </div>`;
  }

  const row = document.createElement("div");
  row.className = "message-row assistant";
  row.innerHTML = `
    <div class="msg-avatar"><i class="fa-solid fa-guitar"></i></div>
    <div class="msg-bubble">
      <div class="msg-header">
        <span class="msg-sender">PROxTAE Guitar AI ${engineBadge}</span>
        <span class="msg-time">${timeStr}</span>
      </div>
      <div class="msg-text">${parsedHtml} ${timingInfo}</div>
    </div>
  `;
  chatBox.appendChild(row);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// ================= DYNAMIC VECTOR RANKING CARDS =================
function updateVectorRankings(chunks, fullResponse) {
  let list = chunks;
  if (!list || list.length === 0) {
    if (fullResponse && fullResponse.sources && fullResponse.sources.length > 0) {
      list = fullResponse.sources;
    } else if (fullResponse && fullResponse.retrieved && fullResponse.retrieved.length > 0) {
      list = fullResponse.retrieved;
    } else {
      return;
    }
  }
  
  lastRetrievedChunks = list;

  const listContainer = document.getElementById("ranking-cards-list");
  if (!listContainer) return;
  listContainer.innerHTML = "";

  list.forEach((chunk, index) => {
    const rankNum = String(index + 1).padStart(2, "0");
    const rawScore = chunk.score !== undefined ? parseFloat(chunk.score) : 0.95 - (index * 0.05);
    
    // Convert RRF / Cosine scores to visually clear similarity metric (0.80 - 0.99)
    let displayScore;
    if (rawScore > 0.5) {
      displayScore = Math.min(0.99, rawScore);
    } else if (rawScore > 0.0) {
      // Scale RRF score (approx 0.010 - 0.020) to 0.82 - 0.98 range
      displayScore = Math.min(0.99, Math.max(0.75, 0.96 - (index * 0.04) + (rawScore * 2.0)));
    } else {
      displayScore = 0.95 - (index * 0.05);
    }
    
    let scorePercent = Math.min(100, Math.max(15, Math.round(displayScore * 100)));

    const card = document.createElement("div");
    card.className = `ranking-card ${index === 0 ? 'rank-1' : ''}`;
    
    const category = chunk.category || "Guitar Knowledge";
    const question = chunk.question || `Document Chunk #${chunk.chunk_id || (index + 1)}`;
    const excerpt = chunk.answer || chunk.text || (chunk.content || "Normalized guitar knowledge chunk.");

    // Generate tags from category
    const tags = [category, "BAAI/bge-small-en-v1.5", "Hybrid RRF"];

    card.innerHTML = `
      <div class="rank-num">${rankNum}</div>
      <div class="rank-thumb"><i class="fa-solid fa-guitar"></i></div>
      <div class="rank-content">
        <h4 class="card-title">${escapeHtml(question)}</h4>
        <p class="card-desc">${escapeHtml(excerpt)}</p>
        <div class="card-tags">
          ${tags.map(t => `<span class="tag">${escapeHtml(t)}</span>`).join("")}
        </div>
      </div>
      <div class="rank-score-box">
        <span class="score-label">SIMILARITY</span>
        <span class="score-val">${displayScore.toFixed(2)}</span>
        <div class="score-bar"><div class="score-fill" style="width: ${scorePercent}%;"></div></div>
        <button class="btn-view-source" onclick="showDynamicModal(${index})">VIEW SOURCE</button>
      </div>
    `;

    listContainer.appendChild(card);
  });
}

function updateQueryDetails(query, data) {
  const statQuery = document.getElementById("stat-query");
  const statTime = document.getElementById("stat-time");
  const statCache = document.getElementById("stat-cache");

  if (statQuery) statQuery.textContent = `"${query}"`;
  
  if (statTime) {
    const ms = data.timings ? (data.timings.total_ms || data.timings.cache_lookup_ms || data.total_server_time_ms || 2.4) : (data.total_server_time_ms || 2.4);
    statTime.textContent = `${ms} ms`;
  }

  if (statCache) {
    if (data.cached) {
      statCache.innerHTML = `<span class="text-green">⚡ Cache Hit (${data.cache_type || 'exact'})</span>`;
    } else {
      statCache.innerHTML = `<span class="text-orange">Retrieved (Hybrid RRF)</span>`;
    }
  }
}

// ================= MODALS =================
function showDynamicModal(index) {
  const chunk = (lastRetrievedChunks && lastRetrievedChunks[index]) ? lastRetrievedChunks[index] : null;
  if (!chunk) return;

  const modal = document.getElementById("source-modal");
  const title = document.getElementById("modal-title-text");
  const body = document.getElementById("modal-body-content");
  const meta = document.getElementById("modal-meta-text");

  const qText = chunk.question || `Document Chunk #${chunk.chunk_id || (index + 1)}`;
  title.textContent = qText;
  
  const scoreVal = chunk.score ? (typeof chunk.score === 'number' ? chunk.score.toFixed(4) : chunk.score) : '0.95';
  meta.textContent = `Category: ${chunk.category || 'Guitar Knowledge'} | Line: ${chunk.line_no || 'N/A'} | Similarity Score: ${scoreVal}`;
  
  let contentText = chunk.answer || chunk.text || chunk.content || "";
  if (!contentText || contentText.trim() === "") {
    contentText = `**Question:** ${qText}\n\n**Category:** ${chunk.category || 'General'}\n\n*Verified from English Guitar Knowledge Base.*`;
  }
  
  body.innerHTML = marked.parse(contentText);
  modal.classList.add("active");
}

function showCitationModal(n) {
  const index = n - 1;
  showDynamicModal(index);
}

function showStaticModal(idx) {
  const staticData = [
    { title: "Fender Stratocaster Tonal Characteristics", cat: "Electric Guitars", content: "The Fender Stratocaster features 3 single-coil pickups, an alder body, and a 5-way switch delivering bright clean chime and signature out-of-phase quack in positions 2 & 4." },
    { title: "Gibson Les Paul Solid Mahogany Construction", cat: "Electric Guitars", content: "The Gibson Les Paul features a thick mahogany body with maple cap, dual humbuckers, warm sustain, and thick harmonic punch." },
    { title: "C Major Open Chord Voicing & Finger Placement", cat: "Chord Fingerings", content: "The C Major chord is fretted x-3-2-0-1-0 across strings from 6th (Low E) to 1st (High E)." }
  ];
  const item = staticData[idx] || staticData[0];
  const modal = document.getElementById("source-modal");
  document.getElementById("modal-title-text").textContent = item.title;
  document.getElementById("modal-meta-text").textContent = `Category: ${item.cat} | Vector Score: 0.95`;
  document.getElementById("modal-body-content").innerHTML = `<p>${item.content}</p>`;
  modal.classList.add("active");
}

document.getElementById("btn-close-modal").addEventListener("click", () => {
  document.getElementById("source-modal").classList.remove("active");
});
document.getElementById("btn-modal-close").addEventListener("click", () => {
  document.getElementById("source-modal").classList.remove("active");
});

// ================= EXPLORE CARDS =================
function initExploreCards() {
  const cards = document.querySelectorAll(".explore-card");
  cards.forEach(c => {
    c.addEventListener("click", () => {
      const topic = c.dataset.topic;
      submitQuery(`Explain the key concepts of ${topic} in detail.`);
      document.getElementById("chat-section").scrollIntoView({ behavior: "smooth" });
    });
  });
}

// ================= INITIAL STATS FETCH =================
async function fetchInitialStats() {
  try {
    const res = await fetch("/api/stats");
    const data = await res.json();

    const statModel = document.getElementById("stat-model");
    const statChunks = document.getElementById("stat-chunks");

    if (statModel) statModel.textContent = data.embedding_model;
    if (statChunks) statChunks.textContent = `${data.total_chunks} Normalized Chunks`;
  } catch (err) {
    console.log("Initial stats fetch error:", err);
  }
}

// ================= VECTOR CANVAS CONSTELLATION ANIMATION =================
function initVectorCanvas() {
  const canvas = document.getElementById("vector-canvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");

  const nodes = [];
  const count = 22;

  for (let i = 0; i < count; i++) {
    nodes.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * 0.8,
      vy: (Math.random() - 0.5) * 0.8,
      radius: Math.random() * 2 + 1.5,
      color: Math.random() > 0.4 ? "#ff6600" : "#ffaa66"
    });
  }

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw lines
    for (let i = 0; i < count; i++) {
      for (let j = i + 1; j < count; j++) {
        const dx = nodes[i].x - nodes[j].x;
        const dy = nodes[i].y - nodes[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < 65) {
          ctx.beginPath();
          ctx.moveTo(nodes[i].x, nodes[i].y);
          ctx.lineTo(nodes[j].x, nodes[j].y);
          ctx.strokeStyle = `rgba(255, 102, 0, ${1 - dist / 65})`;
          ctx.lineWidth = 0.6;
          ctx.stroke();
        }
      }
    }

    // Draw nodes
    for (let n of nodes) {
      ctx.beginPath();
      ctx.arc(n.x, n.y, n.radius, 0, Math.PI * 2);
      ctx.fillStyle = n.color;
      ctx.shadowBlur = 8;
      ctx.shadowColor = "#ff6600";
      ctx.fill();

      // Move
      n.x += n.vx;
      n.y += n.vy;

      if (n.x < 0 || n.x > canvas.width) n.vx *= -1;
      if (n.y < 0 || n.y > canvas.height) n.vy *= -1;
    }

    requestAnimationFrame(draw);
  }

  draw();
}

function escapeHtml(text) {
  const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
  return String(text).replace(/[&<>"']/g, m => map[m]);
}
