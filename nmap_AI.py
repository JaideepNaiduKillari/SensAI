from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import os
from dotenv import load_dotenv
from groq import Groq

# Load API Key from .env file
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Step 1: Run Nmap
def run_nmap(target):
    print(f"Running Nmap on {target}...")
    result = subprocess.run(["nmap", "-sV", target], capture_output=True, text=True)
    return result.stdout

# Step 2: Analyze with Groq (llama-3.3-70b-versatile)
def analyze_with_groq(scan_output):
    print("Sending scan output to Groq...")

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a cybersecurity expert. Analyze the following Nmap scan output and identify potential vulnerabilities, open ports, and recommend remediation."
                },
                {
                    "role": "user",
                    "content": scan_output
                }
            ],
            model="llama-3.3-70b-versatile",
        )

        return chat_completion.choices[0].message.content
    except Exception as e:
        print("Error during Groq API call:", e)
        return "Failed to analyze."

# FastAPI setup
app = FastAPI(
    title="Nmap AI Security Scanner",
    description="An API that runs Nmap scans and analyzes results using AI",
    version="1.0.0"
)

class ScanRequest(BaseModel):
    target: str

@app.get("/")
async def root():
    return {
        "message": "Welcome to Nmap AI Security Scanner",
        "endpoints": {
            "/docs": "Interactive API documentation",
            "/scan": "POST - Run Nmap scan on target",
            "/analyze": "POST - Run Nmap scan and analyze with AI",
            "/scan/{target}": "GET - Run Nmap scan on target (simple)",
            "/analyze/{target}": "GET - Run Nmap scan and analyze with AI (simple)"
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
