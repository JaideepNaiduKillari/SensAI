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

# Main execution
if __name__ == "__main__":
    target = input("Enter IP or domain to scan: ")
    output = run_nmap(target)
    print("\n=== Nmap Scan Result ===\n")
    print(output)
    print("\n=== Groq Analysis ===\n")
    analysis = analyze_with_groq(output)
    print(analysis)
