let chatHistory = [];
let userApiKey = localStorage.getItem('openrouter_key') || '';
let userModel = localStorage.getItem('openrouter_model') || 'nvidia/nemotron-3.5-lightning:free';

document.addEventListener('DOMContentLoaded', () => {
  if (userApiKey) {
    document.getElementById('openrouter-key-input').value = userApiKey;
  }
  if (userModel) {
    document.getElementById('openrouter-model-select').value = userModel;
  }
});

function toggleKeyModal() {
  const modal = document.getElementById('key-modal');
  modal.classList.toggle('hidden');
}

function saveKeySettings() {
  userApiKey = document.getElementById('openrouter-key-input').value.trim();
  userModel = document.getElementById('openrouter-model-select').value;
  localStorage.setItem('openrouter_key', userApiKey);
  localStorage.setItem('openrouter_model', userModel);
  toggleKeyModal();
}

function sendQuickPrompt(promptText) {
  document.getElementById('user-input').value = promptText;
  handleChatSubmit(new Event('submit'));
}

async function handleChatSubmit(e) {
  if (e && e.preventDefault) e.preventDefault();
  
  const inputEl = document.getElementById('user-input');
  const message = inputEl.value.trim();
  if (!message) return;

  // Add User Message
  appendUserMessage(message);
  inputEl.value = '';

  // Add Loading indicator
  const loadingId = appendLoadingIndicator();
  const sendBtn = document.getElementById('send-btn');
  sendBtn.disabled = true;

  chatHistory.push({ role: 'user', content: message });

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        messages: chatHistory,
        openrouter_api_key: userApiKey || null,
        model: userModel
      })
    });

    const data = await res.json();
    removeLoadingIndicator(loadingId);

    if (data.reply) {
      chatHistory.push({ role: 'assistant', content: data.reply });
      appendAssistantMessage(data.reply, data.engine);
      updateKnowledgeFeed(data.search_results);
    } else {
      appendAssistantMessage("I encountered an issue retrieving real estate details. Please try again.", "Error");
    }
  } catch (err) {
    console.error(err);
    removeLoadingIndicator(loadingId);
    appendAssistantMessage("Network or connection error. Please check your setup.", "Error");
  } finally {
    sendBtn.disabled = false;
  }
}

