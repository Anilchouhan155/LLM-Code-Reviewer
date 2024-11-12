# Template for summarizing a pull request
PR_SUMMARY_TEMPLATE = """
Summarize the following pull request description:
{pr_description}
"""

# Template for reviewing code changes
# templates.py

CODE_REVIEW_TEMPLATE = """
You are an AI code reviewer. Please review the following Python code and identify issues in the following categories:
1. Code style and formatting (e.g., PEP8 issues, line length, indentation).
2. Potential bugs or errors (e.g., undefined variables, null pointers).
3. Performance improvements (e.g., inefficient loops, memory usage).
4. Best practices (e.g., code readability, modularity, reusability).

For each issue, please return the output in the following JSON format:

{{
    "type": "issue_type",
    "line": line_number,
    "description": "issue_description",
    "suggestion": "suggested_fix"
}}

Code:
{code}
"""