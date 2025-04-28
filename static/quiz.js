document.addEventListener('DOMContentLoaded', () => {
  const data = JSON.parse(document.getElementById('server-data').textContent);
  const { questionId, commentPrompt, commentReply, commentWav } = data;

  const chatWin  = document.getElementById('chat-window');
  const CHAT_KEY = 'quizChatHistory';
  let hist = [];

  function append(text, cls) {
    const p   = document.createElement('p');
    p.textContent = text;
    p.className   = cls;
    chatWin.appendChild(p);
    chatWin.scrollTop = chatWin.scrollHeight;
    hist.push({ text, cls });
    localStorage.setItem(CHAT_KEY, JSON.stringify(hist));
  }

  (function loadHistory() {
    if (questionId === 0) localStorage.removeItem(CHAT_KEY);
    hist = JSON.parse(localStorage.getItem(CHAT_KEY) || '[]');
    hist.forEach(m => append(m.text, m.cls));
  })();

  async function sendUser(txt) {
    append('🗨️ ' + txt, 'user');

    const res = await fetch('/chat', {
      method : 'POST',
      headers: { 'Content-Type': 'application/json' },
      body   : JSON.stringify({ question_id: questionId, text: txt })
    });
    const d = await res.json();

    append('💬 ' + d.reply, 'bot');

    /* remember latest banter so the answer page can replay it */
    localStorage.setItem('lastBanterPrompt', txt);
    localStorage.setItem('lastBanterReply',  d.reply);
    localStorage.setItem('lastBanterAudio',  d.audio_url);

    new Audio(d.audio_url).play();
  }

  const input = document.getElementById('chat-input');
  const send  = document.getElementById('send-btn');

  send.onclick = () => {
    const t = input.value.trim();
    if (t) {
      input.value = '';
      sendUser(t);
    }
  };
  input.onkeydown = e => { if (e.key === 'Enter') { e.preventDefault(); send.click(); } };

  const timerEl = document.getElementById('timer');
  let left = 30, ticking = false, tickInt;

  document.getElementById('q-audio').onended = () => {
    if (ticking) return;
    ticking = true;
    tickInt = setInterval(() => {
      timerEl.textContent = --left;
      if (left <= 0) {
        clearInterval(tickInt);
        finish();
      }
    }, 1000);
  };

  document.getElementById('answer-form').onsubmit = e => {
    e.preventDefault();
    clearInterval(tickInt);
    finish();
  };

  function finish() {
    document.querySelectorAll('input,button').forEach(el => el.disabled = true);

    if (commentPrompt) {
      append('🗨️ ' + commentPrompt, 'user');
      append('💬 ' + commentReply,  'bot');

      const a = new Audio(commentWav);
      a.onended = () => document.getElementById('answer-form').submit();
      a.play();
    } else {
      document.getElementById('answer-form').submit();
    }
  }
});
