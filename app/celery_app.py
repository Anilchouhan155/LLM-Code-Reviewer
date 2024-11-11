# Importing necessary tools
import os
from celery import Celery
from app.review_agent import analyze_pr  # This is where we analyze the code

broker = os.getenv("CELERY_BROKER_URL")

# Initialize Celery to use Redis as the task queue
celery_app = Celery('code_review', broker=broker)

@celery_app.task(bind=True)
def review_code_task(self, repo_url, pr_number, github_token):
    """
    This is the function that runs in the background.
    It calls the analyze_pr function to check the PR.
    """
    try:
        # Call the function that gets the code and checks it
        result = analyze_pr(repo_url, pr_number, github_token)
        return result
    except Exception as e:
        # If an error occurs, retry the task
        self.retry(exc=e)