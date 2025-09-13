# JOB BUDDY

Setup Instructions

Create Environment:
conda create --name genai
conda activate genai

Install Required Packages:
python3 -m pip install -r requirements.txt

Run FastAPI app:
uvicorn api:app --reload --port 8000

