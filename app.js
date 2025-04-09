const express = require("express");
const multer = require("multer");
const path = require("path");
const cors = require("cors");
app.use(cors());

const app = express();
const port = 3000;

app.use(cors());
app.use(express.json());
app.use(express.static("public")); // Serve static files

// Configure Multer for file uploads
const storage = multer.diskStorage({
    destination: "uploads/",
    filename: (req, file, cb) => {
        cb(null, "uploaded_" + Date.now() + path.extname(file.originalname));
    },
});
const upload = multer({ storage: storage });

// Test route to ensure server is running
app.get("/", (req, res) => {
    res.send("Landslide Prediction Server is Running");
});

// Handle file upload and prediction
app.post("/predict", upload.single("file"), async (req, res) => {
    console.log("Predict route hit");

    if (!req.file) {
        return res.status(400).json({ error: "No file uploaded" });
    }

    try {
        // Simulating prediction and generating image URL
        const predictedImageUrl = `/uploads/predicted_${req.file.filename}.png`;

        // Send response with predicted image URL
        res.json({ imageUrl: predictedImageUrl });
    } catch (error) {
        console.error("Prediction Error:", error);
        res.status(500).json({ error: "Internal Server Error" });
    }
});

// Start server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
