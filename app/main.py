# Importing necessary tools
import subprocess
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from celery.result import AsyncResult
import redis
from app.celery_app import celery_app, review_code_task
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()  # Create FastAPI app

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (or specify specific URLs)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

class AnalyzePRRequest(BaseModel):
    """This is a model that helps us make sure the data sent to the API is correct."""
    repo_url: str
    pr_number: int
    github_token: str = os.getenv("GITHUB_TOKEN")  # GitHub token is optional

@app.post("/analyze-pr")
async def analyze_pr(request: AnalyzePRRequest):
    """
    This endpoint starts the code review process.
    We send GitHub repo URL, PR number, and optionally a GitHub token.
    Celery will start checking the code in the background.
    """
    print(request.github_token, "#########-----")
    task = review_code_task.apply_async(args=[request.repo_url, request.pr_number, request.github_token])
    return {"task_id": task.id}  # We return the task ID so you can track it

@app.get("/status/{task_id}")
async def get_task_status(task_id: str):
    """
    This endpoint checks the status of the code review task.
    It will tell you if the task is pending, processing, or finished.
    """
    task_result = AsyncResult(task_id, app=celery_app)
    return {"task_id": task_id, "status": task_result.status}

@app.get("/results/{task_id}")
async def get_task_results(task_id: str):
    """
    This endpoint gets the result of the code review task once it is finished.
    It will give you details about the issues in the PR.
    """
    task_result = AsyncResult(task_id, app=celery_app)
    if task_result.status == 'SUCCESS':
        return task_result.result  # Return the result when it's ready
    else:
        raise HTTPException(status_code=400, detail="Task failed or is still processing")
    

# additional part 

# Check Redis connection
def check_redis():
    try:
        # Check if Redis is running on localhost:6379
        client = redis.StrictRedis(host='localhost', port=6379, db=0)
        client.ping()  # If Redis is running, this will return True
        print("yoooo")
        return True
    except redis.ConnectionError:
        return False

def check_celery():
    try:
        # Use 'ps aux' to list all running processes and search for 'celery' in the list
        result = subprocess.run(['ps', 'aux'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Check if 'celery' is found in the output
        if 'celery' in result.stdout:
            return True
        
        # Log output for debugging
        print("Celery worker is not running.")
        return False
    except Exception as e:
        # Print any errors in the exception
        print(f"Error occurred while checking Celery: {e}")
        return False

@app.get("/check-system-status")
async def check_system_status():
    # Check FastAPI app status
    fastapi_status = True  # This is always true since FastAPI is the current app
    
    # Check Redis status
    redis_status = check_redis()
    
    # Check Celery status
    celery_status = check_celery()

    # If any of the systems is down, return a failure status
    if not fastapi_status or not redis_status or not celery_status:
        return {"status": "System components are not connected properly"}

    return {"status": "connected"}