# MuzScale

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.2-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

**AI-based Image Upscaling Website using Real-ESRGAN or similar API**

MuzScale is a web application that uses advanced AI algorithms to upscale and enhance images. Built with Flask and powered by DeepAI's image upscaling API, this tool provides professional-quality image enhancement through an intuitive web interface.

## ✨ Features

- 🖼️ **AI-Powered Upscaling**: Uses Real-ESRGAN via DeepAI API for high-quality image enhancement
- 📤 **Easy Upload**: Simple drag-and-drop or click-to-upload interface
- ⚡ **Fast Processing**: Quick image processing with real-time feedback
- 🎨 **Quality Enhancement**: Improves image resolution and quality
- 🌐 **Web-Based**: No installation required, accessible from any browser

## 🚀 Deployment

### Important: GitHub Pages Limitation

**This application cannot be deployed directly on GitHub Pages** because:
- It's a Flask application (Python backend)
- It requires server-side processing
- It needs to handle API calls to DeepAI
- GitHub Pages only supports static HTML/CSS/JavaScript

### Recommended Deployment Platforms

To deploy MuzScale with a GitHub-linked domain, use one of these platforms:

1. **[Render](https://render.com)** (Recommended)
   - Free tier available
   - Automatic GitHub integration
   - Your app will be at: `https://muzscale.onrender.com`

2. **[Railway](https://railway.app)**
   - Simple deployment
   - GitHub integration
   - Your app will be at: `https://muzscale.up.railway.app`

3. **[Heroku](https://heroku.com)**
   - Popular platform
   - Free tier available
   - Your app will be at: `https://muzscale.herokuapp.com`

4. **[PythonAnywhere](https://www.pythonanywhere.com)**
   - Python-focused hosting
   - Easy setup

### 📖 Complete Deployment Guide

**For detailed step-by-step deployment instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md)**

The deployment guide includes:
- ✅ Detailed steps for each platform
- ✅ Environment variable configuration
- ✅ DeepAI API setup instructions
- ✅ Troubleshooting tips
- ✅ How to link your deployment to this GitHub repository
- ✅ Alternative approaches (static frontend + serverless backend)

## 🛠️ Local Development

For local development and testing, see [SETUP.md](./SETUP.md) for complete installation instructions.

### Quick Start

```bash
# Clone the repository
git clone https://github.com/abdulmoiz0portfolio/muzscale.git
cd muzscale

# Install dependencies
pip install -r requirements.txt

# Set your DeepAI API key
export DEEPAI_API_KEY="your_api_key_here"

# Run the application
python app.py
```

Visit `http://localhost:5000` in your browser.

## 📋 Requirements

- Python 3.8+
- Flask 2.3.2
- Werkzeug 2.3.6
- Requests 2.31.0
- DeepAI API key (get from [DeepAI Dashboard](https://deepai.org/dashboard/profile))

## 🔑 API Setup

1. Sign up at [DeepAI](https://deepai.org)
2. Get your API key from the [Dashboard](https://deepai.org/dashboard/profile)
3. Set the environment variable:
   ```bash
   export DEEPAI_API_KEY="your_api_key_here"
   ```

## 📁 Project Structure

```
muzscale/
├── app.py              # Main Flask application
├── templates/          # HTML templates
│   └── index.html      # Main UI
├── requirements.txt    # Python dependencies
├── SETUP.md           # Local setup instructions
├── DEPLOYMENT.md      # Deployment guide
└── README.md          # This file
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 🔗 Links

- **Documentation**: [SETUP.md](./SETUP.md) | [DEPLOYMENT.md](./DEPLOYMENT.md)
- **API Provider**: [DeepAI](https://deepai.org)
- **Repository**: [github.com/abdulmoiz0portfolio/muzscale](https://github.com/abdulmoiz0portfolio/muzscale)

## 📬 Contact

For questions or suggestions, please open an issue in this repository.

---

**Note**: To showcase this project in your portfolio with a live demo link, follow the deployment instructions in [DEPLOYMENT.md](./DEPLOYMENT.md). Once deployed, you can link the live application URL back to this GitHub repository.
