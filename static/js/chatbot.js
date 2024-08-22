const chatbotForm = document.getElementById("chatbot-form");
const chatbotInput = document.getElementById("chatbot-input");
const chatbotMessages = document.getElementById("chatbot-conversation");

chatbotForm.addEventListener("submit", (event) => {
  event.preventDefault();

  // 필드 인풋
  const message = chatbotInput.value;

  // 챗봇 메시지 html 추가

  chatbotMessages.innerHTML += `<div class="item"><div class="icon"><i class="fa fa-user"></i></div><div class="msg"><p> ${message} </p></div>`;
  chatbotMessages.innerHTML += `<div class="item right " id="chat-typing"><div><div class="typing"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div></div></div>`;
  chatbotInput.setAttribute("disabled", "");

  // 필드 초기화
  chatbotInput.value = "";
  window.scrollTo(0, document.body.scrollHeight);

  // 챗봇에 메시지 전송 - 리스폰
  getChatbotResponse(message).then((response) => {
    document.getElementById("chat-typing").remove();
    chatbotMessages.innerHTML += `<div class="item right"><div class="msg"><pre> ${response} </pre></div></div>`;
    chatbotInput.removeAttribute("disabled");
    window.scrollTo(0, document.body.scrollHeight);
  });
});

async function getChatbotResponse(message) {
  // 응답 생성
  var csrftoken = "{{csrf_token | escapejs}}"; // csrf token 및 특수문자 escape 처리
  try {
    // 메시지 전송 fetch 함수
    const response = await fetch("gpt-msg", {
      method: "POST",
      headers: {
        "Content-Tpye": "application/json",
        "X-CSRFTocken": csrftoken,
      },
      body: JSON.stringify({ message: message }),
    });
    return await response.text();
  } catch (e) {
    console.error(e);
    return "요청 중에 에러가 발생했습니다.";
  }
}
