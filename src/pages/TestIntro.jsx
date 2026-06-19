function TestIntro({ onStartTest }) {
  return (
    <div>
      <h1>🤖</h1>

      <h2>
        Давай проверим,
        какие звуки у тебя получаются лучше всего.
      </h2>

      <p>
        Это займёт всего пару минут.
      </p>

      <button onClick={onStartTest}>
        Начать тест
      </button>
    </div>
  );
}

export default TestIntro;