function appendUserMessage(text) {
  const chatBox = document.getElementById('chat-box');
  const div = document.createElement('div');
  div.className = "flex items-start justify-end space-x-3 max-w-3xl ml-auto";
  div.innerHTML = `
    <div class="bg-amber-500 text-slate-950 font-medium rounded-2xl rounded-tr-sm p-4 text-sm leading-relaxed shadow-md">
      ${escapeHtml(text)}
    </div>
    <div class="w-8 h-8 rounded-lg bg-amber-500/20 border border-amber-500/40 text-amber-400 flex items-center justify-center flex-shrink-0 mt-1">
      <i class="fa-solid fa-user text-sm"></i>
    </div>
  `;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function appendAssistantMessage(markdownText, engine) {
  const chatBox = document.getElementById('chat-box');
  const div = document.createElement('div');
  div.className = "flex items-start space-x-3 max-w-3xl";
  
  const parsedHtml = marked.parse(markdownText);

  div.innerHTML = `
    <div class="w-8 h-8 rounded-lg bg-amber-500/20 border border-amber-500/40 text-amber-400 flex items-center justify-center flex-shrink-0 mt-1">
      <i class="fa-solid fa-robot text-sm"></i>
    </div>
    <div class="bg-slate-900 border border-slate-800 rounded-2xl rounded-tl-sm p-4 text-sm leading-relaxed text-slate-200 shadow-md flex-1">
      <div class="flex items-center justify-between pb-2 mb-2 border-b border-slate-800 text-xs text-slate-400">
        <span class="font-semibold text-amber-400">Real Estate Advisor</span>
        <span class="text-[10px] bg-slate-800 px-2 py-0.5 rounded text-slate-400 border border-slate-700/50">${engine || 'AI Engine'}</span>
      </div>
      <div class="markdown-body">
        ${parsedHtml}
      </div>
    </div>
  `;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function appendLoadingIndicator() {
  const chatBox = document.getElementById('chat-box');
  const id = 'loading-' + Date.now();
  const div = document.createElement('div');
  div.id = id;
  div.className = "flex items-start space-x-3 max-w-3xl";
  div.innerHTML = `
    <div class="w-8 h-8 rounded-lg bg-amber-500/20 border border-amber-500/40 text-amber-400 flex items-center justify-center flex-shrink-0 mt-1 animate-pulse">
      <i class="fa-solid fa-robot text-sm"></i>
    </div>
    <div class="bg-slate-900 border border-slate-800 rounded-2xl rounded-tl-sm p-4 text-sm text-slate-400 shadow-md flex items-center space-x-2">
      <span class="w-2 h-2 rounded-full bg-amber-400 animate-ping"></span>
      <span>Consulting DarGlobal & Wasalt Real Estate Knowledge...</span>
    </div>
  `;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
  return id;
}

function removeLoadingIndicator(id) {
  const el = document.getElementById(id);
  if (el) el.remove();
}

function updateKnowledgeFeed(results) {
  if (!results) return;
  const container = document.getElementById('cards-container');
  container.innerHTML = '';

  const dgList = results.darglobal || [];
  const wasaltList = results.wasalt || [];

  if (dgList.length === 0 && wasaltList.length === 0) {
    container.innerHTML = `<p class="text-xs text-slate-500">No direct card matches for this query.</p>`;
    return;
  }

  dgList.forEach(p => {
    const card = document.createElement('div');
    card.className = "bg-slate-950 border border-amber-500/30 rounded-xl p-3 text-xs space-y-1.5 shadow";
    card.innerHTML = `
      <div class="flex items-center justify-between">
        <span class="font-bold text-amber-400">${p.project_name}</span>
        <span class="text-[10px] bg-amber-500/10 text-amber-300 border border-amber-500/20 px-1.5 py-0.5 rounded">DarGlobal</span>
      </div>
      <p class="text-slate-300 line-clamp-2">${p.description}</p>
      <div class="text-[11px] text-slate-400 flex items-center justify-between pt-1">
        <span>📍 ${p.location}</span>
        <a href="${p.url}" target="_blank" class="text-sky-400 hover:underline">Link &rarr;</a>
      </div>
    `;
    container.appendChild(card);
  });

  wasaltList.forEach(p => {
    const card = document.createElement('div');
    card.className = "bg-slate-950 border border-emerald-500/30 rounded-xl p-3 text-xs space-y-1.5 shadow";
    const priceStr = typeof p.price === 'number' ? p.price.toLocaleString() + ' SAR' : (p.price || 'Contact');
    card.innerHTML = `
      <div class="flex items-center justify-between">
        <span class="font-bold text-emerald-400 truncate">${p.title}</span>
        <span class="text-[10px] bg-emerald-500/10 text-emerald-300 border border-emerald-500/20 px-1.5 py-0.5 rounded">Wasalt</span>
      </div>
      <p class="text-slate-300">${p.location.district || ''}, ${p.location.city} • <span class="text-emerald-300 font-semibold">${priceStr}</span></p>
      <div class="text-[11px] text-slate-400 flex items-center justify-between pt-1">
        <span>${p.specs.bedrooms ? p.specs.bedrooms + ' Beds' : ''} ${p.specs.area_sqm ? '• ' + p.specs.area_sqm + ' SQM' : ''}</span>
        <a href="${p.url}" target="_blank" class="text-sky-400 hover:underline">View &rarr;</a>
      </div>
    `;
    container.appendChild(card);
  });
}

function escapeHtml(str) {
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
