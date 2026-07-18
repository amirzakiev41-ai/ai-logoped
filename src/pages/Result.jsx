function Result({ recordings }) {

  const playAudio = (audioBlob) => {
    const audioUrl = URL.createObjectURL(audioBlob);

    const audio = new Audio(audioUrl);
    audio.play();
  };

  return (
    <div className="page">
      <h1>🎉</h1>

      <h2>Отличная работа!</h2>

      <div
        style={{
          width: "100%",
          maxWidth: "500px",
          marginTop: "30px",
        }}
      >
        {recordings.map((recording, index) => (
          <div
            key={index}
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",

              padding: "12px 20px",

              background: "white",

              borderRadius: "12px",

              marginBottom: "12px",

              boxShadow:
                "0 4px 12px rgba(0,0,0,0.08)",
            }}
          >
            <strong>
              {recording.word}
            </strong>

            <button
              onClick={() =>
                playAudio(recording.audio)
              }
            >
              ▶️
            </button>
          </div>
        ))}
      </div>

      <button className="primary-btn">
        Начать тренировку
      </button>
    </div>
  );
}

export default Result;