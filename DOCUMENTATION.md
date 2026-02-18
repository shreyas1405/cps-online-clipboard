# CPS Online Clipboard - Technical Documentation

## 1. Architecture Overview

CPS (Copy Paste Share) is a full-stack web application built using **Flask**. It operates as a temporary, volatile storage system for text and files, facilitating quick cross-device data transfers.

### 1.1 High-Level Architecture

The system consists of three main layers:
1. **Frontend**: A single-page application (SPA) style interface built with vanilla JavaScript
2. **Backend API**: A Flask-based RESTful API handling clip creation, retrieval, and file management
3. **Storage Layer**: 
   - In-Memory Storage: Text clips stored in a global Python dictionary
   - File System Storage: Images/files stored in `uploads/` directory with secure filenames

## 2. System Components

### 2.1 Core Modules

- **`app.py`**: Central Flask application managing routing, API logic, and TTL cleanup
- **`templates/index.html`**: Single-page frontend with CSS (3 themes) and vanilla JavaScript
- **Storage Management**: 24-hour TTL (Time-To-Live) with automatic expiration

### 2.2 ID Generation

6-character alphanumeric ID using character set `ABCDEFGHJKLMNPQRSTUVWXYZ23456789` (excludes ambiguous chars: 0, O, 1, I)

## 3. File Handling & Security

- **Filename Security**: All files processed through `werkzeug.utils.secure_filename`
- **Uniqueness**: Files prefixed with clip ID on disk (e.g., `A7B2X9_image.jpg`)
- **Cleanup Process**: Runs on every API request; removes expired clips from memory and disk

## 4. API Endpoints

### Create Clip
- **URL**: `/api/clipboard`
- **Method**: `POST`
- **Payload**: `multipart/form-data` with `type` (text/image/file) + content
- **Response**: `{"id": "XXXXXX", "type": "text", "filename": "optional"}`

### Retrieve Clip
- **URL**: `/api/clipboard/<cid>`
- **Method**: `GET`
- **Response**: Returns JSON with text content or download URL for files

### Download File
- **URL**: `/download/<cid>`
- **Method**: `GET`
- **Response**: Serves file with original filename

## 5. Frontend Features

- **Mode Switching**: Text, Image, File upload modes
- **Theme Support**: Student (default), Pro, Neon themes
- **Real-Time UI**: Dynamic textarea/upload zone based on mode
- **Clipboard Integration**: Copy generated codes and retrieved text
- **Toast Notifications**: Visual feedback for user actions

## 6. Security & Performance

- **HTTPS Ready**: Designed for encrypted transit
- **Volatile Storage**: Minimal data persistence reduces exposure risk
- **No Accounts**: Zero authentication overhead
- **Sequential Processing**: Hosts pinged one-by-one for deterministic behavior

## 7. Deployment

- **Gunicorn Ready**: See `Procfile` and `runtime.txt`
- **Heroku Compatible**: Python 3.9+ required
- **Environment**: Flask development or production mode

## 8. Future Enhancements

- [ ] Password-protected clips
- [ ] End-to-End Encryption (E2EE)
- [ ] QR Code generation
- [ ] Persistent database (Redis/SQL)
- [ ] Rate limiting
- [ ] Analytics
