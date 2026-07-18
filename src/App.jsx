import { useState } from "react";
import Welcome from "./pages/Welcome";
import TestIntro from "./pages/TestIntro";
import WordTest from "./pages/WordTest";
import Recording from "./pages/Recording";
import Analysis from "./pages/Analysis";
import Result from "./pages/Result";
import { useApp } from "./context/AppContext";

function App() {
  
  const [screen, setScreen] = useState("welcome");
  const {
  words,
  wordIndex,
  setWordIndex,
  recordings,
  setRecordings,
} = useApp();
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
      word={words[wordIndex]}
      current={wordIndex + 1}
      total={words.length}
      onRecord={() => setScreen("recording")}
    />
  );
}

 if (screen === "recording") {
  return (
   <Recording
      word={words[wordIndex]}
      recordings={recordings}
      setRecordings={setRecordings}
      onFinish={() => setScreen("analysis")}
/>
  );
}
 if (screen === "analysis") {
  return (
    <Analysis
      onFinish={() => {
        if (wordIndex < words.length - 1) {
          setWordIndex(wordIndex + 1);
          setScreen("wordTest");
        } else {
          setScreen("result");
        }
      }}
    />
  );
}

if (screen === "result") {
  return (
    <Result
      recordings={recordings}
    />
  );
}

}

export default App;