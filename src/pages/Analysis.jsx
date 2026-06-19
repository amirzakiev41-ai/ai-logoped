import { useEffect } from "react";

function Analysis({ onFinish }) {

  useEffect(() => {
    const timer = setTimeout(() => {
      onFinish();
    }, 2000);

    return () => clearTimeout(timer);
  }, []);

  return (
    <div style={{ textAlign: "center", padding: "40px" }}>
      <h1>🧠</h1>

      <h2>Анализируем речь...</h2>

      <p>
        Пожалуйста, подожди несколько секунд
      </p>
    </div>
  );
}

export default Analysis;