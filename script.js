const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const frame = document.getElementById('frame');
const snapBtn = document.getElementById('snap');
const downloadBtn = document.getElementById('download');
const retakeBtn = document.getElementById('retake');

// Start video stream
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    video.srcObject = stream;
  })
  .catch(err => {
    console.error("Error accessing webcam:", err);
  });

// Capture photo
snapBtn.addEventListener('click', () => {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Mirror image
  ctx.save();
  ctx.translate(canvas.width, 0);
  ctx.scale(-1, 1);
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  ctx.restore();

  const frameImg = new Image();
  frameImg.crossOrigin = "anonymous";
  frameImg.onload = () => {
    ctx.drawImage(frameImg, 0, 0, canvas.width, canvas.height);

    // Kirim ke server
    canvas.toBlob(blob => {
      const formData = new FormData();
      formData.append("file", blob, "photo.png"); // Nama bebas

     fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        body: formData
      })
      .then(res => res.json())
      .then(data => {
        console.log("Uploaded:", data);
      })
      .catch(error => {
        console.error("Upload failed:", error);
      });
    }, "image/png");

    canvas.style.display = 'block';
    video.style.display = 'none';
    frame.style.display = 'none';
    snapBtn.style.display = 'none';
    retakeBtn.style.display = 'inline-block';
  };
  frameImg.src = frame.src;
});

// Download photo
downloadBtn.addEventListener('click', () => {
  const link = document.createElement('a');
  link.download = 'photo_booth.png';
  link.href = canvas.toDataURL('image/png');
  link.click();
});

// Retake photo
retakeBtn.addEventListener('click', () => {
  canvas.style.display = 'none';
  video.style.display = 'block';
  snapBtn.style.display = 'inline-block';
  retakeBtn.style.display = 'none';
});
