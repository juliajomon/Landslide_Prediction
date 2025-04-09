document.getElementById("predict-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  console.log("Submitting form...");

  const fileInput = document.querySelector('input[type="file"]');
  if (!fileInput.files.length) {
      alert("Please select a file.");
      return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  try {
      const response = await fetch("http://localhost:3000/predict", {  // UPDATED URL
          method: "POST",
          body: formData,
      });

      console.log("Server response:", response);

      if (!response.ok) {
          throw new Error("Prediction failed.");
      }

      const data = await response.json();
      document.getElementById("predictedImage").src = data.imageUrl;
  } catch (error) {
      console.error("Error during fetch:", error);
      alert("An error occurred while predicting.");
  }
});
