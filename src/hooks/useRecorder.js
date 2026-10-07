import { useEffect } from "react";

export function useRecorder({
  word,
  recordings,
  setRecordings,
  onFinish,
}) {
  useEffect(() => {
    let mediaRecorder;
    let chunks = [];

    const startRecording = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          audio: true,
        });

        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = (event) => {
          chunks.push(event.data);
        };

        mediaRecorder.onstop = async () => {
          const blob = new Blob(chunks, {
            type: "audio/webm",
          });

          setRecordings((prev) => [
            ...prev,
            {
              word,
              audio: blob,
            },
          ]);

          stream.getTracks().forEach((track) => track.stop());

          // Сразу переходим к анализу
          onFinish();

          // Отправляем аудио на backend
          const formData = new FormData();

          formData.append("user_id", "3");
          formData.append("word_index", "0");
          formData.append(
            "audio",
            blob,
            "recording.webm"
          );

          try {
            const response = await fetch(
              "http://127.0.0.1:8000/lesson/check",
              {
                method: "POST",
                body: formData,
              }
            );

            if (!response.ok) {
              throw new Error(
                `Backend error: ${response.status}`
              );
            }

            const result = await response.json();

            console.log("Ответ backend:", result);
          } catch (error) {
            console.error(
              "Ошибка отправки аудио:",
              error
            );
          }
        };

        mediaRecorder.start();

        setTimeout(() => {
          if (mediaRecorder.state === "recording") {
            mediaRecorder.stop();
          }
        }, 3000);

      } catch (error) {
        console.error("ОШИБКА ЗАПИСИ:", error);
        alert("Ошибка записи: " + error.message);
      }
    };

    startRecording();
  }, []);
}