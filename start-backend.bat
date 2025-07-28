@echo off
echo Starting Nmap AI Security Scanner Backend...
echo Server will be available at http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo Make sure you have:
echo - Nmap installed and in PATH
echo - GROQ_API_KEY in .env file
echo.
python -m uvicorn nmap_AI:app --host 0.0.0.0 --port 8000 --reload
pause
