let mediaRecorder;
let recordedBlobs;

const mimeType = 'audio/webm';

document.querySelector('#start').addEventListener('click', async () => {
  const stream = await navigator.mediaDevices.getUserMedia({audio: true}); // Change here
  mediaRecorder = new MediaRecorder(stream);

  mediaRecorder.onstop = (event) => {
    const blob = new Blob(recordedBlobs, {type: mimeType});
    const formData = new FormData();
    formData.append('audio', blob);
    fetch('http://127.0.0.1:8080/upload_audio', {
      method: 'POST', // Change here
      body: formData
    });
  };

  recordedBlobs = [];
  mediaRecorder.ondataavailable = (event) => {
    if (event.data.size > 0) {
      recordedBlobs.push(event.data);
    } 
  };

  mediaRecorder.start();
});

document.querySelector('#stop').addEventListener('click', () => {
  mediaRecorder.stop();
});