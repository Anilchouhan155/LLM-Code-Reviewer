import json
import os
from langchain.chat_models import ChatOpenAI
from .review_classes import PullRequestRetriever, PRSummaryChain, CodeReviewChain, PullRequestReporter

def analyze_pr(repo_url: str, pr_number: int, github_token: str = None, task_id: str = "abc123"):
    """
    This function fetches code from GitHub PR and analyzes it using LangChain.
    It returns the feedback and stores the results in a structured format.

    Parameters:
        repo_url (str): GitHub repo URL.
        pr_number (int): PR number to fetch and analyze.
        github_token (str, optional): GitHub token for accessing private repos.
        task_id (str): Task ID to track results.

    Returns:
        dict: Analysis results with categorized issues.
    """
    # Parse repo owner and name from URL
    repo_parts = repo_url.rstrip('/').split('/')
    repo_owner = repo_parts[-2]
    repo_name = repo_parts[-1]

    # Initialize the Language Model with OpenAI API key
    openai_api_key = os.getenv("OPENAI_API_KEY")  # Replace with actual key or retrieve from env
    llm = ChatOpenAI(api_key=openai_api_key)

    # Step 1: Retrieve PR data with full file content
    retriever = PullRequestRetriever(github_token, f"{repo_owner}/{repo_name}", pr_number)
    pull_request = retriever.get_pull_request()
    files_content = retriever.get_files_content()  # Retrieve full file content

    # Step 2: Summarize the PR
    pr_summary_chain = PRSummaryChain(llm)
    pr_summary = pr_summary_chain.summarize(pull_request)

    # Step 3: Review the code in each file
    code_review_chain = CodeReviewChain(llm)
    code_reviews = code_review_chain.review_pull_request(files_content)

    # Step 4: Generate a structured JSON report
    reporter = PullRequestReporter(task_id, pr_summary, code_reviews)
    result = reporter.generate_report()

    # Return the result as JSON
    return json.dumps(result, indent=4)