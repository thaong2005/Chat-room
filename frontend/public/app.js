const statusText = document.getElementById("statusText");
const usernameBadge = document.getElementById("usernameBadge");
const messagesEl = document.getElementById("messages");
const typingText = document.getElementById("typingText");
const userListEl = document.getElementById("userList");

const joinModal = document.getElementById("joinModal");
const joinForm = document.getElementById("joinForm");
const nameInput = document.getElementById("nameInput");

const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");

let socket;
let username = "";
let typingTimer;

function connectSocket() {
  const scheme = window.location.protocol === "https:" ? "wss" : "ws";
  socket = new WebSocket(`${scheme}://${window.location.host}/ws`);

  socket.addEventListener("open", () => {
    statusText.textContent = "Connected";
  });

  socket.addEventListener("close", () => {
    statusText.textContent = "Disconnected";
  });

  socket.addEventListener("message", (event) => {
    const payload = JSON.parse(event.data);
    handleServerEvent(payload);
  });
}

function handleServerEvent(payload) {
  switch (payload.type) {
    case "joined": {
      username = payload.username;
      usernameBadge.textContent = username;
      joinModal.classList.add("hidden");
      messagesEl.innerHTML = "";
      for (const item of payload.history || []) {
        appendMessage(item.username, item.content, item.timestamp);
      }
      return;
    }
    case "message": {
      appendMessage(payload.username, payload.content, payload.timestamp);
      return;
    }
    case "system": {
      appendSystemMessage(payload.content);
      return;
    }
    case "users": {
      renderUserList(payload.users || []);
      return;
    }
    case "typing": {
      renderTyping(payload.users || []);
      return;
    }
    case "error": {
      appendSystemMessage(`Error: ${payload.message}`);
      return;
    }
    default:
      return;
  }
}

function appendMessage(author, content, timestamp) {
  const shouldStick =
    messagesEl.scrollHeight - messagesEl.scrollTop - messagesEl.clientHeight < 60;

  const row = document.createElement("article");
  row.className = "message-row";

  const time = new Date(timestamp).toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });

  row.innerHTML = `
    <div class="message-author">${escapeHtml(author)} <span>${escapeHtml(time)}</span></div>
    <div class="message-content">${escapeHtml(content)}</div>
  `;

  messagesEl.appendChild(row);

  if (shouldStick) {
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }
}

function appendSystemMessage(content) {
  const row = document.createElement("p");
  row.className = "system-row";
  row.textContent = content;
  messagesEl.appendChild(row);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function renderUserList(users) {
  userListEl.innerHTML = "";
  for (const name of users) {
    const li = document.createElement("li");
    li.textContent = name;
    if (name === username) {
      li.classList.add("self");
    }
    userListEl.appendChild(li);
  }
}

function renderTyping(users) {
  const others = users.filter((name) => name !== username);
  if (others.length === 0) {
    typingText.textContent = "";
    return;
  }
  if (others.length === 1) {
    typingText.textContent = `${others[0]} is typing...`;
    return;
  }
  typingText.textContent = `${others.length} people are typing...`;
}

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

joinForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const candidate = nameInput.value.trim();
  if (!candidate) {
    return;
  }

  if (socket.readyState !== WebSocket.OPEN) {
    appendSystemMessage("Connection is not ready yet.");
    return;
  }

  socket.send(
    JSON.stringify({
      type: "join",
      username: candidate,
    })
  );
});

chatForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const content = messageInput.value.trim();
  if (!content || !username) {
    return;
  }

  socket.send(
    JSON.stringify({
      type: "message",
      content,
    })
  );

  socket.send(
    JSON.stringify({
      type: "typing",
      isTyping: false,
    })
  );

  messageInput.value = "";
});

messageInput.addEventListener("input", () => {
  if (!username || socket.readyState !== WebSocket.OPEN) {
    return;
  }

  socket.send(
    JSON.stringify({
      type: "typing",
      isTyping: true,
    })
  );

  clearTimeout(typingTimer);
  typingTimer = window.setTimeout(() => {
    socket.send(
      JSON.stringify({
        type: "typing",
        isTyping: false,
      })
    );
  }, 900);
});

connectSocket();
