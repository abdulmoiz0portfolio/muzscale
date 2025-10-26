# MuzScale Setup Guide

## Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/abdulmoiz0portfolio/muzscale.git
   cd muzscale
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up DeepAI API Key**
   
   Get your API key from [DeepAI](https://deepai.org/)
   
   Set it as an environment variable:
   ```bash
   # On Windows (Command Prompt):
   set DEEPAI_API_KEY=your_api_key_here
   
   # On Windows (PowerShell):
   $env:DEEPAI_API_KEY="your_api_key_here"
   
   # On macOS/Linux:
   export DEEPAI_API_KEY=your_api_key_here
   ```
   
   Or create a `.env` file in the project root:
   ```
   DEEPAI_API_KEY=your_api_key_here
   ```

## Running the Application

1. **Start the Flask server**
   ```bash
   python app.py
   ```

2. **Access the application**
   
   Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

1. Click on the upload area or drag and drop an image
2. Supported formats: PNG, JPG, JPEG, WEBP (max 16MB)
3. Click "Upscale Image" button
4. Wait for processing (may take 10-30 seconds)
5. Download the upscaled image

## Features

- **AI-Powered Upscaling**: Uses DeepAI's Waifu2x API for high-quality image enhancement
- **Drag & Drop Upload**: Easy file upload interface
- **Real-time Preview**: See your original image before processing
- **Automatic Cleanup**: Temporary files are automatically removed

## Troubleshooting

**Issue: API Error**
- Verify your DeepAI API key is correct
- Check your internet connection
- Ensure you haven't exceeded API rate limits

**Issue: File Upload Error**
- Check file size is under 16MB
- Verify file format is supported (PNG, JPG, JPEG, WEBP)

**Issue: Port Already in Use**
- Change the port in `app.py` from 5000 to another port
- Or kill the process using port 5000

## Project Structure

```
muzscale/
├── app.py              # Flask backend application
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html     # Frontend HTML interface
├── uploads/           # Temporary upload folder (auto-created)
├── outputs/           # Processed images folder (auto-created)
└── .gitignore         # Git ignore file
```

## API Endpoint

**POST /upscale**
- Upload image for upscaling
- Returns: JSON with success status and output filename

**GET /download/<filename>**
- Download upscaled image
- Returns: Image file

## Notes

- The application creates `uploads/` and `outputs/` folders automatically
- Uploaded files are deleted after processing
- Output files remain in the `outputs/` folder
- For production deployment, consider using a production WSGI server like Gunicorn
