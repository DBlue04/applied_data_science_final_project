document.addEventListener('DOMContentLoaded', () => {
  const data     = JSON.parse(document.getElementById('server-data').textContent);
  const resultEl = document.getElementById('result-audio');

  if (!data.wav) {
    data.wav = localStorage.getItem('lastBanterAudio') || '';
  }

  const wipeCache = () => {
    localStorage.removeItem('lastBanterPrompt');
    localStorage.removeItem('lastBanterReply');
    localStorage.removeItem('lastBanterAudio');
  };

  const nextURL = `/quiz/${data.next_id}`;
  let   jumped  = false;
  const goNext  = () => { if (!jumped) { jumped = true; window.location.href = nextURL; } };

  function playChatAudio() {
    if (jumped) return;

    if (data.wav) {
      const chat = new Audio(data.wav);
      chat.addEventListener('canplaythrough', () => chat.play());
      chat.addEventListener('ended', () => { wipeCache(); goNext(); });
      chat.addEventListener('error', goNext);
    } else {                    
      wipeCache();
      goNext();
    }
  }

  resultEl.addEventListener('ended', playChatAudio);
  resultEl.addEventListener('error', playChatAudio);

  setTimeout(playChatAudio, 120000);
});
