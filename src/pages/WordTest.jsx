import fish from "../assets/fish.png";
import crayfish from "../assets/crayfish.png";
import ball from "../assets/ball.png";
import bug from "../assets/bug.png";
import lamp from "../assets/lamp.png";
import Card from "../components/Card/Card";
import ProgressBar from "../components/ProgressBar/ProgressBar";
function WordTest({ word, onRecord, current, total }) {
  const handleMicClick = async () => {
    try {
      await navigator.mediaDevices.getUserMedia({
        audio: true,
      });

      onRecord();
    } catch (error) {
      alert("Не удалось получить доступ к микрофону");
    }
  };

  const wordImages = {
  РЫБА: fish,
  РАК: crayfish,
  ШАР: ball,
  ЖУК: bug,
  ЛАМПА: lamp,
};

  return (
    <div className="page">
      <ProgressBar
  current={current}
  total={total}
/>

     <Card>
  <img
    src={wordImages[word]}
    alt={word}
    className="word-image"
  />

  <h1 className="word-title">
    {word}
  </h1>

  <p>
    Нажми на микрофон и произнеси слово
  </p>

  <button
    className="mic-btn"
    onClick={handleMicClick}
  >
    🎤
  </button>

  <p style={{ marginTop: "20px" }}>
    {current} / {total}
  </p>
</Card>
    </div>
  );
}

export default WordTest;