# CPS - Copy Paste Share 🚀

[![Flask](https://img.shields.io/badge/Flask-2.0+-blue.svg)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-yellow.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)


## 👁️ View Live

[**Try it now!**](https://cps-online-clipboard.onrender.com) - Visit the live demo to start sharing instantly.
**CPS (Copy Paste Share)** is a lightweight, temporary online clipboard designed for quick and easy sharing of text, images, and files across different devices. No accounts, no history, just a one-time 6-character code to send your data in seconds.

## ✨ Features

- ✏️ **Text Sharing**: Paste messages, URLs, or code snippets instantly.
- 🖼️ **Image Support**: Upload and share screenshots or photos.
- 📁 **File Uploads**: Support for PDF, ZIP, and other common formats.
- 🕒 **Auto-Expiry**: All clips automatically expire and are deleted from the server after 24 hours.
- 🎨 **Modern UI**: Dark-themed, responsive interface with multiple themes (Student, Pro, Neon).
- 🔐 **Privacy Focused**: No sign-up required. Clips are stored temporarily in-memory or on disk with secure filenames.

## 🚀 How it Works

1. **Create**: Paste your text or upload a file.
2. **Share**: Tap "Share Clip" to generate a unique 6-character code (e.g., `A7B2X9`).
3. **Retrieve**: Type that code on any other device to load and download your content instantly.

## 🛠️ Tech Stack

- **Backend**: Python / Flask
- **Frontend**: HTML5, CSS3 (Modern Flexbox/Grid, Custom Themes), Vanilla JavaScript
- **Deployment**: Gunicorn / Heroku ready

## 📦 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/shreyas1405/cps-online-clipboard.git
   cd cps-online-clipboard
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```
   The app will be available at `http://127.0.0.1:5000`.

## 📂 Project Structure

- `app.py`: Main Flask application server.
- `templates/`: Contains `index.html` (Single-page frontend).
- `uploads/`: Temporary storage for uploaded files and images.
- `requirements.txt`: Python package dependencies.
- `Procfile` & `runtime.txt`: Configuration for Heroku deployment.

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
Built with ❤️ by [Shreyas](https://github.com/shreyas1405)
