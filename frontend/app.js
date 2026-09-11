const API_URL = "http://127.0.0.1:8000/api/chat";
const sessionId = crypto.randomUUID();

const form = document.getElementById("chat-form");
const input = document.getElementById("message");
const chat = document.getElementById("chat");

function addMessage(role, text, meta = "") {
  const div = document.createElement("div");
  div.className = `message ${role}`;
  div.textContent = text;

  if (meta) {
    const metaDiv = document.createElement("div");
    metaDiv.className = "meta";
    metaDiv.textContent = meta;
    div.appendChild(metaDiv);
  }

  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const message = input.value.trim();
  if (!message) return;

  addMessage("user", message);
  input.value = "";

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        session_id: sessionId,
        message
      })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Request failed.");
    }

    const tools = data.tools_used
      .map(tool => `${tool.tool} (${tool.status})`)
      .join(", ") || "None";

    const sources = data.sources
      .map(source => source.title)
      .join(", ") || "None";

    addMessage(
      "assistant",
      data.answer,
      `Intent: ${data.intent.join(" + ")} | MCP: ${tools} | Sources: ${sources}`
    );
  } catch (error) {
    addMessage("assistant", `Error: ${error.message}`);
  }
});
