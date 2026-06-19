function Welcome({ onStart }) {
  return (
    <div style={{ textAlign: "center", padding: "40px" }}>
      <h1>🤖</h1>

      <h2>Привет!</h2>

      <p>
        Я помогу тебе тренировать речь
        и говорить красиво.
      </p>

      <button onClick={onStart}>
        Начать 🚀
      </button>
    </div>
  );
}

export default Welcome;