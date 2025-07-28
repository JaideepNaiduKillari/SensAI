from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import os
from dotenv import load_dotenv
from groq import Groq
from typing import Optional


DEFAULT_TARGET = "scanme.nmap.org"

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Step 1: Run Nmap (optimized for better performance)
def run_nmap(target=None):
    if target is None:
        target = DEFAULT_TARGET
    
    print(f"Running Nmap on {target}...")
    try:
        # Optimized nmap command with -Pn to skip host discovery
        # This fixes the "Host seems down" issue
        result = subprocess.run([
            "nmap", "-sV", "-Pn", "-T5", "--max-rtt-timeout", "500ms",
            "--max-retries", "1", "--host-timeout", "60s", target
        ], capture_output=True, text=True, timeout=120)  # 2 minute timeout
        return result.stdout
    except subprocess.TimeoutExpired:
        return f"Scan of {target} timed out after 2 minutes"
    except Exception as e:
        return f"Scan of {target} failed: {e}"

# Step 2: Analyze with Groq (llama-3.3-70b-versatile)
def analyze_with_groq(scan_output):
    print("Sending scan output to Groq...")
    
    # Check if we have a valid API key
    if not GROQ_API_KEY:
        print("Error: GROQ_API_KEY not found in environment variables")
        return "Error: GROQ_API_KEY not configured. Please set your Groq API key in a .env file."
    
    # Check if client is properly initialized
    if not client:
        print("Error: Groq client not initialized")
        return "Error: Groq client not initialized properly."
    
    try:
        print(f"Using API key: {GROQ_API_KEY[:10]}...")
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a cybersecurity expert. Analyze the following Nmap scan output and provide a clean, professional security analysis. Format your response as follows:\n\n## Security Analysis Report\n\n### 🔍 Open Ports & Services\nList each open port with its service and version (if available)\n\n### ⚠️ Potential Vulnerabilities\nIdentify security concerns based on the scan results\n\n### 🔧 Recommendations\nProvide actionable security recommendations\n\n### 📊 Risk Assessment\nBrief overall risk level (Low/Medium/High)\n\nUse clear, professional language without excessive markdown formatting. Focus on actionable insights."
                },
                {
                    "role": "user",
                    "content": scan_output
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.1,
            max_tokens=1000
        )
        
        print("Groq API call successful!")
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Detailed error during Groq API call: {type(e).__name__}: {str(e)}")
        return f"Failed to analyze: {type(e).__name__}: {str(e)}"

# FastAPI setup
app = FastAPI(
    title="Nmap AI Security Scanner",
    description="An API that runs Nmap scans and analyzes results using AI",
    version="1.0.0"
)

# Add CORS middleware to allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScanRequest(BaseModel):
    target: str

@app.get("/")
async def root():
    return {
        "message": "Welcome to Nmap AI Security Scanner",
        "default_target": DEFAULT_TARGET,
        "endpoints": {
            "/docs": "Interactive API documentation",
            "/scan": "POST - Run Nmap scan on target",
            "/analyze": "POST - Run Nmap scan and analyze with AI",
            "/scan/{target}": "GET - Run Nmap scan on target (simple)",
            "/analyze/{target}": "GET - Run Nmap scan and analyze with AI (simple)",
            "/quick-scan": "GET - Run Nmap scan on default target (scanme.nmap.org)",
            "/quick-analyze": "GET - Run Nmap scan and AI analysis on default target"
        }
    }

@app.post("/scan")
async def scan_post(scan_request: ScanRequest):
    try:
        target = scan_request.target
        output = run_nmap(target)
        return {"target": target, "scan_result": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/scan/{target}")
async def scan_get(target: str):
    try:
        output = run_nmap(target)
        return {"target": target, "scan_result": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze")
async def analyze_post(scan_request: ScanRequest):
    try:
        target = scan_request.target
        output = run_nmap(target)
        analysis = analyze_with_groq(output)
        return {"target": target, "scan_result": output, "analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analyze/{target}")
async def analyze_get(target: str):
    try:
        output = run_nmap(target)
        analysis = analyze_with_groq(output)
        return {"target": target, "scan_result": output, "analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Quick endpoints using default target (scanme.nmap.org)
@app.get("/quick-scan")
async def quick_scan():
    """Run a quick scan on the default target (scanme.nmap.org)"""
    try:
        output = run_nmap()  # Uses default target
        return {"target": DEFAULT_TARGET, "scan_result": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/quick-analyze")
async def quick_analyze():
    """Run a quick scan and AI analysis on the default target (scanme.nmap.org)"""
    try:
        output = run_nmap()  # Uses default target
        analysis = analyze_with_groq(output)
        return {"target": DEFAULT_TARGET, "scan_result": output, "analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

