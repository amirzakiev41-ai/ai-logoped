
import { useState } from "react";

function Result({ recordings, onRestart }) {
  const [playing, setPlaying] = useState(null);

  const analyzed = recordings.filter(
    (recording) => recording.result
  );

  const averageScore = analyzed.length
    ? analyzed.reduce(
        (sum, recording) =>
          sum + (Number(recording.result.score) || 0),
        0
      ) / analyzed.length
    : 0;

  const successfulWords = analyzed.filter(
    (recording) => recording.result.status === "SUCCESS"
  ).length;

  const playAudio = (audioBlob, index) => {
    const audioUrl = URL.createObjectURL(audioBlob);
    const audio = new Audio(audioUrl);

    setPlaying(index);

    audio.onended = () => {
      setPlaying(null);
      URL.revokeObjectURL(audioUrl);
    };

    audio.onerror = () => {
      setPlaying(null);
      URL.revokeObjectURL(audioUrl);
    };

    audio.play().catch(() => {
      setPlaying(null);
      URL.revokeObjectURL(audioUrl);
    });
  };

  return (
    <div className="page">
      <h1>Результаты тестирования</h1>

      <h2>
        Средний балл: {averageScore.toFixed(1)} / 100
      </h2>

      <p>
        Успешно распознано: {successfulWords} из{" "}
        {analyzed.length}
      </p>

      <div
        style={{
          width: "100%",
          maxWidth: "550px",
          marginTop: "25px",
        }}
      >
        {recordings.map((recording, index) => {
          const result = recording.result;

          return (
            <div
              key={index}
              style={{
                background: "white",
                padding: "20px",
                borderRadius: "12px",
                marginBottom: "15px",
                boxShadow:
                  "0 4px 12px rgba(0,0,0,0.08)",
                color: "#222",
              }}
            >
              <h3>{recording.word}</h3>

              <p>
                Распознано:{" "}
                <strong>
                  {result?.recognized_word || "Нет данных"}
                </strong>
              </p>

              <p>
                Балл:{" "}
                <strong>
                  {result?.score ?? "Нет данных"}
                </strong>
              </p>

              <p>
                Статус:{" "}
                <strong
                  style={{
                    color:
                      result?.status === "SUCCESS"
                        ? "green"
                        : "darkorange",
                  }}
                >
                  {result?.status === "SUCCESS"
                    ? "Успешно"
                    : "Требует внимания"}
                </strong>
              </p>

              <button
                onClick={() =>
                  playAudio(recording.audio, index)
                }
                disabled={playing === index}
              >
                {playing === index
                  ? "Воспроизводится..."
                  : "▶ Прослушать запись"}
              </button>
            </div>
          );
        })}
      </div>

      <button
        className="primary-btn"
        onClick={onRestart}
      >
        Начать тренировку заново
      </button>
    </div>
  );
}

export default Result;
