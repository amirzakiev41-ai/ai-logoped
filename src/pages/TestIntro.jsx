function TestIntro({ onStartTest }) {
  return (
    <div className="page">
      <div className="word-card">
        <div className="avatar">
          🤖
          </div>

        <h2>
          Давай проверим,
          <br />
          какие звуки у тебя получаются лучше всего.
        </h2>

        <p className="subtitle">
          Это займёт всего пару минут.
        </p>

        <button
          className="primary-btn"
          onClick={onStartTest}
        >
          Начать тест
        </button>
      </div>
    </div>
  );
}

export default TestIntro;