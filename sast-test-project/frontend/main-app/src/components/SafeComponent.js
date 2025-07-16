// False Positive: Кажется опасным, но на самом деле безопасно
function SafeComponent() {
  const content = "<b>Это безопасный HTML</b>"; // Жестко закодированное значение
  
  // False Positive: SAST может ошибочно детектировать XSS
  return <div dangerouslySetInnerHTML={{ __html: content }} />; // На самом деле безопасно
}