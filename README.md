# 🛡️ Nmap AI Security Scanner

A modern web application that combines network scanning with AI-powered vulnerability analysis.

## 🌟 Features

- **Advanced Network Scanning**: Optimized Nmap integration for fast, accurate scans
- **AI-Powered Analysis**: Groq AI provides professional security analysis
- **Modern Web Interface**: Clean, responsive React frontend
- **Real-time Results**: Live scanning progress and formatted results
- **Multiple Scan Options**: Quick scans, custom targets, and analysis modes

## 🏛️ Architecture

```
Frontend (React + Material-UI)  ←→  Backend (FastAPI + Nmap + Groq AI)
     Port 3000                           Port 8000
```

## 📋 Prerequisites

1. **Python 3.12+** installed
2. **Node.js 16+** and npm installed
3. **Nmap** installed and available in PATH
4. **Groq API Key** (free from https://console.groq.com/keys)

## 🚀 Quick Start

### 1. Clone and Setup Backend
```bash
# Navigate to the project directory
cd SensAI-main

# Install Python dependencies
pip install fastapi uvicorn python-dotenv groq

# Ensure .env file has your Groq API key
echo "GROQ_API_KEY=your_api_key_here" > .env
```

### 2. Setup Frontend
```bash
# Frontend is already set up in nmap-scanner-frontend/
cd nmap-scanner-frontend
npm install  # (already done during creation)
```

### 3. Start the Application

**Option 1: Using Batch Files (Windows)**
```bash
# Terminal 1 - Start Backend
start-backend.bat

# Terminal 2 - Start Frontend  
start-frontend.bat
```

**Option 2: Manual Commands**
```bash
# Terminal 1 - Backend
python -m uvicorn nmap_AI:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2 - Frontend
cd nmap-scanner-frontend
npm start
```

### 4. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🎯 Usage

### Web Interface
1. Open http://localhost:3000 in your browser
2. Enter a target (IP address or domain)
3. Choose scan type:
   - **Basic Scan**: Nmap results only
   - **Scan + AI Analysis**: Includes vulnerability analysis
   - **Quick Scan**: Fast scan of scanme.nmap.org
   - **Quick Analysis**: Fast scan + AI analysis

### API Endpoints
- `GET /quick-scan` - Quick scan of default target
- `GET /quick-analyze` - Quick scan + AI analysis
- `GET /scan/{target}` - Scan specific target
- `GET /analyze/{target}` - Scan + analyze specific target
- `POST /scan` - Scan with JSON payload
- `POST /analyze` - Scan + analyze with JSON payload

## 🔧 Configuration

### Backend Settings
- **Default Target**: `scanme.nmap.org` (safe for testing)
- **Scan Timeout**: 2 minutes
- **Nmap Options**: `-sV -Pn -T5` (optimized for speed)

### Frontend Settings
- **API Base URL**: `http://localhost:8000`
- **Material-UI Theme**: Professional blue/purple gradient
- **Responsive Design**: Works on desktop and mobile

## 📊 Example Output

### Scan Results
```
Starting Nmap 7.97 ( https://nmap.org ) at 2025-07-28 20:57 +0530
Nmap scan report for scanme.nmap.org (45.33.32.156)
Host is up (0.28s latency).
Not shown: 996 closed tcp ports (reset)
PORT     STATE SERVICE    VERSION
22/tcp   open  ssh        OpenSSH 6.6.1p1
80/tcp   open  http       Apache httpd 2.4.7
443/tcp  open  https      Apache httpd 2.4.7
```

### AI Analysis
```
## Security Analysis Report

### 🔍 Open Ports & Services
- Port 22/tcp: SSH (OpenSSH 6.6.1p1)
- Port 80/tcp: HTTP (Apache 2.4.7)
- Port 443/tcp: HTTPS (Apache 2.4.7)

### ⚠️ Potential Vulnerabilities
- Outdated OpenSSH version may have known CVEs
- Apache 2.4.7 is outdated and potentially vulnerable

### 🔧 Recommendations
- Update OpenSSH to latest version
- Upgrade Apache to current stable release
- Implement proper firewall rules

### 📊 Risk Assessment
Medium - Several outdated services detected
```

## 🛠️ Troubleshooting

### Common Issues

1. **"Failed to connect to API server"**
   - Ensure backend is running on port 8000
   - Check CORS settings in nmap_AI.py

2. **"Nmap command not found"**
   - Install Nmap and add to PATH
   - Test with `nmap --version`

3. **"Failed to analyze"**
   - Check Groq API key in .env file
   - Verify internet connection

4. **Slow scans**
   - Normal for network scans (30s-2min)
   - Use Quick Scan for faster results

## 🔒 Security Notes

- Always get permission before scanning networks
- Use `scanme.nmap.org` for testing (officially sanctioned)
- Don't scan production systems without authorization
- Keep API keys secure and private

## 📁 Project Structure

```
SensAI-main/
├── nmap_AI.py              # FastAPI backend
├── .env                    # Environment variables
├── start-backend.bat       # Backend startup script
├── start-frontend.bat      # Frontend startup script
├── README.md              # This file
└── nmap-scanner-frontend/ # React frontend
    ├── src/
    │   ├── App.js         # Main React component
    │   ├── App.css        # Custom styles
    │   └── index.js       # React entry point
    └── package.json       # Frontend dependencies
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is for educational and authorized security testing purposes only.

---

**Made with ❤️ using React, FastAPI, Nmap, and Groq AI**
