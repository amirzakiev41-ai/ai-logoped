
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
        console.log("Начинаем запись:", word);

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
          const blob = new Blob(chunks, {
            type: mediaRecorder.mimeType || "audio/webm",
          });

          console.log("Запись завершена");
          console.log("Формат аудио:", blob.type);
          console.log("Размер аудио:", blob.size, "байт");

          if (blob.size === 0) {
            console.error("Запись пустая");
            alert("Не удалось записать звук. Попробуй ещё раз.");
            stream?.getTracks().forEach((track) => track.stop());
            return;
          }

          try {
            const formData = new FormData();
            formData.append("user_id", String(userId));
            formData.append("word_index", String(wordIndex));
            formData.append("audio", blob, "recording.webm");

            console.log("Отправляем аудио на backend...");
            const requestStart = performance.now();

            const response = await fetch(
              "http://127.0.0.1:8000/lesson/check",
              {
                method: "POST",
                body: formData,
              }
            );

            const responseTime =
              (performance.now() - requestStart) / 1000;

            console.log(
              `Время ответа backend: ${responseTime.toFixed(2)} сек.`
            );

            const responseText = await response.text();

            console.log("HTTP статус:", response.status);
            console.log("Ответ backend:", responseText);

            if (!response.ok) {
              throw new Error(
                `Backend вернул ошибку ${response.status}: ${responseText}`
              );
            }

            const result = JSON.parse(responseText);

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
              alert(
                "Не удалось проанализировать речь. " +
                  "Открой консоль браузера и терминал backend."
              );
            }
          } finally {
            stream?.getTracks().forEach((track) => track.stop());
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

        stream?.getTracks().forEach((track) => track.stop());
      }
    }

    startRecording();

    return () => {
      cancelled = true;
      clearTimeout(timeoutId);

      if (mediaRecorder?.state === "recording") {
        mediaRecorder.stop();
      } else {
        stream?.getTracks().forEach((track) => track.stop());
      }
    };
  }, [
    word,
    wordIndex,
    userId,
    setRecordings,
    onFinish,
  ]);
}

