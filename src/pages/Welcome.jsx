import Button from "../components/Button/Button";

function Welcome({ onStart }) {
  return (
    <div className="page">
      <div className="avatar">
        🤖
      </div>

      <h1>AI Логопед</h1>

      <p className="subtitle">
        Привет! Я помогу тебе тренировать речь
        и научиться красиво произносить звуки.
      </p>

      <Button onClick={onStart}>
        Начать тест 🚀
      </Button>
    </div>
  );
}

export default Welcome;