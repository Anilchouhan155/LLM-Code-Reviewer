# review_classes.py

import re
from github import Github
from langchain.prompts import PromptTemplate
from langchain.schema import AIMessage
from .templates import PR_SUMMARY_TEMPLATE, CODE_REVIEW_TEMPLATE
import json

class PullRequestRetriever:
    def __init__(self, github_token: str, repo_name: str, pr_number: int):
        self.github = Github(github_token)
        self.repo_name = repo_name
        self.pr_number = pr_number
        self.repo = self.github.get_repo(repo_name)

    def get_pull_request(self):
        """Fetch pull request details."""
        return self.repo.get_pull(self.pr_number)

    def get_files_content(self):
        """Retrieve the full content of each file in the pull request."""
        pr = self.get_pull_request()
        files_content = []
        for file in pr.get_files():
            file_content = self.repo.get_contents(file.filename).decoded_content.decode("utf-8")
            files_content.append({"name": file.filename, "content": file_content})
        return files_content


class PRSummaryChain:
    def __init__(self, llm):
        self.sequence = PromptTemplate(input_variables=["pr_description"], template=PR_SUMMARY_TEMPLATE) | llm

    def summarize(self, pull_request):
        pr_description = pull_request.body or "No description provided."
        response = self.sequence.invoke({"pr_description": pr_description})

        if isinstance(response, AIMessage):
            response = response.content

        return response


class CodeReviewChain:
    def __init__(self, llm):
        self.sequence = PromptTemplate(input_variables=["code"], template=CODE_REVIEW_TEMPLATE) | llm

    def review_file(self, file_content):
        """Perform code review on the entire content of a file."""
        response = self.sequence.invoke({"code": file_content})

        # Ensure response is accessed as text
        if isinstance(response, AIMessage):
            response = response.content

        print("Received at line 57:", response)
        # Check for multiple JSON-like objects and parse them individually
        issues = []
        try:
            # Use regex to extract each JSON-like block
            json_objects = re.findall(r'\{.*?\}', response, re.DOTALL)
            for obj in json_objects:
                try:
                    # Parse each JSON object and append to issues list
                    parsed_issue = json.loads(obj)
                    if isinstance(parsed_issue, dict):
                        issues.append(parsed_issue)
                except json.JSONDecodeError:
                    print("Warning: Could not decode a part of the response as JSON. Part:", obj)
                    
        except Exception as e:
            print(f"Error: Could not process response. {e}")
            print("Received:", response)
        
        return issues
        
    def review_pull_request(self, files_content):
        """Perform code review on all files in the pull request."""
        reviews = []
        for file in files_content:
            file_review = {
                "name": file["name"],
                "issues": self.review_file(file["content"])  # Review each file's entire content
            }
            reviews.append(file_review)
        return reviews


class PullRequestReporter:
    def __init__(self, task_id, pr_summary, code_reviews):
        self.task_id = task_id
        self.pr_summary = pr_summary
        self.code_reviews = code_reviews

    def generate_report(self):
        """Generate a report in the required JSON format."""
        # Debugging output to verify structure
        print("Debug: Code Reviews Structure", self.code_reviews)

        total_issues = sum(len(file["issues"]) for file in self.code_reviews if isinstance(file["issues"], list))
        critical_issues = sum(
            1 for file in self.code_reviews if isinstance(file["issues"], list) 
            for issue in file["issues"] if isinstance(issue, dict) and issue.get("type") == "bug"
        )

        report = {
            "task_id": self.task_id,
            "status": "completed",
            "results": {
                "files": self.code_reviews,
                "summary": {
                    "total_files": len(self.code_reviews),
                    "total_issues": total_issues,
                    "critical_issues": critical_issues,
                }
            }
        }
        return report