// Adds a 'submit' event listener to the form with id 'uploadForm'
document.getElementById('uploadForm').addEventListener('submit', async function (e) {

  e.preventDefault(); 
  // Prevents the default form submission behavior (which would reload the page)

  const fileInput = document.getElementById('file');
  // Gets the file input element with id 'file'

  const file = fileInput.files[0];
  // Retrieves the first selected file from the input field

  const formData = new FormData();
  // Creates a new FormData object to send the file in a POST request

  formData.append('file', file);
  // Appends the selected file to the FormData object with the key 'file'

  try {
    const response = await fetch('http://127.0.0.1:5000/upload', {
      method: 'POST',
      body: formData
    });
    // Sends an asynchronous POST request to the backend Flask server with the form data

    const result = await response.json();
    // Waits for the server's JSON response and parses it

    if (result.error) {
      alert("Error: " + result.error);
      // If the response contains an error message, display it as an alert
      return;
      // Stop further execution
    }

    // Set image sources and prediction text
    document.getElementById('originalImage').src = `data:image/png;base64,${result.original_image}`;
    // Displays the original image by converting base64 string to an image source

    document.getElementById('predictedImage').src = `data:image/png;base64,${result.predicted_image}`;
    // Displays the predicted image using the base64 string from the response

    document.getElementById('predictionText').textContent = `Prediction: ${result.prediction}`;
    // Displays prediction result as text under the images or in a specific div/span

  } catch (error) {
    console.error("Upload failed:", error);
    // Logs any error that occurs during the fetch or processing

    alert("Something went wrong. Check console for details.");
    // Alerts the user that an unexpected error occurred
  }
});
