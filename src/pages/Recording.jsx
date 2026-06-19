import { useEffect } from "react";

function Recording({ onFinish }) {

  useEffect(() => {
    const timer = setTimeout(() => {
      onFinish();
    }, 3000);

    return () => clearTimeout(timer);
  }, []);

  return (
    <div style={{ textAlign: "center", padding: "40px" }}>
      <h1>🎤</h1>

      <h2>Запись идёт...</h2>

      <p>
        Произнеси слово громко и чётко
      </p>
    </div>
  );
}

export default Recording;