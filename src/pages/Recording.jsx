import { useRecorder } from "../hooks/useRecorder";

function Recording({
  onFinish,
  word,
  wordIndex,
  userId,
  recordings,
  setRecordings,
}) {
  useRecorder({
    word,
    wordIndex,
    userId,
    recordings,
    setRecordings,
    onFinish,
  });

  return (
    <div className="page">
      <div className="recording-container">
        <div className="mic-pulse">🎤</div>
        <h2>Запись идёт...</h2>
        <p>Произнеси слово громко и чётко</p>
        <div className="wave">
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
    </div>
  );
}

export default Recording;