# Template for summarizing a pull request
PR_SUMMARY_TEMPLATE = """
Summarize the following pull request description:
{pr_description}
"""

# Template for reviewing code changes
CODE_REVIEW_TEMPLATE = """
You are a code reviewer. Review the following code for:
1. Code style issues (e.g., line length, indentation, naming conventions).
2. Potential bugs or errors (e.g., null pointer exceptions, undefined variables).
3. Performance improvements (e.g., inefficient loops, memory usage).
4. Best practices (e.g., code readability, modularity, reusability).

Code:
{code}

Return the review in JSON format with fields: type, line, description, and suggestion.
"""