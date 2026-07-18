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

        mediaRecorder.onstop = () => {
          const blob = new Blob(chunks, {
            type: "audio/webm",
          });

          setRecordings([
            ...recordings,
            {
              word,
              audio: blob,
            },
          ]);

          stream.getTracks().forEach((track) =>
            track.stop()
          );

          onFinish();
        };

        mediaRecorder.start();

        setTimeout(() => {
          mediaRecorder.stop();
        }, 3000);

      } catch (error) {
        console.error(error);
        alert("Ошибка записи");
      }
    };

    startRecording();

  }, []);
}