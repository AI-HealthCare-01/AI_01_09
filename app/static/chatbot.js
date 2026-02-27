// 챗봇 상태 관리
const chatbot = {
  isOpen: false,
  sessionId: null,
  messages: [],
};

// 챗봇 초기화
function initChatbot() {
  const button = document.getElementById('chatbot-button');
  const container = document.getElementById('chatbot-container');
  const closeBtn = document.getElementById('chatbot-close');
  const endBtn = document.getElementById('chatbot-end');
  const ttsBtn = document.getElementById('chatbot-tts');
  const sendBtn = document.getElementById('chatbot-send');
  const input = document.getElementById('chatbot-input');

  // 챗봇 열기/닫기
  button.addEventListener('click', toggleChatbot);
  closeBtn.addEventListener('click', toggleChatbot);

  // 챗 종료
  endBtn.addEventListener('click', endChat);

  // TTS 읽어주기
  ttsBtn.addEventListener('click', readLastMessage);

  // 메시지 전송
  sendBtn.addEventListener('click', sendMessage);
  input.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  // 초기 환영 메시지
  addMessage('assistant', '안녕하세요! 👋 Cloud9 Care 챗봇입니다. 무엇을 도와드릴까요?');
}

// 챗봇 토글
function toggleChatbot() {
  chatbot.isOpen = !chatbot.isOpen;
  const container = document.getElementById('chatbot-container');
  
  if (chatbot.isOpen) {
    container.classList.add('open');
  } else {
    container.classList.remove('open');
  }
}

// 메시지 전송
async function sendMessage() {
  const input = document.getElementById('chatbot-input');
  const message = input.value.trim();
  
  if (!message) return;

  // 사용자 메시지 추가
  addMessage('user', message);
  input.value = '';

  // 로딩 표시
  showTypingIndicator();

  try {
    // API 호출
    const response = await fetch('/api/v1/chat/message', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: message,
        session_id: chatbot.sessionId,
      }),
    });

    if (!response.ok) {
      throw new Error('메시지 전송 실패');
    }

    const data = await response.json();
    
    // 세션 ID 저장
    if (data.session_id) {
      chatbot.sessionId = data.session_id;
    }

    // 로딩 제거
    hideTypingIndicator();

    // 봇 응답 추가
    addMessage('assistant', data.assistant_message || '응답을 받지 못했습니다.');

    // 응급 상황 처리
    if (data.action_type === 'EMERGENCY') {
      addEmergencyAlert();
    }

  } catch (error) {
    console.error('챗봇 오류:', error);
    hideTypingIndicator();
    addMessage('assistant', '죄송합니다. 일시적인 오류가 발생했습니다. 다시 시도해주세요.');
  }
}

// 메시지 추가
function addMessage(role, content) {
  const messagesContainer = document.getElementById('chatbot-messages');
  const messageDiv = document.createElement('div');
  messageDiv.className = `message ${role}`;

  const avatar = document.createElement('div');
  avatar.className = 'message-avatar';
  avatar.textContent = role === 'user' ? '👤' : '🤖';

  const contentDiv = document.createElement('div');
  contentDiv.className = 'message-content';
  contentDiv.textContent = content;

  messageDiv.appendChild(avatar);
  messageDiv.appendChild(contentDiv);

  messagesContainer.appendChild(messageDiv);
  
  // 스크롤을 최하단으로
  messagesContainer.scrollTop = messagesContainer.scrollHeight;

  // 메시지 저장
  chatbot.messages.push({ role, content, timestamp: new Date() });
}

// 타이핑 인디케이터 표시
function showTypingIndicator() {
  const messagesContainer = document.getElementById('chatbot-messages');
  const typingDiv = document.createElement('div');
  typingDiv.className = 'message assistant';
  typingDiv.id = 'typing-indicator';

  const avatar = document.createElement('div');
  avatar.className = 'message-avatar';
  avatar.textContent = '🤖';

  const typingContent = document.createElement('div');
  typingContent.className = 'message-content typing-indicator';
  typingContent.innerHTML = `
    <div class="typing-dot"></div>
    <div class="typing-dot"></div>
    <div class="typing-dot"></div>
  `;

  typingDiv.appendChild(avatar);
  typingDiv.appendChild(typingContent);
  messagesContainer.appendChild(typingDiv);
  
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// 타이핑 인디케이터 제거
function hideTypingIndicator() {
  const indicator = document.getElementById('typing-indicator');
  if (indicator) {
    indicator.remove();
  }
}

// 응급 알림 추가
function addEmergencyAlert() {
  const messagesContainer = document.getElementById('chatbot-messages');
  const alertDiv = document.createElement('div');
  alertDiv.className = 'message assistant';
  alertDiv.style.background = '#fff3cd';
  alertDiv.style.border = '2px solid #ff6b6b';
  alertDiv.style.padding = '12px';
  alertDiv.style.borderRadius = '8px';
  alertDiv.style.marginTop = '10px';

  alertDiv.innerHTML = `
    <strong style="color: #d63031;">⚠️ 응급 상황 감지</strong><br>
    <p style="margin-top: 8px; font-size: 13px;">
      즉시 가까운 응급실을 방문하시거나<br>
      119에 연락하시기 바랍니다.
    </p>
  `;

  messagesContainer.appendChild(alertDiv);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// 액세스 토큰 가져오기 (로컬 스토리지 또는 쿠키에서)
function getAccessToken() {
  // 비로그인 상태에서도 챗봇 사용 가능하므로 빈 문자열 반환
  return localStorage.getItem('access_token') || '';
}

// 챗 종료 기능
async function endChat() {
  if (!confirm('챗을 종료하시겠습니까? 모든 대화 내용이 삭제됩니다.')) {
    return;
  }

  // 세션 초기화
  chatbot.sessionId = null;
  chatbot.messages = [];

  // 메시지 창 초기화
  const messagesContainer = document.getElementById('chatbot-messages');
  messagesContainer.innerHTML = '';

  // 환영 메시지 다시 표시
  addMessage('assistant', '안녕하세요! 👋 Cloud9 Care 챗봇입니다. 무엇을 도와드릴까요?');

  alert('챗이 종료되었습니다.');
}

// 마지막 AI 답변 읽어주기 (TTS)
function readLastMessage() {
  // 마지막 assistant 메시지 찾기
  const assistantMessages = chatbot.messages.filter(msg => msg.role === 'assistant');
  
  if (assistantMessages.length === 0) {
    alert('읽어줄 메시지가 없습니다.');
    return;
  }

  const lastMessage = assistantMessages[assistantMessages.length - 1].content;

  // Web Speech API 사용
  if ('speechSynthesis' in window) {
    // 이전 음성 중지
    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(lastMessage);
    utterance.lang = 'ko-KR'; // 한국어
    utterance.rate = 1.0; // 속도
    utterance.pitch = 1.0; // 음정
    
    window.speechSynthesis.speak(utterance);
  } else {
    alert('이 브라우저는 음성 읽기를 지원하지 않습니다.');
  }
}

// 페이지 로드 시 초기화
document.addEventListener('DOMContentLoaded', initChatbot);
