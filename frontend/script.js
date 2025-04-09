document.getElementById('uploadForm').addEventListener('submit', async function (e) {
  e.preventDefault();

  const fileInput = document.getElementById('file');
  const file = fileInput.files[0];
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch('http://127.0.0.1:5000/upload', {
      method: 'POST',
      body: formData
    });

    const result = await response.json();

    if (result.error) {
      alert("Error: " + result.error);
      return;
    }

    // Set image sources and prediction text
    document.getElementById('originalImage').src = `data:image/png;base64,${result.original_image}`;
    document.getElementById('predictedImage').src = `data:image/png;base64,${result.predicted_image}`;
    document.getElementById('predictionText').textContent = `Prediction: ${result.prediction}`;

  } catch (error) {
    console.error("Upload failed:", error);
    alert("Something went wrong. Check console for details.");
  }
});
