import { createContext, useContext, useState } from "react";

const AppContext = createContext();

export function AppProvider({ children }) {
  const words = [
    "РЫБА",
    "РАК",
    "ШАР",
    "ЖУК",
    "ЛАМПА",
  ];

  const [recordings, setRecordings] = useState([]);
  const [wordIndex, setWordIndex] = useState(0);

  return (
    <AppContext.Provider
      value={{
        words,
        recordings,
        setRecordings,
        wordIndex,
        setWordIndex,
      }}
    >
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  return useContext(AppContext);
}