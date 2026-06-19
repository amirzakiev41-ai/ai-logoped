import { useState } from "react";
import Welcome from "./pages/Welcome";
import TestIntro from "./pages/TestIntro";
import WordTest from "./pages/WordTest";
import Recording from "./pages/Recording";
import Analysis from "./pages/Analysis";
import Result from "./pages/Result";

function App() {

  
  const [screen, setScreen] = useState("welcome");

  if (screen === "welcome") {
    return (
      <Welcome
        onStart={() => setScreen("testIntro")}
      />
    );
  }

  if (screen === "testIntro") {
    return (
      <TestIntro
        onStartTest={() => setScreen("wordTest")}
      />
    );
  }

  if (screen === "wordTest") {
    return (
      <WordTest
        onRecord={() => setScreen("recording")}
      />
    );
  }

 if (screen === "recording") {
  return (
    <Recording
      onFinish={() => setScreen("analysis")}
    />
  );
}
  if (screen === "analysis") {
  return (
    <Analysis
      onFinish={() => setScreen("result")}
    />
  );
}

if (screen === "result") {
  return <Result />;
}
}

export default App;