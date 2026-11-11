const form = document.getElementById("messageForm");
const messageInput = document.getElementById("messageInput");
const messageType = document.getElementById("messageType");
const tone = document.getElementById("tone");
const generateBtn = document.getElementById("generateBtn");
const formError = document.getElementById("formError");
const charCount = document.getElementById("charCount");
const emptyState = document.getElementById("emptyState");
const loadingState = document.getElementById("loadingState");
const generatedText = document.getElementById("generatedText");
const outputActions = document.getElementById("outputActions");
const copyFeedback = document.getElementById("copyFeedback");

let latestMessage = "";

messageInput.addEventListener("input", () => {
  charCount.textContent = `${messageInput.value.length.toLocaleString()} / 12,000`;
  formError.textContent = "";
});

function showLoading(isLoading) {
  generateBtn.disabled = isLoading;
  generateBtn.querySelector(".btn-label").textContent = isLoading ? "Working..." : "Generate with AI";
  emptyState.hidden = true;
  generatedText.hidden = true;
  outputActions.hidden = true;
  loadingState.hidden = !isLoading;
  copyFeedback.textContent = "";
}

async function generateMessage() {
  const message = messageInput.value.trim();
  if (!message) {
    formError.textContent = "Please enter your message first.";
    messageInput.focus();
    return;
  }

  formError.textContent = "";
  showLoading(true);

  try {
    const response = await fetch("/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message,
        message_type: messageType.value,
        tone: tone.value
      })
    });

    const data = await response.json();
    if (!response.ok || !data.success) {
      throw new Error(data.error || "Something went wrong. Please try again.");
    }

    latestMessage = data.generated_message;
    generatedText.textContent = latestMessage;
    loadingState.hidden = true;
    generatedText.hidden = false;
    outputActions.hidden = false;
  } catch (error) {
    loadingState.hidden = true;
    emptyState.hidden = false;
    formError.textContent = error.message || "Unable to connect to the AI service. Please try again.";
  } finally {
    generateBtn.disabled = false;
    generateBtn.querySelector(".btn-label").textContent = "Generate with AI";
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  generateMessage();
});

document.getElementById("regenerateBtn").addEventListener("click", () => {
  // Calls the backend again, creating a fresh Groq API request.
  generateMessage();
});

document.getElementById("copyBtn").addEventListener("click", async () => {
  if (!latestMessage) return;
  try {
    await navigator.clipboard.writeText(latestMessage);
    copyFeedback.textContent = "Copied to clipboard!";
  } catch (_error) {
    copyFeedback.textContent = "Clipboard access was blocked by your browser.";
  }
});

document.getElementById("downloadBtn").addEventListener("click", () => {
  if (!latestMessage) return;
  const blob = new Blob([latestMessage], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "improved-message.txt";
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
});

document.getElementById("clearBtn").addEventListener("click", () => {
  form.reset();
  latestMessage = "";
  messageInput.value = "";
  charCount.textContent = "0 / 12,000";
  generatedText.textContent = "";
  generatedText.hidden = true;
  loadingState.hidden = true;
  outputActions.hidden = true;
  emptyState.hidden = false;
  formError.textContent = "";
  copyFeedback.textContent = "";
});
