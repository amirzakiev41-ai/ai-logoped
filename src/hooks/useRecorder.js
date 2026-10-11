
import { useEffect } from "react";

export function useRecorder({
  word,
  wordIndex,
  userId,
  recordings,
  setRecordings,
  onFinish,
}) {
  useEffect(() => {
    let mediaRecorder;
    let stream;
    let timeoutId;
    let cancelled = false;
    const chunks = [];

    async function startRecording() {
      try {
        stream = await navigator.mediaDevices.getUserMedia({
          audio: true,
        });

        if (cancelled) {
          stream.getTracks().forEach((track) => track.stop());
          return;
        }

        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = (event) => {
          if (event.data.size > 0) {
            chunks.push(event.data);
          }
        };

        mediaRecorder.onstop = async () => {
          try {
            const blob = new Blob(chunks, {
              type: mediaRecorder.mimeType || "audio/webm",
            });

            const formData = new FormData();
            formData.append("user_id", String(userId));
            formData.append("word_index", String(wordIndex));
            formData.append("audio", blob, "recording.webm");

            const response = await fetch(
              "http://127.0.0.1:8000/lesson/check",
              {
                method: "POST",
                body: formData,
              }
            );

            if (!response.ok) {
              throw new Error(
                `Backend вернул ошибку ${response.status}: ${await response.text()}`
              );
            }

            const result = await response.json();

            console.log("Ответ backend:", result);

            setRecordings((prev) => [
              ...prev,
              {
                word,
                audio: blob,
                result,
              },
            ]);

            if (!cancelled) {
              onFinish();
            }
          } catch (error) {
            console.error("Ошибка отправки или анализа аудио:", error);
            if (!cancelled) {
              alert("Не удалось проанализировать речь. Подробности — в консоли.");
            }
          } finally {
            if (stream) {
              stream.getTracks().forEach((track) => track.stop());
            }
          }
        };

        mediaRecorder.start();

        timeoutId = setTimeout(() => {
          if (mediaRecorder?.state === "recording") {
            mediaRecorder.stop();
          }
        }, 3000);
      } catch (error) {
        console.error("Ошибка записи:", error);

        if (!cancelled) {
          alert("Не удалось начать запись: " + error.message);
        }

        if (stream) {
          stream.getTracks().forEach((track) => track.stop());
        }
      }
    }

    startRecording();

    return () => {
      cancelled = true;
      clearTimeout(timeoutId);

      if (mediaRecorder?.state === "recording") {
        mediaRecorder.stop();
      } else if (stream) {
        stream.getTracks().forEach((track) => track.stop());
      }
    };
  }, [word, wordIndex, userId, setRecordings, onFinish]);
}