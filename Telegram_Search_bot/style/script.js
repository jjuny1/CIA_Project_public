function GoToMessage(replyToId) {
  const targetId = `${replyToId}`;
  const targetElement = document.getElementById(targetId);

  if (targetElement) {
      targetElement.scrollIntoView({ behavior: 'smooth' });
      // 색상 변화
      targetElement.classList.add('highlight-message');
      setTimeout(() => {
        targetElement.classList.remove('highlight-message');
    }, 2000);
      return false;
  } else {
      console.error('해당 메시지를 찾을 수 없습니다:', targetId);
      return false;
  }
}